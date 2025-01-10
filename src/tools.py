# A sales agent qualifies the lead to ensure they are speaking with the decision-maker or a relevant stakeholder.
from langchain.tools import Tool
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
import os
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.agents import tool, create_tool_calling_agent
from src.variables import company_name

def knowledge_base(query: str):
    """Retrieve information related to a query."""

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

    vector_store = FAISS.load_local("vector_store/knowledge_base", embeddings,allow_dangerous_deserialization=True)

    retirivals = vector_store.similarity_search(query, k=2)
    content = "\n".join(doc.page_content for doc in retirivals)
    return content

def generate_calendly_invitation_link(query):
    '''Generate a calendly invitation link based on the single query string'''
    event_type_uuid = os.getenv("CALENDLY_EVENT_UUID")
    api_key = os.getenv('CALENDLY_API_KEY')
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    url = 'https://api.calendly.com/scheduling_links'
    payload = {
    "max_event_count": 1,
    "owner": f"https://api.calendly.com/event_types/{event_type_uuid}",
    "owner_type": "EventType"
    }
    
    
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        data = response.json()
        return f"url: {data['resource']['booking_url']}"
    else:
        return "Failed to create Calendly link: "

def payment_upi():
    return f"Payment Upi id : {company_name}@okaxis" 

def payment_link(amount):

    return "Payment Link : https://razorpay.com/{100....}"


def execute_tools(response):

    if response == "No":
        return 
    else:
        pass
        
    

if __name__ == "__main__":
    print(combine_tools())
