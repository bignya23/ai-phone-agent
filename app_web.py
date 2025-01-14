from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import agent
import src.speech_to_text as speech_to_text
import src.text_to_speech
import src.tools

app = Flask(__name__)

UPLOAD_FOLDER = "frontend/src/audio"  # Directory to save audio files
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

CORS(app, resources={
    r"/*": {
        "origins": [
            "https://ai-phone-agent-1.onrender.com",  # Frontend domain
            "http://localhost:5173",  # Local development
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Range", "X-Content-Range"],
        "supports_credentials": True,
        "max_age": 3600
    }
})


# Add CORS headers to all responses
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'https://ai-phone-agent-1.onrender.com')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

conversation_history = ""
user_input = ""
inputs = {}
tools_response = ""


@app.route("/get_info", methods=["POST", "OPTIONS"])
def get_info():

    if request.method == "OPTIONS":
        return "", 204
    
    data = request.get_json()
    global inputs
    
    inputs = {
        "salesperson_name": data.get("salespersonName"),
        "salesperson_role": data.get("salespersonRole"),
        "company_name": data.get("companyName"),
        "company_business": data.get("companyBusiness"),
        "company_values": data.get("companyValues"),
        "conversation_purpose": data.get("conversationPurpose"),
        "conversation_type": data.get("conversationType"),
        "use_tools" : data.get("withTools")
    }
    
    return jsonify(inputs)


@app.route("/audio/<path:filename>")
def serve_audio(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/agent", methods=["GET", "OPTIONS"])
def main_agent():

    if request.method == "OPTIONS":
        return "", 204

    
    global conversation_history
    global user_input
    global inputs
    global tools_response

    # Generate response from agent
    response = agent.sales_conversation_with_tools(
        inputs["salesperson_name"],
        inputs["salesperson_role"],
        inputs["company_name"],
        inputs["company_business"],
        inputs["company_values"],
        inputs["conversation_purpose"],
        inputs["conversation_type"],
        tools_response,
        conversation_history,
    )

    clean_message = response
    isendofcall = False
    if response.endswith("<END_OF_TURN>"):
        clean_message = response.split("<END_OF_TURN>")[0].strip()
    
    if response.endswith("<END_OF_CALL>"):
        clean_message = response.split("<END_OF_CALL>")[0].strip()
        isendofcall = True

    # Generate audio file
    try:
        audio_file_name = src.text_to_speech.text_to_speech(clean_message)
        audio_file_full_path = os.path.join(app.config["UPLOAD_FOLDER"], audio_file_name)
        print(audio_file_full_path)
        audio_url = f"https://ai-phone-agent.onrender.com/{audio_file_name}"
        print(audio_url)
    except Exception as e:
        return jsonify({"error": f"Failed to generate TTS: {str(e)}"}), 500
    
    conversation_history += f"Sales Agent: {clean_message}\n"

    return jsonify({
        "message": clean_message,
        "audioUrl": audio_url,
        "isEndOfCall": isendofcall
    })

@app.route("/upload_audio", methods=["POST", "OPTIONS"])
def upload_audio():


    if request.method == "OPTIONS":
        return "", 204

    
    global conversation_history
    global user_input
    global inputs
    global tools_response

    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    print("Audio Received")

    # Save the received audio file temporarily
    temp_filename = "frontend_recording.wav"
    audio_file.save(temp_filename)
    
    # Convert speech to text
    try:
        user_input = speech_to_text.speech_to_text(temp_filename)
    except Exception as e:
        return jsonify({"error": f"Failed to process audio: {str(e)}"}), 500
    
    conversation_history += f"User: {user_input}\n"
    print(user_input)
    tools_response = ""
    if inputs["use_tools"] == True:
        tools_response_json = agent.conversation_tool(conversation_history)
        print(f"Tools : {tools_response_json}\n")
        if tools_response_json != "NO":
            tools_response = src.tools.get_tools_response(tools_response_json)

        print(f"Tools Response {tools_response}" )

    # Generate response from agent
    response = agent.sales_conversation_with_tools(
        inputs["salesperson_name"],
        inputs["salesperson_role"],
        inputs["company_name"],
        inputs["company_business"],
        inputs["company_values"],
        inputs["conversation_purpose"],
        inputs["conversation_type"],
        tools_response,
        conversation_history
    )
    print("Generating response")

    clean_message = response
    isendofcall = False
    if response.endswith("<END_OF_TURN>"):
        clean_message = response.split("<END_OF_TURN>")[0].strip()
    
    if response.endswith("<END_OF_CALL>"):
        clean_message = response.split("<END_OF_CALL>")[0].strip()
        isendofcall = True

    # Generate audio file
    try:
        audio_file_name = src.text_to_speech.text_to_speech(clean_message)
        audio_file_full_path = os.path.join(app.config["UPLOAD_FOLDER"], audio_file_name)
        print(audio_file_full_path)
        audio_url = f"https://ai-phone-agent.onrender.com/audio/{audio_file_name}"
        print(audio_url)
    except Exception as e:
        return jsonify({"error": f"Failed to generate TTS: {str(e)}"}), 500
    
    conversation_history += f"Sales Agent: {clean_message}\n"
    
    # Clean up temporary audio file
    os.remove(temp_filename)

    return jsonify({
        "message": clean_message,
        "audioUrl": audio_url,
        "isEndOfCall": isendofcall
    })

if __name__ == "__main__":
    app.run(debug=True)
