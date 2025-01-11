from flask import Flask, request, redirect, url_for, jsonify
import requests
import agent
import speech_to_text
import src.text_to_speech
import time
import playsound
app = Flask(__name__)

conversation_history = ""
user_input = ""

@app.route("/get_info" , methods =["POST"])
def get_info():
    data = request.get_json()

    salesperson_name = data.get("salesperson_name")
    salesperson_role = data.get("salesperson_role")
    company_name = data.get("company_name")
    company_business = data.get("company_business")
    company_values = data.get("company_values")
    conversation_purpose = data.get("conversation_purpose")
    conversation_type = data.get("conversation_type")

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

    response = get_info()
    
    data = response.get_json()

    salesperson_name = data["salesperson_name"]
    salesperson_role = data["salesperson_role"]
    company_name = data["company_name"]
    company_business = data["company_business"]
    company_values = data["company_values"]
    conversation_purpose = data["conversation_purpose"]
    conversation_type = data["conversation_type"]


    while True:  
        conversation_history += f"User : {user_input}\n"
        start = time.time()
        response = agent.sales_conversation(salesperson_name, salesperson_role, company_name, company_business, company_values, conversation_purpose, conversation_type,conversation_history)

        if response.endswith("<END_OF_TURN>"):
            clean_message = response.split("<END_OF_TURN>")[0].strip()
            
        if response.endswith("<END_OF_CALL>"):
            clean_message = response.split("<END_OF_CALL>")[0].strip()
            break
        else:
            clean_message = response.strip()
            
        end = time.time()
            
        print(f"Time Taken : {end - start}")
        print("Playing audio....")

        file_path = src.text_to_speech.text_to_speech(clean_message)
        playsound.playsound(file_path)

        if response.endswith("<END_OF_CALL>"):
            pass
            # user_input = input("You: ")
        filename = speech_to_text.audio_file()
        user_input = speech_to_text.speech_to_text(filename)
        conversation_history += f"Sales Agent: {clean_message}\n"

    return jsonify({
       "The call has ended..."
    })


if __name__ == "__main__":
    app.run(debug=True)