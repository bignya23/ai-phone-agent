from phi.agent import Agent
from phi.model.groq import Groq
from src.speech_to_text import speech_to_text
from dotenv import load_dotenv
import time

load_dotenv()
def Ai_Agent(question="What is the weather report in india today"):
    agent = Agent(
        name="Agent",
        model=Groq(id="llama-3.3-70b-versatile"),
        description=
                    "Your goal is to provide a professional, empathetic, and natural conversation "
                    "to build trust and close deals."
                    " Provide responses in plain text without any formatting. Give human like responces with words like "
                     "umm, ahh etc"
                    "Give all answers in one line and as short as possible.",
        add_history_to_messages=True,
        num_history_responses=10
    )

    response = agent.run(question)
    return response.content



if __name__ == "__main__":
    start = time.time()
    print(Ai_Agent())
    end = time.time()
    print(end - start)




# start = time.time()
#
# from groq import Groq
#
# client = Groq()
#
#
# def ai_agent(question):
#     chat_completion = client.chat.completions.create(
#         #
#         # Required parameters
#         #
#         messages=[
#             # Set an optional system message. This sets the behavior of the
#             # assistant and can be used to provide specific instructions for
#             # how it should behave throughout the conversation.
#             {
#                 "role": "system",
#                 "content": "Give all answers in one line and as short as possible. Your goal is to provide a professional, empathetic, and natural conversation to build trust and close deals. Provide responses in plain text without any formatting."
#             },
#             # Set a user message for the assistant to respond to.
#             {
#                 "role": "user",
#                 "content": question,
#             }
#         ],
#
#         # The language model which will generate the completion.
#         model="mixtral-8x7b-32768",
#
#     )
#
#     return chat_completion.choices[0].message.content
#
# # print(ai_agent(question="schedule an appoiintment with doctor"))
#
# end = time.time()
# print(end - start)
