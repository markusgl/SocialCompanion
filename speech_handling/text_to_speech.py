import pyttsx3
import os
from gtts import gTTS
import pyglet
import time
import logging
import json



class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init('sapi5')  # use SAPI5 engine
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', rate - 30)  # words per minute
        self.engine.setProperty('volume', 0.9)
        # 'pocketsphinx' or 'google'
        self.runtime = "pocketsphinx"


    def utter_voice_message(self, message):
        try:
            if self.runtime == "google":
                # Google Text-to-Speech API - needs internet connectivity
                filename = 'temp_voice.mp3'
                tts = gTTS(text=message, lang='de')
                tts.save(filename)

                media = pyglet.media.load(filename, streaming=False)
                media.play()

                time.sleep(media.duration)
                os.remove(filename)

            # Pocketsphinx - works offline
            elif self.runtime == "pocketsphinx":
                self.engine.say(message)
                self.engine.runAndWait()

            # No speech output

        except:
            logging.error("Problem during TTS")


if __name__ == '__main__':
    TextToSpeech().utter_voice_message("Guten Tag, ich bin Carina")