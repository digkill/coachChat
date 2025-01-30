import streamlit as st

from gigachat_api import send_prompt, get_access_token

st.title("Coach Chat")

if "access_token" not in st.session_state:
    try:
        st.session_state.access_token = get_access_token()
        st.toast("You are now logged in!")
    except Exception as e:
        st.toast(f"Error getting access token: {e}")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "ai", "content": "Решу задачу"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if user_prompt := st.chat_input():
    st.chat_message("user").write(user_prompt)
#    st.toast(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    response = send_prompt(user_prompt, st.session_state.access_token)
    st.chat_message("ai").write(response)
    st.session_state.messages.append({"role": "ai", "content": response})