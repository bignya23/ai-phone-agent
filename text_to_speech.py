import time
import os
import requests
import pyaudio
import wave
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

def play_audio_from_response(response):
    """
    Play WAV audio directly from the API response.
    """
    if response.status_code == 200:
        # Load audio content into a BytesIO stream
        audio_stream = BytesIO(response.content)

        # Read the WAV file from the stream
        with wave.open(audio_stream, 'rb') as wf:
            p = pyaudio.PyAudio()

            # Open a PyAudio stream
            stream = p.open(
                format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True
            )

            # Play the audio in chunks
            chunk = 1024
            data = wf.readframes(chunk)
            while data:
                stream.write(data)
                data = wf.readframes(chunk)

            # Close the stream
            stream.stop_stream()
            stream.close()
            p.terminate()
            print("Audio played successfully.")
    else:
        print(f"Failed to generate TTS audio. Status code: {response.status_code}, Response: {response.text}")

def text_to_speech(input_response="What is the weather report in india"):
    """
    Generate TTS audio and play it directly.
    """
    token = os.getenv("WAVES_API_KEY")
    start_in = time.time()
    url = "https://waves-api.smallest.ai/api/v1/lightning/get_speech"

    payload = {
        "voice_id": "arman",
        "text": input_response,
        "sample_rate": 8000,
        "add_wav_header": True
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    end_in = time.time()
    print(end_in - start_in)
    # Play audio directly from the response
    play_audio_from_response(response)


if __name__ == "__main__":
    start = time.time()
    text_to_speech()
    end = time.time()
    print(end - start)