from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.tools import BaseTool
from langchain_core.messages import SystemMessage, HumanMessage
from models import get_llm, gemini_llm
from text_to_speech import text_to_speech
from prompts import SALES_AGENT_TOOLS_PROMPT, SALES_AGENT_INCEPTION_PROMPT_WITH_TOOLS
from variables import *

class CRMTool(BaseTool):
    name: str = "search_customer"
    description: str = "Search for customer information in the CRM system"
    
    def _run(self, query: str) -> str:
        # Simulate CRM lookup
        return f"Customer found: {query} - Premium tier, 2 years subscription"

class ProductCatalogTool(BaseTool):
    name: str = "search_products"
    description: str = "Search for product information and pricing"
    
    def _run(self, query: str) -> str:
        # Simulate product catalog lookup
        return f"Product found: {query} - $99/month, Enterprise features included"


def create_sales_agent():
    # Initialize the model
    llm = gemini_llm()
    
    # Define tools
    tools = [
        CRMTool(),
        ProductCatalogTool()
    ]
    
    prompt = PromptTemplate.from_template(SALES_AGENT_TOOLS_PROMPT)
    
    # Create the agent
    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )
    
    # Create the agent executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )
    
    return agent_executor

class SalesAgentManager:
    def __init__(self):
        self.agent = create_sales_agent()
        self.chat_history = []
    
    def process_message(self, message: str) -> str:
        """Process a customer message and return the agent's response"""
        response = self.agent.invoke({
            "salesperson_name" : salesperson_name,
            "salesperson_role" : salesperson_role,
            "company_name" : company_name,
            "company_business": company_business,
            "company_values" :company_values,
            "conversation_purpose": conversation_purpose,
            "conversation_type" : conversation_type,
            "input": message,
            "chat_history": self.chat_history
        })
        
        # Update chat history
        self.chat_history.extend([
            HumanMessage(content=message),
            SystemMessage(content=response["output"])
        ])
        
        return response["output"]
    

if __name__ == "__main__":
    sales_manager = SalesAgentManager()
    user_query = ""

    while True:
        user_query = input("User: ")
        response = sales_manager.process_message(user_query)
        print(response)
        text_to_speech(response)