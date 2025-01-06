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




# # Create a simple prompt
# prompt = ChatPromptTemplate.from_messages([
#     ("system", SALES_PROMPT),
#     ("user", "{input}")
# ])

# Create the chain that guarantees JSON output
# chain = prompt | llm

# def parse_product(description: str) -> dict:
#     result = chain.invoke({"input": description})
#     print(result.content)
#     return result.content

        
# Example usage
# while True:
#     description = input("User : ")
#     content = parse_product(description)
#     end = time.time()
#     print(end - start)

#     text_to_speech.text_to_speech(content)
