from unittest import TestCase
from speech_handling.text_to_speech import TextToSpeech


class TextToSpeechTestCase(TestCase):
    def setUp(self):
        self.tts = TextToSpeech()

    def test_utter_voice_message_with_sapi(self):
        self.tts.runtime = 'sapi'
        self.assertEqual('TTS finished', self.tts.utter_voice_message('Hallo'))

    def test_utter_voice_message_with_google(self):
        self.tts.runtime = 'google'
        self.assertEqual('TTS finished', self.tts.utter_voice_message('Hallo'))

    def test_utter_voice_message_with_empty_message(self):
        self.assertEqual('TTS finished', self.tts.utter_voice_message(''))

    def test_utter_voice_message_without_speech_engine(self):
        self.tts.engine = ''
        self.assertEqual('TTS finished', self.tts.utter_voice_message(''))
