import pyttsx3
from gtts import gTTS
import pyglet
import time
import logging


class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init('sapi5')  # use SAPI5 engine
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', rate - 30)  # words per minute
        self.engine.setProperty('volume', 0.9)
        # 'sapi' or 'google'
        self.runtime = "sapi"

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
                #os.remove(filename)

            # Sapi Microsoft speech engine - works offline
            elif self.runtime == "sapi":
                self.engine.say(message)
                self.engine.runAndWait()
                print('TTS finished')
            # No speech output

        except:
            logging.error("Problem during TTS")

