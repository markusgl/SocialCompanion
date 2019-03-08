import pyttsx3
import pyglet
import time
import logging
import os

from gtts import gTTS

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class GoogleTTS:
    def utter_voice_message(self, message):
        try:
            # Google Text-to-Speech API - needs internet connectivity
            #filename = ROOT_DIR + '\\temp_voice.mp3'
            filename = 'temp_voice.mp3'
            tts = gTTS(text=message, lang='de', slow=False)
            tts.save(filename)

            media = pyglet.media.load(filename, streaming=True)
            media.play()
            time.sleep(media.duration)
            #os.remove(filename)

            return 'TTS finished'
        except Exception as err:
            logging.error("Error during TTS {}".format(err))
            return None

    def check_google_connection(self):
        try:
            message = "Hallo"
            filename = 'temp_voice.mp3'
            tts = gTTS(text=message, lang='de')
            tts.save(filename)
            os.remove(filename)
            return True
        except Exception as err:
            logging.error("Error during Google TTS testing {}".format(err))
            return False


class SapiTTS:
    def __init__(self):
        # Sapi Microsoft speech engine - works offline
        self.engine = pyttsx3.init('sapi5')  # use SAPI5 engine
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', rate - 20)  # words per minute
        self.engine.setProperty('volume', 0.9)

    def utter_voice_message(self, message):
        try:
            self.engine.say(message)
            self.engine.runAndWait()

            return 'TTS finished'
        except Exception as err:
            logging.error("Error during TTS {}".format(err))
            return None


if __name__ == '__main__':
    gtts = GoogleTTS()
    gtts.utter_voice_message('Guten Tag, mein Name ist Carina')

