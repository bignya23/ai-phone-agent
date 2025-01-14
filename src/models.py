from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq LLM
def get_llm():
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0.9,
        api_key= os.getenv("GROQ_API_KEY"),
        max_tokens=512
    )

    return llm


def gemini_llm():

    os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.7,
        max_tokens=512,
        max_retries=2,
    )

    return llm
