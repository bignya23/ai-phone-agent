from langchain_core.prompts import PromptTemplate
from src.prompts import SALES_AGENT_INCEPTION_PROMPT, STAGE_ANALYZER_INCEPTION_PROMPT
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from src.models import get_llm
from src.tools import combine_tools

def conversation_stage_chain(llm : ChatGroq):
    """To get the Conversation Stage"""
    prompt = PromptTemplate(
        template= STAGE_ANALYZER_INCEPTION_PROMPT,
        input_variables= [
            "conversation_history",
            "conversation_stage_id",
            "conversation_stages"
        ]
    )

    chain = prompt | llm | StrOutputParser()

    return chain

def conversation_tool_chain(llm : ChatGroq):

    """Get the response parser."""

    prompt = PromptTemplate(
        template= SALES_AGENT_INCEPTION_PROMPT,
        input_variables=[
            "salesperson_name",
            "salesperson_role",
            "company_name",
            "company_business",
            "company_values",
            "conversation_purpose",
            "conversation_type",
            "conversation_history",
            ],
    )

    return prompt
    # response = chain.invoke(input={"adjective" : "funny"})
    # return response

def conversation_chain(llm : ChatGroq):

    """Get the response parser."""

    # prompt1 = PromptTemplate(
    #     template="Tell me a {adjective} joke",
    #     input_variables=["adjective"]
    # )

    tools = combine_tools()

    prompt = PromptTemplate(
        template= SALES_AGENT_INCEPTION_PROMPT,
        input_variables=[
            "salesperson_name",
            "salesperson_role",
            "company_name",
            "company_business",
            "company_values",
            "conversation_purpose",
            "conversation_type",
            "conversation_history",
            ],
    )

    chain = prompt | llm.bind_tools(tools) | StrOutputParser()

    return chain
    # response = chain.invoke(input={"adjective" : "funny"})
    # return response



if __name__ == "__main__":
    print(conversation_chain(get_llm()))
    