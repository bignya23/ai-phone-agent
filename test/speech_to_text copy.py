import os
from groq import Groq
import time
# Initialize the Groq client

start = time.time()
client = Groq()

# Specify the path to the audio file
filename = os.path.dirname(__file__) + "/audio/output.wav" # Replace with your audio file!


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
    print(transcription.text)

end = time.time()

print(end - start)