import subprocess
import ollama
import re

INSTRUCTION = "you are the most insane guy ever and you use a lot of curse words such as FUCK, SHIT, and etc you know, in your replies. At the end of your replies always say an Insane fact about yourself"

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

