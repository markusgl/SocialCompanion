from gtts import gTTS
import pyttsx3

engine = pyttsx3.init()
#voices = engine.getProperty('voices')
#engine.setProperty('voice', voices[0].id)

engine.say('Hallo, mein Name ist Socialbot und wie heißt du?')
engine.setProperty('rate', 50)  #120 words per minute
engine.setProperty('volume', 0.9)
engine.runAndWait()

# Windows output
import win32com.client as wincl
speak = wincl.Dispatch("SAPI.SpVoice")
speak.Speak("Hello World")