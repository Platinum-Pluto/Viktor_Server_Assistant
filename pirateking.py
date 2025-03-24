import ollama
import re
import requests
from gradio_client import Client
from functools import wraps


INSTRUCTION = "you are the most insane guy ever and you use a lot of curse words such as FUCK, SHIT, and etc you know, in your replies. At the end of your replies always say an Insane fact about yourself"

def check_ollama_status(if_running, if_not_running):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            url = 'http://localhost:11434'
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    func(*args, **kwargs)  # Execute perform_action first
                    return if_running(*args, **kwargs)
            except requests.ConnectionError:
                pass
            func(*args, **kwargs)  # Execute perform_action even if server is not running
            return if_not_running(*args, **kwargs)
        return wrapper
    return decorator

def on_server_running(*args, **kwargs):
    print("Ollama server is running.")
    response = ollama.chat(model=args[1], messages=[
            {
            'role': 'user',
            'content': args[0] + " {INSTRUCTION}"
            },
    ])
    res = response['message']['content']
    res = re.sub(r'<think>.*?</think>', '', res, flags=re.DOTALL)
    return res


def on_server_not_running(*args):
    print("Ollama server is not running.")
    message = f'{args[0]} + {INSTRUCTION}'
    client = Client("tencent/Hunyuan-T1")
    result = client.predict(message=message, api_name="/chat")
    res = re.sub(r'> \*\*Start thinking\*\*.*?> \*\*End thinking\*\*\n', '', result, flags=re.DOTALL)
    return  res


@check_ollama_status(if_running=on_server_running, if_not_running=on_server_not_running)
def pirate(*args):
    print("Performing action with arguments:", args)


#print(perform_action("What are you upto?"))
