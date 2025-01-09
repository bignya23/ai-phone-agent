from phi.agent import Agent
from phi.model.groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def ai_phone_agent(customer_info, product_details):
    """
    AI phone agent to handle sales calls, provide information, address objections, and close deals.
    """

    # Create the Groq-based agent
    agent = Agent(
        name="SalesAgent",
        model=Groq(id="llama-3.3-70b-versatile"),  # Use the Groq model
        description=(
            "You are a quick, engaging, and professional sales agent. Be concise, relatable, and friendly. "
            "Use natural language with fillers like 'umm' for realism. Focus on capturing attention quickly, "
            "explaining the value, and closing deals efficiently. Keep sentences short and clear."
        ),
        add_history_to_messages=True,
        num_history_responses=5,  # Retain conversation context
    )

    # Example input to simulate a real customer call
    initial_prompt = (
        f"Customer Info: {customer_info}\n"
        f"Product Details: {product_details}\n"
        "Start the call by introducing yourself, explaining the purpose of the call, and engaging the customer."
    )

    # Generate response
    response = agent.run(initial_prompt)
    return response.content

# Example usage
if __name__ == "__main__":
    customer_info = "The customer is a small business owner in the retail industry, looking to improve online sales."
    product_details = "Our product is an AI-powered e-commerce tool that improves website conversion rates by 30%."

    print("AI Phone Agent Simulation:\n")
    response = ai_phone_agent(customer_info, product_details)
    print(response)
