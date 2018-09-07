import pyttsx3
import os
from gtts import gTTS
import pyglet
import time

import logging


class TextToSpeech():
    def __init__(self):
        # TTS with pocketshpinx
        self.engine = pyttsx3.init('sapi5')  # use SAPI5 engine
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', rate - 30)  # words per minute
        self.engine.setProperty('volume', 0.9)

    def utter_voice_message(self, message):
        try:
            # Google Text-to-Speech API
            filename = 'temp_voice.mp3'
            tts = gTTS(text=message, lang='de')
            tts.save(filename)

            media = pyglet.media.load(filename, streaming=False)
            media.play()

            time.sleep(media.duration)
            os.remove(filename)

            # Pocketsphinx
            """
            self.engine.say(message)
            self.engine.runAndWait()
            """
        except:
            logging.error("Problem during TTS")


if __name__ == '__main__':
    TextToSpeech().utter_voice_message("Guten Tag, ich bin Carina")