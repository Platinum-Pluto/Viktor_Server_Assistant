import os
from dotenv import load_dotenv
import cmd 
import subprocess
from tqdm import tqdm
from manual import print_manual
import sys
import pyaudio
import wave
import time
import platform
import functools
import re
#from pirateking import pirateKing, pirate
import threading, time, sys
from pirateking import pirate
from tts import tts
import sys

load_dotenv()

history = []


CHAR_SFX = os.getenv('CHAR_SFX')


def print_slow(text, delay=0.01, sound_file= CHAR_SFX):
    words = text.split()
    p = pyaudio.PyAudio()
    wf = wave.open(sound_file, 'rb')
    sound_data = wf.readframes(wf.getnframes())
    format = p.get_format_from_width(wf.getsampwidth())
    channels = wf.getnchannels()
    rate = wf.getframerate()
    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    output=True)

    def play_sound():
        stream.write(sound_data)

    for word in words:
        for char in word:
            sys.stdout.write(char)
            sys.stdout.flush()
            play_sound() 
            time.sleep(delay / 10) 
        sys.stdout.write(' ')
        sys.stdout.flush()
        time.sleep(delay)  

    stream.stop_stream()
    stream.close()
    wf.close()
    p.terminate()

    sys.stdout.write('\n')
    sys.stdout.flush()

def restrict_os(allowed_os):
    """Decorator to restrict function execution based on OS."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_os = platform.system()
            if current_os not in allowed_os:
                clean_name = re.sub(r"^do_", "", func.__name__)
                print_slow(f"[WARNING] {clean_name} is restricted on {current_os}. Skipping execution.")
                return  
            return func(*args, **kwargs)
        return wrapper
    return decorator

def run_command_with_progress(command, description):
    with tqdm(total=100, desc=description, bar_format="{l_bar}{bar} [remaining: {remaining}, {n_fmt}/{total_fmt} installed]") as pbar:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
        for line in process.stdout:
            if "progress" in line:
                pbar.update(10)
        process.wait()
        if process.returncode != 0:
            for line in process.stderr:
                print_slow(line.strip())
            raise subprocess.CalledProcessError(process.returncode, command)
        pbar.update(100 - pbar.n)  


def spinner(done_event):
    while not done_event.is_set():
        for cursor in '|/-\\':
            if done_event.is_set():
                break
            sys.stdout.write(cursor)
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write('\b')



class MyTerminal(cmd.Cmd):
    
    prompt = '> '


    def do_say(self, line):
        history.append(f'say {line}')
        print_slow(line)


    def do_man(self, line):
        history.append(f'man {line}')
        print_manual(line)


    def do_greet(self, line):
        history.append(f'greet {line}')
        print_slow("Hello, " + line)

    def do_exit(self, line):
        return True

    def do_cd(self, path):
        try:
            os.chdir(path)
            print_slow(f"Changed directory to {os.getcwd()}")
        except Exception as e:
            print_slow(f"Failed to change directory: {e}")

    def do_history(self, line):
        for i, element in enumerate(history):
            print_slow(f"{i + 1}: {element}")

    def do_save_history(self, output_file_path):
        if not output_file_path:
            output_file_path = "output.txt"
            with open(output_file_path, "w") as file:
                for i, element in enumerate(history):
                    file.write(f"{i + 1}: {element}\n")
        else:
            with open(output_file_path, "w") as file:
                for i, element in enumerate(history):
                    file.write(f"{i + 1}: {element}\n")

    def do_clear(self, line):
        history.clear()
        print_slow("History has been cleared")


        
    def default(self, line):
        try:
            output = subprocess.check_output(line, shell=True)
            print_slow(output.decode())
        except subprocess.CalledProcessError as e:
            print_slow(f"Command failed: {e}")

    
    def do_active(self, line):
        return None
    
    def do_crawl(self, line):
        #crawl4ai to extract data from the link
        return None
    
    def do_rank(self, line):
        #returns top LLM models currently directly from the HF website
        return None
    @restrict_os(["Linux", "Darwin"])  
    def do_monitor(self, line):

        """
        This function runs Snort in a separate terminal and logs alerts in JSON format.
        """
        json_log_file = "/var/log/snort/alert.json"  # Ensure Snort has permission to write here
        command = f"sudo snort -A json -c /etc/snort/snort.conf -l /var/log/snort --alert-json"

        
        try:

            subprocess.Popen(["gnome-terminal", "--", "bash", "-c", command])            
            history.append(f'monitor {command}')
            print_slow(f"Snort is running and logging alerts to {json_log_file}.")
        except Exception as e:
            history.append(f'monitor {command} caused exception {e}')
            print_slow(e)
                


    @restrict_os(["Linux", "Darwin"])  # Allow only on Linux and macOS
    def do_defend(self, line):
        """
        Blocks traffic from a specific IP using UFW and restarts the firewall.
        """
        command = f"sudo ufw deny from {line}"
        restart = "sudo systemctl restart ufw"

        try:
            subprocess.run(command, shell=True, check=True)
            subprocess.run(restart, shell=True, check=True)

            history.append(f'defend {line}')
            print_slow(f"Blocked traffic from {line}.")
            with open("blocked_ips.log", "a") as log_file:
                log_file.write(f"{line}\n")
        except Exception as e:
            history.append(f'defend {line} caused exception {e}')
            print_slow(f"Error: {e}")



    def do_download(self, line):
        #download any file 
        return None    
    
    @restrict_os(["Linux", "Darwin"])  # Allow only on Linux and macOS
    def do_status(self, line):

        #Add in other stuff as well
        status = subprocess.run("sudo ufw status", shell=True, capture_output=True, text=True)
        print_slow(status.stdout)

        return None
    #Get-Process ollama* | Stop-Process -Force | ollama serve
    def do_talk(self, line):
        history.append(f'say {line}')
        done_event = threading.Event()
        spinner_thread = threading.Thread(target=spinner, args=(done_event,))
        spinner_thread.start()

        res = pirate(generation_text = line, model = 'huihui_ai/deepseek-r1-abliterated:7b')
        
        done_event.set()
        spinner_thread.join()

        print_slow(res)
        tts(res)


"""    @restrict_os(["Linux", "Darwin"])  # Allow only on Linux and macOS
    def do_speak(self, line):
        done_event = threading.Event()
        spinner_thread = threading.Thread(target=spinner, args=(done_event,))
        spinner_thread.start()

        res = pirateKing(reference_audio_path = "rupert.mp3", reference_text = "", custom_config = None, generation_text = line, model = 'huihui_ai/deepseek-r1-abliterated:8b')
        
        done_event.set()
        spinner_thread.join()

        print_slow(res)
    
    def do_talk(self, line):
        done_event = threading.Event()
        spinner_thread = threading.Thread(target=spinner, args=(done_event,))
        spinner_thread.start()

        res = pirateKing(generation_text = line, model = 'huihui_ai/deepseek-r1-abliterated:8b')
        
        done_event.set()
        spinner_thread.join()

        print_slow(res)"""
  


if __name__ == '__main__':

    welcome = """
    𝙿𝚛𝚘𝚓𝚎𝚌𝚝 𝚅𝙸𝙺𝚃𝙾𝚁
   """
    print(welcome)
    MyTerminal().cmdloop()


