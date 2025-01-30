import json
import uuid

import requests
import streamlit as st
from requests.auth import HTTPBasicAuth

CLIENT_ID = st.secrets["CLIENT_ID"]
CLIENT_SECRET = st.secrets["CLIENT_SECRET"]

# curl -L -X POST 'https://ngw.devices.sberbank.ru:9443/api/v2/oauth' \
# -H 'Content-Type: application/x-www-form-urlencoded' \
# -H 'Accept: application/json' \
# -H 'RqUID: 184f809c-8bea-4420-853f-50027c8152bd' \
# -H 'Authorization: Basic <Authorization key>' \
# --data-urlencode 'scope=GIGACHAT_API_PERS'

def get_access_token() -> str:
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    st.toast(CLIENT_SECRET)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'Authorization': f'Basic {CLIENT_SECRET}',
        'RqUID': str(uuid.uuid4()),
    }
    payload = {"scope": "GIGACHAT_API_PERS"}
    res = requests.post(url=url, headers=headers, data=payload, verify=False)
    st.toast(res.content)
    access_token = res.json()["access_token"]
    return access_token

def get_image():
    pass

def send_prompt(msg: str, access_token: str):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    payload = json.dumps({
        "model": "GigaChat-Pro",
        "messages": [
            {
                "role": "user",
                "content": msg,
            }
        ],
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.post(url, headers=headers, data=payload, verify=False)
    return response.json()["choices"][0]["message"]["content"]

def send_prompt_and_get_response():
    send_prompt()
    ...