import requests
import json
import threading
import speech_recognition as sr
import logging

from flask import Flask, request
from speech_handling.text_to_speech import SapiTTS, GoogleTTS

logger = logging.getLogger(__name__)
app = Flask(__name__)

tts = GoogleTTS()
recognizer = sr.Recognizer()


def send_message_to_voice_channel(message):
    # encoded_query = quote(query)
    #print(f'sending message {message}')
    url = "http://56b7de37.ngrok.io/app/message"

    data = {"sender": "user", "message": message}
    data_json = json.dumps(data)
    headers = {'Content-Type': 'application/json'}

    requests.post(
        url=url,
        data=data_json,
        headers=headers
    )


def speech_to_text():
    with sr.Microphone() as source:
        print('Listening...')
        # increase threshold if stt tries to recognize for too long
        recognizer.energy_threshold = 1000
        audio = recognizer.listen(source)
        recognizer.adjust_for_ambient_noise(source)
        try:
            message = recognizer.recognize_google(audio, language="de_DE")
            print(f'Deine Eingabe: {message}')
            send_message_to_voice_channel(message)
        except sr.UnknownValueError:
            tts.utter_voice_message("Ich habe dich leider nicht verstanden")
            logger.warning("Could not understand audio")
        except sr.RequestError as e:
            logger.error(f"Error: {e}")


def command_line_input():
    message = input("User: ")
    send_message_to_voice_channel(message)


@app.route("/", methods=['POST'])
def receive_bot_response():
    payload = request.json
    message = payload.get("message", None)
    print(f'Bot: {message}')

    return "success", 200


thread = threading.Thread(target=app.run)
thread.start()
send_message_to_voice_channel('/start')

while True:
    speech_to_text()
