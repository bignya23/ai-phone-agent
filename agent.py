from src.models import get_llm,gemini_llm
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from src.chains import conversation_chain, conversation_stage_chain, conversation_tool_chain
import src.text_to_speech as text_to_speech
from src.variables import *
from src.tools import *
from src.stages import CONVERSATION_STAGES

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
        # Run the agent
        return response
    except Exception as e:
        return f"Error: {str(e)}"
    
def conversation_tool(conversation_history=""):

    chain = conversation_tool_chain(get_llm())
    try:
        # Prepare input for the agent
        response = chain.invoke({
            "conversation_history": conversation_history
        })

        # Run the agent
        return response
    except Exception as e:
        return f"Error: {str(e)}"



def sales_conversation(conversation_history=""):
    chain = conversation_chain(get_llm())

    try:
        # Prepare input for the agent
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
        
        # Run the agent
        return response
    except Exception as e:
        return f"Error: {str(e)}"
    


if __name__ == "__main__":
    conversation_history = ""
    user_input = ""
    
    while True:
        conversation_history += f"User : {user_input}\n"
        # current_stage = conversation_tool(conversation_history)
        # print(f"Tool : {current_stage}\n")
        response = sales_conversation(conversation_history)
        print(f"Sales Agent: {response}")
        user_input = input("You: ")
        if "<END_OF_CALL>" in user_input:
            print("Sales Agent: Thank you for your time. Have a great day!")
            break
        conversation_history += f"Sales Agent: {response}\n"



