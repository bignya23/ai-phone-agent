from flask import Flask, request, jsonify
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather
from agent import sales_conversation
from src.text_to_speech import text_to_speech
import requests
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure Twilio client
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
BASE_URL = os.getenv('BASE_URL', 'https://764e-14-139-217-140.ngrok-free.app')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Global conversation history string
conversation_history = ""

@app.route("/call_user", methods=["POST"])
def call_user():
    """Initiate a call to a specified phone number."""
    try:
        data = request.get_json()
        to_phone = data.get("to_phone")
        
        if not to_phone:
            return jsonify({"error": "Please provide a valid phone number."}), 400
        
        call = client.calls.create(
            to=to_phone,
            from_=TWILIO_PHONE_NUMBER,
            url=f"{BASE_URL}/handle_call",
            status_callback=f"{BASE_URL}/call_status",
            status_callback_event=['completed', 'failed']
        )
        
        logger.info(f"Initiated call to {to_phone} with SID: {call.sid}")
        return jsonify({
            "message": "Call initiated successfully",
            "call_sid": call.sid
        }), 200
        
    except Exception as e:
        logger.error(f"Error initiating call: {str(e)}")
        return jsonify({"error": "Failed to initiate call"}), 500

@app.route("/handle_call", methods=["POST"])
def handle_call():
    """Handle initial call and subsequent interactions."""
    try:
        response = VoiceResponse()
        # welcome_message = "Please state your query after the beep."
        # response.say(welcome_message, voice="alice")
        
        gather = Gather(
            input="speech",
            timeout=3,
            speech_timeout="auto",
            action="/process_query",
            method="POST",
            language="en-US",
            enhanced=True
        )
        
        response.append(gather)
        response.redirect("/handle_call")
        
        return str(response), 200
        
    except Exception as e:
        logger.error(f"Error in handle_call: {str(e)}")
        return str(VoiceResponse().say("An error occurred. Please try again later.")), 500

@app.route("/process_query", methods=["POST"])
def process_query():
    """Process user's speech input and generate response."""
    global conversation_history
    try:
        speech_result = request.values.get('SpeechResult')
        
        if not speech_result:
            response = VoiceResponse()
            response.say("I couldn't hear anything. Please try again.", voice="alice")
            response.redirect("/handle_call")
            return str(response)
        
        logger.info(f"Received speech input: {speech_result}")
        
        # Update conversation history
        conversation_history += f"User: {speech_result}\n"
        
        # Generate AI response
        llm_response = sales_conversation(conversation_history)
        print(llm_response)
        conversation_history += f"Agent: {llm_response}\n"
        
        # Convert response to speech
        try:
            audio_url = text_to_speech(llm_response)
            
            response = VoiceResponse()
            response.play(audio_url)
            # response.pause(length=1)
            response.redirect("/handle_call")
            
            return str(response)
            
        except Exception as e:
            logger.error(f"TTS Error: {str(e)}")
            # Fallback to basic TTS if custom TTS fails
            response = VoiceResponse()
            response.say(llm_response, voice="alice")
            response.redirect("/handle_call")
            return str(response)
            
    except Exception as e:
        logger.error(f"Error in process_query: {str(e)}")
        response = VoiceResponse()
        response.say("An error occurred processing your request. Please try again.", voice="alice")
        response.redirect("/handle_call")
        return str(response)

@app.route("/call_status", methods=["POST"])
def call_status():
    """Handle call status callbacks and cleanup."""
    global conversation_history
    status = request.values.get('CallStatus')
    
    if status in ['completed', 'failed']:
        # Reset conversation history when call ends
        conversation_history = ""
            
    logger.info(f"Call ended with status: {status}")
    return "", 200

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True)