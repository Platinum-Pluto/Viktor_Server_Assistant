import subprocess
import ollama
import re
import requests
from gradio_client import Client
from functools import wraps
INSTRUCTION = "you are the most insane guy ever and you use a lot of curse words such as FUCK, SHIT, and etc you know, in your replies. At the end of your replies always say an Insane fact about yourself"

"""
def pirate(generation_text = "Hello there!", model = 'huihui_ai/deepseek-r1-abliterated:7b'):
    response = ollama.chat(model=model, messages=[
        {
        'role' : 'user',
        'content' : generation_text+" {INSTRUCTION}"
        },
    ])
    res = response['message']['content']
    res = re.sub(r'<think>.*?</think>', '', res, flags=re.DOTALL)
    return res 


def is_ollama_server_running(url="http://localhost:11434", timeout=2):

    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200
    except requests.RequestException:
        return False

def pirate(generation_text="Hello there!", model='huihui_ai/deepseek-r1-abliterated:7b'):
    if not is_ollama_server_running():
        print("Ollama offline")
        message = f'{generation_text} + {INSTRUCTION}'
        client = Client("tencent/Hunyuan-T1")
        result = client.predict(message=message, api_name="/chat")
        return  result
    else:
        response = ollama.chat(model=model, messages=[
            {
            'role': 'user',
            'content': generation_text + " {INSTRUCTION}"
            },
        ])
        res = response['message']['content']
        res = re.sub(r'<think>.*?</think>', '', res, flags=re.DOTALL)
        return res
"""