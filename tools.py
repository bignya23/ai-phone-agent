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

@tool
def get_knowledge_base(query: str):
    """Retrieve information related to a query."""

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

    vector_store = FAISS.load_local("vector_store/knowledge_base", embeddings,allow_dangerous_deserialization=True)

    retirivals = vector_store.similarity_search(query, k=2)
    content = "\n".join(doc.page_content for doc in retirivals)
    return content

def generate_calendly_invitation_link(query):
    '''Generate a calendly invitation link based on the single query string'''
    pass


def combine_tools():
    
    tools = [get_knowledge_base]


    return tools



if __name__ == "__main__":
    print(combine_tools())
    print(get_knowledge_base("matresses options"))