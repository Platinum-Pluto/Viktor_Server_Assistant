import requests

def is_ollama_server_running(url="http://localhost:11434", timeout=2):

    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200
    except requests.RequestException:
        return False

if __name__ == "__main__":
    if is_ollama_server_running():
        print("Ollama server is running on localhost.")
    else:
        print("Ollama server is NOT running on localhost.")
