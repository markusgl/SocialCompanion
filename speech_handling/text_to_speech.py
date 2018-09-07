import pyttsx3


class TextToSpeech():
    def __init__(self):
        # TTS with pocketshpinx
        self.engine = pyttsx3.init('sapi5')  # use SAPI5 engine
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', rate - 30)  # words per minute
        self.engine.setProperty('volume', 0.9)

    def out_text_message(self, message):
        self.engine.say(message)
        self.engine.runAndWait()


if __name__ == '__main__':
    TextToSpeech().out_text_message('Hallo ich bin SocialBot und wie heißt du?')