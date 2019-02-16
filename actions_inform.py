"""
These actions are used to ask the user for missing information
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from speech_handling.text_to_speech import TextToSpeech
from analytics_engine.analytics import AnalyticsEngine

tts = False  # toggle speech output (text to speech)


class ActionAskTime(Action):
    def name(self):
        return 'utter_ask_time'

    def run(self, dispatcher, tracker, domain):
        bot_reply_message = "An welchem Tag oder zu welcher Uhrzeit?"
        AnalyticsEngine().analyze_utterance(tracker.latest_message.text)

        dispatcher.utter_message(bot_reply_message)
        if tts:
            TextToSpeech().utter_voice_message(bot_reply_message)

        return []


class ActionAskSubject(Action):
    def name(self):
        return 'utter_ask_subject'

    def run(self, dispatcher, tracker, domain):
        bot_reply_message = "Wie lautet der Betreff?"
        AnalyticsEngine().analyze_utterance(tracker.latest_message.text)

        dispatcher.utter_message(bot_reply_message)
        if tts:
            TextToSpeech().utter_voice_message(bot_reply_message)

        return []


class ActionAskLocation(Action):
    def name(self):
        return 'utter_ask_location'

    def run(self, dispatcher, tracker, domain):
        bot_reply_message = "An welchem Ort?"
        AnalyticsEngine().analyze_utterance(tracker.latest_message.text)

        dispatcher.utter_message(bot_reply_message)
        if tts:
            TextToSpeech().utter_voice_message(bot_reply_message)

        return []