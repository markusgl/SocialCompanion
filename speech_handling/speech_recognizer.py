import speech_recognition as sr


class SpeechHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def speech_to_text(self):
        with sr.Microphone() as source:
            print('start listening')
            audio = self.recognizer.listen(source)
            self.recognizer.adjust_for_ambient_noise(source, duration=5)  # adapt to the noise
            message = None
            try:
                message = self.recognizer.recognize_sphinx(audio, language="de-DE")
                print("Sphinx thinks you said " + self.recognizer.recognize_sphinx(audio, language="de-DE"))
            except sr.UnknownValueError:
                print("Sphinx could not understand audio")
            except sr.RequestError as e:
                print("Sphinx error; {0}".format(e))

        return message

if __name__ == '__main__':
    hanler = SpeechHandler()
    hanler.speech_to_text()