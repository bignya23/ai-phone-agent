import requests
import os
import aiagent
import wave
import pyaudio

def save_wav_file(response, file_path="output.wav"):
    """
    Save the WAV file from the API response.
    """
    if response.status_code == 200:
        with open(file_path, "wb") as wav_file:
            wav_file.write(response.content)
        print(f"WAV file saved as {file_path}")
    else:
        print(f"Failed to save WAV file. Status code: {response.status_code}, Response: {response.text}")

def play_wav_file(file_path):
    """
    Play the WAV file using PyAudio.
    """
    chunk = 1024  # Chunk size for reading the WAV file

    with wave.open(file_path, 'rb') as wf:
        p = pyaudio.PyAudio()

        # Open stream
        stream = p.open(
            format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True
        )

        # Read and play the WAV file in chunks
        data = wf.readframes(chunk)
        while data:
            stream.write(data)
            data = wf.readframes(chunk)

        # Close the stream
        stream.stop_stream()
        stream.close()
        p.terminate()
        print(f"Finished playing {file_path}")


def text_to_speech(input_response = "What is the weather report"):
    # Main code
    token = os.getenv("WAVES_API_KEY")

    url = "https://waves-api.smallest.ai/api/v1/lightning/get_speech"

    payload = {
        "voice_id": "emily",
        "text": input_response,
        "sample_rate": 24000,
        "add_wav_header": True
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    # Save and play the WAV file
    wav_file_path = "output.wav"
    save_wav_file(response, wav_file_path)
    play_wav_file(wav_file_path)


if __name__ == "__main__":
    text_to_speech()