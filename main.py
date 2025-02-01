import os
import tempfile
from io import StringIO

import streamlit as st
from streamlit_chat import message
from streamlit.components.v1 import html
import anthropic
from gigachat_api import get_access_token, send_prompt_and_get_response, send_file_and_get_response, get_image

audio_path = "https://docs.google.com/uc?export=open&id=16QSvoLWNxeqco_Wb2JvzaReSAw5ow6Cl"
img_path = "https://www.groundzeroweb.com/wp-content/uploads/2017/05/Funny-Cat-Memes-11.jpg"
youtube_embed = '''
<iframe width="400" height="215" src="https://www.youtube.com/embed/LMQ5Gauy17k" title="YouTube video player" frameborder="0" allow="accelerometer; encrypted-media;"></iframe>
'''

markdown = """
### HTML in markdown is ~quite~ **unsafe**
<blockquote>
  However, if you are in a trusted environment (you trust the markdown). You can use allow_html props to enable support for html.
</blockquote>

* Lists
* [ ] todo
* [x] done

Math:

Lift($L$) can be determined by Lift Coefficient ($C_L$) like the following
equation.

$$
L = \\frac{1}{2} \\rho v^2 S C_L
$$

~~~py
import streamlit as st

st.write("Python code block")
~~~

~~~js
console.log("Here is some JavaScript code")
~~~

"""

table_markdown = '''
A Table:

| Feature     | Support              |
| ----------: | :------------------- |
| CommonMark  | 100%                 |
| GFM         | 100% w/ `remark-gfm` |
'''

st.session_state.setdefault(
    'past',
    ['plan text with line break',
     'play the song "Dancing Vegetables"',
     'show me image of cat',
     'and video of it',
     'show me some markdown sample',
     'table in markdown']
)
st.session_state.setdefault(
    'generated',
    []
)


st.title("CodeClass ChatBot")

uploaded_file = st.file_uploader("Загрузить файл", type=("txt", "md", "png", "jpg", "jpeg"))

chat_placeholder = st.empty()

def on_input_change():
    user_input = st.session_state.user_input
    st.session_state.past.append(user_input)
    st.session_state.generated.append("The messages from Bot\nWith new line")

def on_btn_click():
    del st.session_state.past[:]
    del st.session_state.generated[:]

def send_prompt(u_prompt: str):
    st.chat_message("user").write(u_prompt)
    st.session_state.messages.append({"role": "user", "content": u_prompt})

    with st.spinner("Минуточку ..."):
        response_file = ""

        if uploaded_file:
            temp_dir = tempfile.mkdtemp()
            path = os.path.join(temp_dir, uploaded_file.name)

            with open(path, "wb") as f:
                f.write(uploaded_file.getvalue())

            response_file = send_file_and_get_response(path, st.session_state.access_token)
            #   article = uploaded_file.read().decode()
            #   send_prompt(article)
            #   response, is_image = send_prompt_and_get_response(user_prompt, st.session_state.access_token)

            st.chat_message("ai").write(response_file)
            st.session_state.messages.append({"role": "ai", "content": response_file})

            data = get_image(file_id=response_file, access_token=st.session_state.access_token)

            st.chat_message("ai").image(data)
            st.session_state.messages.append({"role": "ai", "content": data, "is_image": True})


        response, is_image = send_prompt_and_get_response(u_prompt, st.session_state.access_token, response_file)
        if is_image:
            st.chat_message("ai").image(response)
            st.session_state.messages.append({"role": "ai", "content": response, "is_image": True})
        else:
            st.chat_message("ai").write(response)
            st.session_state.messages.append({"role": "ai", "content": response})


with chat_placeholder.container():
    for i in range(len(st.session_state['generated'])):
        message(st.session_state['past'][i], is_user=True, key=f"{i}_user")
        message(
            st.session_state['generated'][i]['data'],
            key=f"{i}",
            allow_html=True,
            is_table=True if st.session_state['generated'][i]['type'] == 'table' else False
        )



#with st.container():
#    st.text_input("User Input:", on_change=on_input_change, key="user_input")

#st.html("<style>.st-emotion-cache-13k62yr {background: #222222 !important;}</style>")

if "access_token" not in st.session_state:
    try:
        st.session_state.access_token = get_access_token()
        st.toast("You are now logged in!")
    except Exception as e:
        st.toast(f"Error getting access token: {e}")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "ai", "content": "Привет! Чем могу помочь тебе?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


if user_prompt := st.chat_input():
    send_prompt(user_prompt)




st.button("Очистить чат", on_click=on_btn_click)