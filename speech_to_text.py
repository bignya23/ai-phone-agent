import time
import torch
import pyaudio
import wave
import os
import numpy as np
import asyncio
from faster_whisper import WhisperModel
from queue import Queue

# Initialize Whisper model
device = "cuda" if torch.cuda.is_available() else "cpu"

def setup_audio_stream():
    """Setup the PyAudio stream."""
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    return p, stream

async def record_audio(queue, silence_threshold=2000, silence_duration=2):
    """Asynchronously record audio and send frames to the queue."""
    print(f"Recording audio... Press Ctrl+C to stop.")

    frames_per_buffer = 1024
    sample_rate = 16000
    p, stream = setup_audio_stream()

    try:
        silence_frames = 0

        while True:
            data = stream.read(frames_per_buffer)
            audio_data = np.frombuffer(data, dtype=np.int16)
            volume_norm = np.linalg.norm(audio_data)

            if volume_norm < silence_threshold:
                silence_frames += 1
            else:
                silence_frames = 0

            # Stop recording on prolonged silence
            if silence_frames > silence_duration * (sample_rate / frames_per_buffer):
                print("Silence detected, stopping recording...")
                break

            # Add audio data to the queue for transcription
            queue.put(data)

            await asyncio.sleep(0)  # Yield control to other tasks

    except KeyboardInterrupt:
        print("\nRecording stopped.")

    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

async def transcribe_audio(queue, model):
    """Asynchronously transcribe audio from the queue."""
    print("Starting transcription...")
    audio_data = b""

    while True:
        # Collect audio chunks from the queue
        while not queue.empty():
            audio_data += queue.get()

        if audio_data:
            # Save the audio data to a temporary WAV file
            temp_file = "temp_audio.wav"
            save_audio_to_file(audio_data, temp_file)

            # Transcribe the temporary audio file
            segments, _ = model.transcribe(temp_file)
            for segment in segments:
                print(f"Transcription: {segment.text}")

            # Clear audio data after transcription
            audio_data = b""

        await asyncio.sleep(0.5)  # Polling interval for transcription

def save_audio_to_file(audio_data, filename):
    """Save the audio data to a WAV file."""
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)  # Mono audio
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))  # 16-bit audio
        wf.setframerate(16000)  # 16kHz sample rate
        wf.writeframes(audio_data)

async def main():
    # Initialize the Whisper model
    model_size = "base"
    model = WhisperModel(model_size, device=device)

    # Create a shared queue for audio data
    queue = Queue()

    # Start recording and transcribing tasks
    await asyncio.gather(
        record_audio(queue),
        transcribe_audio(queue, model)
    )

if __name__ == "__main__":
    asyncio.run(main())
