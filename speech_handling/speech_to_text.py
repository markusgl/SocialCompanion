import speech_recognition as sr
import requests
import json
import logging

logger = logging.getLogger(__name__)


class SpeechHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def send_message_to_voice_channel(self, message):
        url = "http://827f042a.ngrok.io/app/message"
        data = {"sender": "testsender", "message": message}
        data_json = json.dumps(data)
        headers = {'Content-Type': 'application/json'}

        requests.post(
                url=url,
                data=data_json,
                headers=headers
        )

    def speech_to_text(self):
        #while True:
        with sr.Microphone() as source:
            print('Sag etwas:')
            audio = self.recognizer.listen(source)
            self.recognizer.adjust_for_ambient_noise(source, duration=3)  # adapt to the noise
            message = None
            try:
                message = self.recognizer.recognize_google(audio, language="de_DE")
                #self.send_message_to_voice_channel(message)
                #message = self.recognizer.recognize_bing(audio, key=BING_KEY, language="de-DE")
                #message = self.recognizer.recognize_sphinx(audio, language="de-DE"))
                print("You said: " + message)
            except sr.UnknownValueError:
                logger.warning("Could not understand audio")
            except sr.RequestError as e:
                logger.error(f"Error: {e}")


if __name__ == '__main__':
    handler = SpeechHandler()
    handler.speech_to_text()
