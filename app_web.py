from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import agent
import src.speech_to_text as speech_to_text
import src.text_to_speech
import src.tools

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

conversation_history = ""
user_input = ""
inputs = {}
tools_response = ""

@app.route("/get_info", methods=["POST"])
def get_info():
    data = request.get_json()
    global inputs
    
    inputs = {
        "salesperson_name": data.get("salespersonName"),
        "salesperson_role": data.get("salespersonRole"),
        "company_name": data.get("companyName"),
        "company_business": data.get("companyBusiness"),
        "company_values": data.get("companyValues"),
        "conversation_purpose": data.get("conversationPurpose"),
        "conversation_type": data.get("conversation_type"),
        "use_tools" : data.get("use_tools")
    }
    
    return jsonify(inputs)

@app.route("/agent", methods=["GET"])
def main_agent():
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
        audio_file_path = src.text_to_speech.text_to_speech(clean_message)
    except Exception as e:
        return jsonify({"error": f"Failed to generate TTS: {str(e)}"}), 500
    
    conversation_history += f"Sales Agent: {clean_message}\n"

    return jsonify({
        "message": clean_message,
        "audioUrl": audio_file_path,
        "isEndOfCall": isendofcall
    })

@app.route("/upload_audio", methods=["POST"])
def upload_audio():
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
    if inputs["use_tools"] == "true":
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
        audio_file_path = src.text_to_speech.text_to_speech(clean_message)
    except Exception as e:
        return jsonify({"error": f"Failed to generate TTS: {str(e)}"}), 500
    
    conversation_history += f"Sales Agent: {clean_message}\n"
    
    # Clean up temporary audio file
    os.remove(temp_filename)

    return jsonify({
        "message": clean_message,
        "audioUrl": audio_file_path,
        "isEndOfCall": isendofcall
    })

if __name__ == "__main__":
    app.run(debug=True)
