import os
from groq import Groq

# Initialize the Groq client
client = Groq()

# Specify the path to the audio file

def transcribe(filepath):

    filename = filepath # Replace with your audio file!

    # Open the audio file
    with open(filename, "rb") as file:
        # Create a transcription of the audio file
        transcription = client.audio.transcriptions.create(
        file=(filename, file.read()), # Required audio file
        model="whisper-large-v3-turbo", # Required model to use for transcription
        prompt="Specify context or spelling",  # Optional
        response_format="json",  # Optional
        language="en",  # Optional
        temperature=0.0  # Optional
        )
        # Print the transcription text
     
    return transcription.text