import time
import os
import requests
from dotenv import load_dotenv
import uuid

load_dotenv()

def text_to_speech(input_response="What is the weather report in india"):
    """
    Generate TTS audio, save it locally, and return the file path.
    Returns:
        str: Path to the saved audio file or None if there's an error
    """
    try:
        token = os.getenv("WAVES_API_KEY")
        if not token:
            raise ValueError("WAVES_API_KEY not found in environment variables")

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

        # Make request to Waves API
        start_time = time.time()
        response = requests.request("POST", url, json=payload, headers=headers)
        
        if response.status_code != 200:
            print(f"Waves API error: {response.status_code}, {response.text}")
            return None

        # Create audio directory if it doesn't exist
        audio_dir = "static/audio"
        os.makedirs(audio_dir, exist_ok=True)

        # Generate unique filename
        filename = f"audio_{uuid.uuid4()}.wav"
        file_path = os.path.join(audio_dir, filename)

        # Save the audio file
        with open(file_path, 'wb') as f:
            f.write(response.content)

        print(f"Audio processing time: {time.time() - start_time:.2f} seconds")
        print(f"Audio saved to: {file_path}")
        
        # Return the URL-friendly path
        return f"/static/audio/{filename}"

    except Exception as e:
        print(f"Error in text_to_speech: {str(e)}")
        return None

if __name__ == "__main__":
    start = time.time()
    path = text_to_speech()
    print(f"Total execution time: {time.time() - start:.2f} seconds")
    print(f"Audio path: {path}")