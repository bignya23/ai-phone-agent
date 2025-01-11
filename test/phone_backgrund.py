from pydub.generators import WhiteNoise
from pydub import AudioSegment
import random

def generate_phone_call_background(duration=10):
    """
    Generate background sound for a phone call with faint static noise and occasional beeps.

    Parameters:
    - duration: Duration of the audio in seconds.

    Returns:
    - AudioSegment object containing the generated sound.
    """
    # Generate white noise for static background
    static_noise = WhiteNoise().to_audio_segment(duration=duration * 1000, volume=-30)  # Adjust volume

    # Create occasional faint beeps
    beep = AudioSegment.sine(frequency=1000).apply_gain(-20).fade_in(50).fade_out(50)
    beeps = AudioSegment.silent(duration=0)
    for _ in range(random.randint(2, 5)):  # Add 2-5 random beeps
        start_time = random.randint(0, duration - 1) * 1000  # Random time within duration
        beeps = beeps.overlay(beep, position=start_time)

    # Mix static noise with beeps
    phone_call_background = static_noise.overlay(beeps)

    return phone_call_background

# Generate and export the sound
phone_call_sound = generate_phone_call_background(duration=10)  # 10-second sound
phone_call_sound.export("phone_call_background.wav", format="wav")
print("Phone call background sound generated and saved as 'phone_call_background.wav'.")
