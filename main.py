import speech_to_text
import aiagent
import text_to_speech
import time
while True:
    try:
        start = time.time()
        question = speech_to_text.speech_to_text()
        # print("Question : ")
        # question = input()
        response = aiagent.ai_agent(question)
        text_to_speech.text_to_speech(response)
        end = time.time()
        print(end - start)

    except KeyboardInterrupt:
        print("Stopping...")
        break