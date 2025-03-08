from gradio_client import Client, handle_file
from pydub import AudioSegment
from pydub.playback import play
import os 
from dotenv import load_dotenv

load_dotenv()


tts_path = os.getenv('TTS_PATH')
client = Client("mrfakename/E2-F5-TTS")


def tts(text):
    result = client.predict(
        ref_audio_input=handle_file(tts_path),
        ref_text_input="",
        gen_text_input=text,
        api_name="/basic_tts"
    )

    audio_file = result[0]
    sound = AudioSegment.from_file(audio_file)
    play(sound)  # Play audio in terminal
