import torch
import pyaudio
import wave
import os
import numpy as np
from faster_whisper import WhisperModel

# Initialize Whisper model
device = "cuda" if torch.cuda.is_available() else "cpu"

def record_audio(p, stream, filename, silence_threshold = 2000, silence_duration = 2):
    """Record audio from the microphone and save it to a single file."""
    frames_per_buffer = 1024
    sample_rate = 16000
    channels = 1
    sampwidth = p.get_sample_size(pyaudio.paInt16)  # 16-bit audio
    
    frames = []  # Accumulate audio data
    silence_frames = 0

    print(f"Recording audio... Press Ctrl+C to stop.")
    
    try:
        while True: 
            data = stream.read(frames_per_buffer)
            frames.append(data)


            audio_data = np.frombuffer(data, dtype=np.int16)
            volume_norm = np.linalg.norm(audio_data)

            if volume_norm < silence_threshold:
                silence_frames += 1
            else:
                silence_frames = 0

            if silence_frames > silence_duration * (sample_rate / frames_per_buffer):
                print("Silence detected, stopping recording...")
                break

    except KeyboardInterrupt:
        print("\nRecording stopped.")

    # Save the recorded audio to a single WAV file
    save_audio_to_file(b''.join(frames), filename)

def save_audio_to_file(audio_data, filename):
    """Save the audio data to a WAV file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)  # Mono audio
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))  # 16-bit audio
        wf.setframerate(16000)  # 16kHz sample rate
        wf.writeframes(audio_data)

def speech_to_text():
    # Initialize the Whisper model
    model_size = "base"
    model = WhisperModel(model_size, device=device)

    # Microphone Input Setup
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

    print("Listening for speech... Press Ctrl+C to stop.")

    # Record a single audio file
    audio_file = "audio/captured_audio.wav"
    record_audio(p, stream, audio_file)

    # Transcribe the recorded audio file
    segments, _ = model.transcribe(audio_file)

    # Extract and print the transcription
    transcription = []
    for segment in segments:
        print(f"Transcription: {segment.text}")
        transcription.append(segment.text)

    # print("\nFinal Transcription:")
    text = ""
    for t in transcription:
        text += t

    return text
   

if __name__ == "__main__":
    speech_to_text()
