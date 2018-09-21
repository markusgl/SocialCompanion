# TTS with microsof speech engine
import pyttsx3


engine = pyttsx3.init('sapi5') # use SAPI5 engine
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
print(voices)
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-30)  #words per minute
engine.setProperty('volume', 0.9)

engine.say('Ich habe dich leider nicht verstanden. Kannst du das wiederholen?')
engine.runAndWait()

"""

# TTS with google TTS
from gtts import gTTS
# Windows output
#import win32com.client as wincl
#speak = wincl.Dispatch("SAPI.SpVoice")
#speak.Speak("LeBron James kommt nach Berlin. - Mittelbayerische'")

import os
from gtts import gTTS
import pyglet
import time
from io import BytesIO

bot_reply_message = "Guten Tag, ich bin Carina. Ich kann für dich Termine finden oder dich über aktuelle " \
                            "Nachrichten informieren. Sag mir einfach was zu tun möchtest.\n" \
                            "Um uns besser kennen zu lernen würde ich gerne deinen Namen erfahren. Wie heißt du?"

filename = 'temp_voice.mp3'
tts = gTTS(bot_reply_message, lang='de')
tts.save(filename)

media = pyglet.media.load(filename, streaming=False)
media.play()
time.sleep(media.duration)
os.remove(filename)
"""