# A sales agent qualifies the lead to ensure they are speaking with the decision-maker or a relevant stakeholder.
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.agents import tool, create_tool_calling_agent
from src.variables import company_name
import json

def knowledge_base(product_name: str):
    """Retrieve information related to a query."""

    # embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

    # vector_store = FAISS.load_local("vector_store/knowledge_base", embeddings,allow_dangerous_deserialization=True)

    # retirivals = vector_store.similarity_search(product_name, k=2)
    # content = "\n".join(doc.page_content for doc in retirivals)

    # return content
    return f"The {product_name} is available is our website, so visit website {company_name}.com for more details."


def payment_upi(amount):
    return f"Payment Upi id : {company_name}@okaxis for amount: {amount}" 

def payment_link(amount):
    return f"Payment Link : https://razorpay.com/100 for {amount}"

def schedule_call(date: str, time: str):
    return f"Call Scheduled... for {date} and {time}"

def get_tools_response(json_str):

    tool_name, tools_args = extract_tool_info(json_str)

    if tool_name == "knowledge_base":
        arg1 = tools_args[0]
        return knowledge_base(arg1)
    elif tool_name == "schedule_call":
        arg1 = tools_args[0]
        arg2 = tools_args[0]
        return schedule_call(arg1, arg2)
    elif tool_name == "payment_upi":
        arg1 = tools_args[0]
        return payment_upi(arg1)
    elif tool_name == "payment_link":
        arg1 = tools_args[0]
        return payment_link(arg1)
    else:
        return "Tool Not found!!!"
    

def extract_tool_info(json_str):


    data = json.loads(json_str)
        
    tools_ = data['tools_to_use'][0]['tool_name']
    arguments_array = list(data['tools_to_use'][0]['arguments'].values())
    print(tools_)
    print(arguments_array)

    return tools_, arguments_array

    

if __name__ == "__main__":
    json_str = '''
    {
    "tools_to_use": [
        {
        "tool_name": "knowledge_base",
        "arguments": {
            "product_name": "thermostat"
        }
        }
    ]
    }
    '''

    
    extract_tool_info(json_str)

    
