from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from speech_handling.text_to_speech import TextToSpeech


class ActionAskTime(Action):
    def name(self):
        return 'utter_ask_time'

    def run(self, dispatcher, tracker, domain):
        bot_reply_message = "An welchem Tag oder zu welcher Uhrzeit?"

        dispatcher.utter_message(bot_reply_message)
        TextToSpeech().utter_voice_message(bot_reply_message)


class ActionAskSubject(Action):
    def name(self):
        return 'utter_ask_subject'

    def run(self, dispatcher, tracker, domain):
        bot_reply_message = "Wie lautet der Betreff?"

        dispatcher.utter_message(bot_reply_message)
        TextToSpeech().utter_voice_message(bot_reply_message)


class ActionAskLocation(Action):
    def name(self):
        return 'utter_ask_location'

    def run(self, dispatcher, tracker, domain):
        bot_reply_message = "An welchem Ort?"

        dispatcher.utter_message(bot_reply_message)
        TextToSpeech().utter_voice_message(bot_reply_message)
