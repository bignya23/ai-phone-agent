import src.speech_to_text as speech_to_text
# import test.aiagent as aiagent
import src.text_to_speech as text_to_speech
import time
while True:
    try:
        question = speech_to_text.speech_to_text()
        # print("Question : ")
        # question = input()
        # response = aiagent.Ai_Agent(question)

        # text_to_speech.text_to_speech(response)
        end1 = time.time()
        # print(end1 - end)

    except KeyboardInterrupt:
        print("Stopping...")
        break