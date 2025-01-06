from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from prompts import SALES_AGENT_TOOLS_PROMPT
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from dotenv import load_dotenv

load_dotenv()




sales_agent_prompt = PromptTemplate(
   
    template="""
You are a sales agent named alex from techno.


Always be polite, keep responses concise, and adapt to the stage. 
Respond in one sentence and output "<END_OF_CALL>" when the call ends.


"""
)



llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0.0,
    max_retries=2,
    
)


chain = sales_agent_prompt | llm


response = chain.invoke("hello")

print(response)