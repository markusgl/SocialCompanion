# TTS with pocketshpinx
import pyttsx3

engine = pyttsx3.init('sapi5') # use SAPI5 engine
#voices = engine.getProperty('voices')
#engine.setProperty('voice', voices[0].id)
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-30)  #words per minute
engine.setProperty('volume', 0.9)

engine.say('LeBron James kommt nach Berlin. - Mittelbayerische')
engine.runAndWait()

# TTS with google TTS

from gtts import gTTS
# Windows output
#import win32com.client as wincl
#speak = wincl.Dispatch("SAPI.SpVoice")
#speak.Speak("LeBron James kommt nach Berlin. - Mittelbayerische'")

#from gtts import gTTS
#tts = gTTS('LeBron James kommt nach Berlin. - Mittelbayerische', lang='de')

#tts.save('hello.mp3')
