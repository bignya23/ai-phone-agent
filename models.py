from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import time
import text_to_speech
start = time.time()

# Initialize Groq LLM
def get_llm():
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0.7,
        api_key="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",
        max_tokens=512
    )

    return llm

