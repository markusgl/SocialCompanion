from gtts import gTTS
import pyttsx3

engine = pyttsx3.init('sapi5') # use SAPI5 engine
#voices = engine.getProperty('voices')
#engine.setProperty('voice', voices[0].id)
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-25)  #words per minute
engine.setProperty('volume', 0.9)

engine.say('LeBron James kommt nach Berlin. - Mittelbayerische')
engine.runAndWait()

# Windows output
#import win32com.client as wincl
#speak = wincl.Dispatch("SAPI.SpVoice")
#speak.Speak("Hello World")