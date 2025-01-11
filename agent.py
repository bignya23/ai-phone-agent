from src.models import get_llm,gemini_llm
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from src.chains import conversation_chain, conversation_stage_chain, conversation_tool_chain
from src.text_to_speech import text_to_speech, play_audio_from_response
from src.variables import *
from src.tools import *
from src.stages import CONVERSATION_STAGES
import asyncio
from pydub import AudioSegment
from pydub.playback import play
import time
from playsound import playsound
from speech_to_text import audio_file, speech_to_text
conversation_stage_id = 1

def get_conversation_stage(conversation_history=""):

    global conversation_stage_id
    chain = conversation_stage_chain(get_llm())
    try:
        # Prepare input for the agent
        response = chain.invoke({
            "conversation_stage_id" : conversation_stage_id,
            "conversation_history": conversation_history,
            "conversation_stages" : CONVERSATION_STAGES
        })
        # print(response)

        conversation_stage_id = response
        return response
    except Exception as e:
        return f"Error: {str(e)}"
    
def conversation_tool(conversation_history=""):

    chain = conversation_tool_chain(get_llm())
    try:
        response = chain.invoke({
            "conversation_history": conversation_history
        })

        # Run the agent
        return response
    except Exception as e:
        return f"Error: {str(e)}"



def sales_conversation(salesperson_name, salesperson_role, company_name, company_business, company_values, conversation_purpose, conversation_type, conversation_history=""):
    chain = conversation_chain(get_llm())

    try:
        response = chain.invoke({
            "salesperson_name" : salesperson_name,
            "salesperson_role" : salesperson_role,
            "company_name" : company_name,
            "company_business": company_business,
            "company_values" :company_values,
            "conversation_purpose": conversation_purpose,
            "conversation_type" : conversation_type,
            "conversation_history": conversation_history
        })
        
        return response
    except Exception as e:
        return f"Error: {str(e)}"

# def split_message_at_middle_period(message):
#     mid_index = len(message) // 2  # Find the middle index
#     # Look for the nearest full stop before and after the middle index
#     before_period = message.rfind('.', 0, mid_index)
#     after_period = message.find('.', mid_index)
    
#     # Determine which period is closer to the middle
#     if before_period == -1 and after_period == -1:
#         # No full stops in the message, return the entire message as one chunk
#         return [message]
#     elif before_period == -1:  # No period before the middle
#         split_index = after_period + 1
#     elif after_period == -1:  # No period after the middle
#         split_index = before_period + 1
#     else:  # Choose the closest full stop
#         split_index = before_period + 1 if (mid_index - before_period) <= (after_period - mid_index) else after_period + 1
    
#     # Split the message at the closest full stop
#     return [message[:split_index].strip(), message[split_index:].strip()]


def main():
    conversation_history = ""
    user_input = ""
    
    while True:
        conversation_history += f"User : {user_input}\n"
        # current_stage = conversation_tool(conversation_history)
        # print(f"Tool : {current_stage}\n")
        start = time.time()
        response = sales_conversation(conversation_history)

        if response.endswith("<END_OF_TURN>"):
            clean_message = response.split("<END_OF_TURN>")[0].strip()
        
        if response.endswith("<END_OF_CALL>"):
            clean_message = response.split("<END_OF_CALL>")[0].strip()


        print(f"Sales Agent: {clean_message}")
        # messages = [clean_message]
        # if len(clean_message) > 150:
        #     messages = split_message_at_middle_period(clean_message)
        
    
        # await text_to_speech(response)
        end = time.time()
        
        print(f"Time Taken : {end - start}")
        print("Playing audio....")

        file_path = text_to_speech(clean_message)
        playsound(file_path)

        if response.endswith("<END_OF_CALL>"):
            break
        # user_input = input("You: ")
        filename = audio_file()
        user_input = speech_to_text(filename)
        conversation_history += f"Sales Agent: {clean_message}\n"

if __name__ == "__main__":
    main()



