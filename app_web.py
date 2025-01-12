from flask import Flask, request, redirect, url_for, jsonify
from flask_cors import CORS  # Importing CORS
import requests
import agent
import speech_to_text
import src.text_to_speech
import time
import playsound

app = Flask(__name__)

# Initialize CORS to allow all domains by default
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])  # Change to match your frontend URL

conversation_history = ""
user_input = ""
inputs = {}

@app.route("/get_info", methods=["POST"])
def get_info():
    data = request.get_json()
    global inputs

    salesperson_name = data.get("salespersonName")
    salesperson_role = data.get("salespersonRole")
    company_name = data.get("companyName")
    company_business = data.get("companyBusiness")
    company_values = data.get("companyValues")
    conversation_purpose = data.get("conversationPurpose")
    conversation_type = data.get("conversation_type")


    inputs = {
        "salesperson_name": salesperson_name,
        "salesperson_role": salesperson_role,
        "company_name": company_name,
        "company_business": company_business,
        "company_values": company_values,
        "conversation_purpose": conversation_purpose,
        "conversation_type": conversation_type
    }

    return jsonify({
        "salesperson_name": salesperson_name,
        "salesperson_role": salesperson_role,
        "company_name": company_name,
        "company_business": company_business,
        "company_values": company_values,
        "conversation_purpose": conversation_purpose,
        "conversation_type": conversation_type
    })

@app.route("/agent", methods=["POST"])
def main_agent():
    global conversation_history
    global user_input
    global inputs

    salesperson_name = inputs["salesperson_name"]
    salesperson_role = inputs["salesperson_role"]
    company_name =inputs["company_name"]
    company_business = inputs["company_business"]
    company_values = inputs["company_values"]
    conversation_purpose = inputs["conversation_purpose"]
    conversation_type = inputs["conversation_type"]
    print(salesperson_name)
    print(salesperson_role)

    while True:
        conversation_history += f"User : {user_input}\n"
        start = time.time()
        response = agent.sales_conversation(salesperson_name, salesperson_role, company_name, company_business, company_values, conversation_purpose, conversation_type, conversation_history)

        clean_message = response

        if response.endswith("<END_OF_TURN>"):
            clean_message = response.split("<END_OF_TURN>")[0].strip()
            
        if response.endswith("<END_OF_CALL>"):
            clean_message = response.split("<END_OF_CALL>")[0].strip()
            break

        end = time.time()
        print(clean_message)
            
        print(f"Time Taken : {end - start}")
        print("Playing audio....")

        file_path = src.text_to_speech.text_to_speech(clean_message)
        # fronend play
        playsound.playsound(file_path)
        
    
        if response.endswith("<END_OF_CALL>"):
            break
        
        # frontend recording file 
        filename = speech_to_text.audio_file()
        user_input = speech_to_text.speech_to_text(filename)
        # user_input = input("You: ")
        print(user_input)
        conversation_history += f"Sales Agent: {clean_message}\n"

    return jsonify({
       "message" : "The call has ended..."
    })

if __name__ == "__main__":
    app.run(debug=True)
