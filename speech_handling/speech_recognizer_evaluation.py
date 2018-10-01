import pyaudio
import speech_recognition as sr
import wave

"""
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "file.wav"

audio = pyaudio.PyAudio()

# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
print("recording...")
frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    validation_set = stream.read(CHUNK)
    frames.append(validation_set)
print("finished recording")

# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()   


# Write audio to wav-file
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()
"""

# print available input devices
p = pyaudio.PyAudio()
for i in range(p.get_device_count()): #list all available audio devices
  dev = p.get_device_info_by_index(i)
  print((i, dev['name'], dev['maxInputChannels']))

# choose an input device from the list
input_device_number = 2

recognizer = sr.Recognizer()
with sr.Microphone(input_device_number) as source:
    # listen for 1 second and create the ambient noise energy level
    recognizer.adjust_for_ambient_noise(source, duration=1)
    #recognizer.energy_threshold = 500
    print("Sag etwas!")
    audio = recognizer.listen(source, phrase_time_limit=5)

"""
# recognize speech using Sphinx
try:
    print("Sphinx STT: " + recognizer.recognize_sphinx(audio, language="de-DE"))
except sr.UnknownValueError:
    print("Sphinx could not understand audio")
except sr.RequestError as e:
    print("Sphinx error; {0}".format(e))


# google speech recognition
try:
    print("Google Speech Recognition: " + recognizer.recognize_google(audio, language="de-DE"))
except sr.UnknownValueError:
    print("Konnte dich nicht verstehen")
except sr.RequestError as e:
    print("Konnte die Abfrage nicht senden; {0}".format(e))

"""

# recognize speech using Microsoft Bing Voice Recognition
BING_KEY = "307d014082ce4bb9aa83b240ee0ffe62"  # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
try:
    print("Microsoft Bing recognized: " + recognizer.recognize_bing(audio, key=BING_KEY, language="de-DE"))
except sr.UnknownValueError:
    print("Microsoft Bing Voice Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))


