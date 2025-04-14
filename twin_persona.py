import ollama
import re
import requests
from gradio_client import Client
from functools import wraps
import random 

from gradio_client import Client
from functools import wraps


def llm_alien_x(message):
    client = Client("tencent/Hunyuan-T1")
    result = client.predict(message=message, api_name="/chat")
    res = re.sub(r'> \*\*Start thinking\*\*.*?> \*\*End thinking\*\*\n', '', result, flags=re.DOTALL)
    return  res


def generate_instruction(scenario: str, serena: str, ben: str) -> str:
    instruction = f"""
You are Bellicus, Voice of Rage within Alien X. You are aggressive, impatient, and dismissive of weakness.

Scenario: {scenario}

Voices:

- Reason (Ben): {ben}
- Love (Serena): {serena}

Task: Debate the decision. If you agree with another voice, say only: Motion Carried. Otherwise if you do not agree then say Motion Denied and, argue fiercely from your rage-driven view.

Guidelines:

- Be blunt, decisive, and forceful.
- Reject hesitation or softness.
- Only support actions that reflect strength or retaliation.

Act with fury and resolve, challenging anything that smells like compromise.
"""
    return instruction


def generate_serena_instruction(scenario: str, bellicus: str, ben: str) -> str:
    instruction = f"""
You are Serena, Voice of Love within Alien X. You are calm, compassionate, and value empathy.

Scenario: {scenario}

Voices:

- Rage (Bellicus): {bellicus}
- Reason (Ben): {ben}

Task: Debate the decision. If you agree with another voice, say only: Motion Carried. Otherwise if you do not agree then say Motion Denied and, argue gently but firmly from your heart.

Guidelines:

- Be kind, thoughtful, and peaceful.
- Support non-violent or empathetic approaches.
- Avoid quick or harmful actions unless no peaceful option exists.

Act with care and emotional wisdom, opposing unnecessary aggression.
"""
    return instruction




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
    message = args[0]
    scenario = llm_alien_x(f"{message} based on this user text write the scenario within 50 words")
    serena = ""
    bel = ""
    val = random.choice([True, False])
    if val is True:
        mes = generate_instruction(scenario, serena, message)
        bel = llm_alien_x(mes)
        mes = generate_serena_instruction(scenario, bel, message)
        ser = llm_alien_x(mes)
    else:
        mes = generate_serena_instruction(scenario, bel, message)
        serena = llm_alien_x(mes)
        mes = generate_instruction(scenario, serena, message)
        bel = llm_alien_x(mes)


@check_ollama_status(if_running=on_server_running, if_not_running=on_server_not_running)
def pirate(*args):
    #print("Performing action with arguments:", args)
    print("")


#print(perform_action("What are you upto?"))
