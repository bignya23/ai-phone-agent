from langchain.prompts import ChatPromptTemplate
from src.models import get_llm
from langchain.agents import initialize_agent
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from src.chains import conversation_chain
import src.text_to_speech as text_to_speech
from src.variables import *
from src.tools import *

chain = conversation_chain(get_llm())

def sales_conversation(conversation_history=""):
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

def sales_conversation_with_tools(conversation_history=""):
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
        response = sales_conversation(conversation_history)
        print(f"Sales Agent: {response}")
        user_input = input("You: ")
        if "<END_OF_CALL>" in user_input:
            print("Sales Agent: Thank you for your time. Have a great day!")
            break
        conversation_history += f"Sales Agent: {response}\n"



