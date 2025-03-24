import requests

def is_ollama_running():
    url = 'http://localhost:11434'
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True
    except requests.ConnectionError:
        pass
    return False

if __name__ == "__main__":
    if is_ollama_running():
        print("Ollama server is running.")
    else:
        print("Ollama server is not running.")
