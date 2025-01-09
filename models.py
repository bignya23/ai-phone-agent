from langchain_groq import ChatGroq
import os

# Initialize Groq LLM
def get_llm():
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0.7,
        api_key= os.getenv("GROQ_API_KEY"),
        max_tokens=512
    )

    return llm

