from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.tools import BaseTool
from typing import List, Any
from langchain_core.messages import SystemMessage, HumanMessage
from models import get_llm
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
    llm = get_llm()
    
    # Define tools
    tools = [
        CRMTool(),
        ProductCatalogTool()
    ]
    
    # Create the agent prompt template
    prompt_template = """You are an experienced sales agent. Your goal is to help customers find the right products and provide accurate information.

    You have access to the following tools:
    {tools}

    Available tools: {tool_names}

    Follow these steps for each interaction:
    1. Understand the customer's needs
    2. Use appropriate tools to gather information
    3. Provide personalized recommendations
    4. Answer any questions clearly

    Remember to:
    - Be professional and courteous
    - Focus on value proposition
    - Handle objections effectively
    - Document all interactions

    Use the following format:
    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of {tool_names}
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question
    
    Previous conversation:
    {chat_history}
    
    Question: {input}
    
    {agent_scratchpad}"""
    
    prompt = PromptTemplate.from_template(prompt_template)
    
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
            "input": message,
            "chat_history": self.chat_history
        })
        
        # Update chat history
        self.chat_history.extend([
            HumanMessage(content=message),
            SystemMessage(content=response["output"])
        ])
        
        return response["output"]

# Example usage
if __name__ == "__main__":
    sales_manager = SalesAgentManager()
    
    # Example conversation
    responses = [
        sales_manager.process_message("I'm interested in your enterprise solution"),
        sales_manager.process_message("What's the pricing for 100 users?"),
        sales_manager.process_message("Can you check my current subscription status?")
    ]
    
    for i, response in enumerate(responses, 1):
        print(f"\nInteraction {i}:")
        print(response)