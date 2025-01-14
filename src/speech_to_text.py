
import wave
# import numpy as np
import time
from collections import deque

# # Audio configuration
# CHUNK = 1024  # Frames per buffer
# FORMAT = pyaudio.paInt16  # Audio format
# CHANNELS = 1  # Mono
# RATE = 16000  # Sampling rate
# SILENCE_THRESHOLD = 2000  # RMS threshold for silence
# SILENCE_DURATION = 1.0  # Silence duration in seconds to trigger save
# SILENCE_DELAY = 5  # Number of consecutive silent chunks to confirm silence
# DETECTION_START_SECONDS = 1.5  # Time in seconds before silence detection begins

# def detect_silence(audio_chunk):
#     """Detect silence based on RMS energy."""
#     rms = np.sqrt(np.mean(np.square(audio_chunk)))
#     return rms < SILENCE_THRESHOLD

# def save_audio(filename, frames, rate):
#     """Save audio frames to a WAV file."""
#     wf = wave.open(filename, 'wb')
#     wf.setnchannels(CHANNELS)
#     wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
#     wf.setframerate(rate)
#     wf.writeframes(b''.join(frames))
#     wf.close()

# def audio_file():
#     p = pyaudio.PyAudio()
#     stream = p.open(
#         format=FORMAT,
#         channels=CHANNELS,
#         rate=RATE,
#         input=True,
#         frames_per_buffer=CHUNK,
#     )

#     print("Recording... Press Ctrl+C to stop.")

#     audio_frames = []
#     silence_queue = deque(maxlen=SILENCE_DELAY)  # Queue to track silent chunks
#     file_count = 1
#     silence_start_time = None
#     recording_start_time = time.time()

#     try:
#         while True:
#             # Read audio data
#             audio_data = stream.read(CHUNK, exception_on_overflow=False)
#             audio_array = np.frombuffer(audio_data, dtype=np.int16)
#             audio_frames.append(audio_data)

#             # Skip silence detection if recording hasn't reached the start time
#             elapsed_time = time.time() - recording_start_time
#             if elapsed_time < DETECTION_START_SECONDS:
#                 continue

#             # Detect silence and maintain a queue of results
#             is_silent = detect_silence(audio_array)
#             silence_queue.append(is_silent)

#             # Confirm silence only if all recent chunks are silent
#             if all(silence_queue):
#                 if silence_start_time is None:
#                     silence_start_time = time.time()
#                 elif time.time() - silence_start_time >= SILENCE_DURATION:
#                     # Save audio segment when silence persists
#                     filename = "audio_segment.wav"
#                     save_audio(filename, audio_frames, RATE)
#                     print(f"Saved: {filename}")
#                     return filename
#             else:
#                 silence_start_time = None
#                 return None

#     except KeyboardInterrupt:
#         print("Recording stopped.")
#         # Save any remaining audio
#         if audio_frames:
#             filename = f"audio_segment_{file_count}.wav"
#             save_audio(filename, audio_frames, RATE)
#             print(f"Saved: {filename}")

#     finally:
#         stream.stop_stream()
#         stream.close()
#         p.terminate()

def speech_to_text(filename):
    import os
    from groq import Groq

    # Initialize the Groq client
    client = Groq()


    # Open the audio file
    with open(filename, "rb") as file:
        transcription = client.audio.transcriptions.create(
        file=(filename, file.read()), 
        model="whisper-large-v3-turbo", 
        prompt="Specify context or spelling",  
        response_format="json",  
        language="en",  
        temperature=0.0  
        )

        return transcription.text

if __name__ == "__main__":
    # filename = audio_file()
    # print(speech_to_text(filename))
    pass
