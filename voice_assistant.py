import json
import ibm_watson
import pyttsx
import speech_recognition as sr
import winsound
import os


def save_feedback(feedback):
    try:
        file = open('C:\\Users\\lgunupudi\\feedback.txt', "a")
        file.write(feedback+"\n")
    except IOError:
        print("Unable to append file: ")
    else:
        file.close()


def take_feedback():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please provide feedback!!!")
        engine = pyttsx.init()
        engine.say("Please provide feedback")
        engine.runAndWait()
        audio = r.listen(source)
    try:
        user_input_feedback = str(r.recognize_google(audio))
        print(user_input_feedback)
        save_feedback(user_input_feedback)
    except Exception:
        print("Feedback not provided")


def beep():
    frequency = 200  # Set Frequency To 2500 Hertz
    duration = 250
    winsound.Beep(frequency, duration)


def execute_command(user_input, session_id):
    service = ibm_watson.AssistantV2(
        iam_apikey='Lxa1VrZzTwE9xnMrMFJUaE1Q74txlo8tj1oFLlvaTy61',
        version='2019-02-28',
        url='https://gateway-lon.watsonplatform.net/assistant/api'
    )
    assistant_response_command = service.message(
        assistant_id='cc6ddadf-b029-47ac-956a-8ccfdf354996',
        session_id=session_id,
        input={
            'message_type': 'text',
            'text': user_input
        }
    ).get_result()

    print(json.dumps(assistant_response_command, indent=2))
    speak = assistant_response_command['output']['generic'][0]['text']
    engine = pyttsx.init()
    engine.say(speak)
    engine.runAndWait()


def get_emotion_meter():
    score = os.environ["Emotion"]
    final_score = "F5 is likely " + score
    engine = pyttsx.init()
    engine.say(final_score)
    engine.runAndWait()


def call_josh():
    service = ibm_watson.AssistantV2(
        iam_apikey='Lxa1VrZzTwE9xnMrMFJUaE1Q74txlo8tj1oFLlvaTy61',
        version='2019-02-28',
        url='https://gateway-lon.watsonplatform.net/assistant/api'
        )

    session_response = service.create_session(
        assistant_id='cc6ddadf-b029-47ac-956a-8ccfdf354996'
    ).get_result()

    session_id = str(session_response['session_id'])

    assistant_response = service.message(
        assistant_id='cc6ddadf-b029-47ac-956a-8ccfdf354996',
        session_id=session_id,
        input={
            'message_type': 'text',
            'text': 'Hello'
        }
    ).get_result()
    print(json.dumps(assistant_response, indent=2))
    r = sr.Recognizer()
    engine = pyttsx.init()
    engine.say("How can i help you")
    engine.runAndWait()
    with sr.Microphone() as source:
        print("Please give some input!!!")
        audio = r.listen(source)
    try:
        user_input = str(r.recognize_google(audio))
        print(user_input)
        if user_input.find('feedback') >= 0:
            take_feedback()
        elif user_input.find('emotion') >= 0:
            get_emotion_meter()
        else:
            execute_command(user_input, session_id)

    except Exception:
        print("Did not receive input")


while True:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say Mike!!!")
        beep()
        audio = r.listen(source)
    try:
        user_input_josh = str(r.recognize_google(audio))
        print(user_input_josh)
        if user_input_josh.find("Mike") >= 0:
            call_josh()
    except Exception:
        print("Mike is not called")
