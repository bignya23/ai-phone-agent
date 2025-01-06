from langchain.prompts import ChatPromptTemplate
from models import get_llm
from langchain.agents import initialize_agent
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from chains import conversation_chain
import text_to_speech

chain = conversation_chain(get_llm())

# agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def sales_conversation(conversation_history=""):
    try:
        # Prepare input for the agent
        response = chain.invoke({
            "salesperson_name" : "Alex",
            "salesperson_role" : "Business Development Representative",
            "company_name" : "Sleep Haven",
            "company_business": """Sleep Haven is a premium mattress company that provides customers with the most comfortable and supportive sleeping experience possible. We offer a range of high-quality mattresses, pillows, and bedding accessories that are designed to meet the unique needs of our customers.""",
            "company_values" : """Our mission at Sleep Haven is to help people achieve a better night's sleep by providing them with the best possible sleep solutions. We believe that quality sleep is essential to overall health and well-being, and we are committed to helping our customers achieve optimal sleep by offering exceptional products and customer service.""",
            "conversation_purpose": "find out whether they are looking to achieve better sleep via buying a premier mattress.",
            "conversation_type" : "call",
            "conversation_history": conversation_history
        })
        
        # Run the agent
        return response
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    conversation_history = ""
    print("Sales Agent: Hello! This is Alex from TechCorp. How can I assist you today?")
    
    while True:
        user_input = input("You: ")
        if "<END_OF_CALL>" in user_input:
            print("Sales Agent: Thank you for your time. Have a great day!")
            break
        conversation_history += f"User : {user_input}\n"
        response = sales_conversation(conversation_history)
        print(f"Sales Agent: {response}")
        conversation_history += f"Sales Agent: {response}\n"



