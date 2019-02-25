"""
Basic actions for greeting, goodbye, accept and decline
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import datetime
import logging

from random import randint
from rasa_core.actions.action import Action
from rasa_core.events import ReminderScheduled
from speech_handling.text_to_speech import TextToSpeech

tts = False  # toggle speech output (text to speech)

class ActionWelcomeMessage(Action):
    def name(self):
        return 'action_welcome_message'

    def run(self, dispatcher, tracker, domain):


        bot_reply_message = "Guten Tag, mein Name ist Carina. " \
                            "Ich kann aktuelle Nachrichten vorlesen " \
                            "oder einfach eine nette Unterhaltung führen. " \
                            "Was möchten Sie tun?"
        buttons = [{"title": 'Informationen abrufen', "payload": "/getinformation"},
                   {"title": 'Eine Unterhaltung beginnen', "payload": "/chatting"}]
        dispatcher.utter_button_message(text=bot_reply_message, buttons=buttons)
        if tts:
            TextToSpeech().utter_voice_message(bot_reply_message)

        trigger_date = None
        if trigger_date:
            return [ReminderScheduled('action_remind_drink', trigger_date, kill_on_user_message=True)]

        return []

    @staticmethod
    def schedule_reminder():
        trigger_date = datetime.datetime.now() + datetime.timedelta(seconds=10)
        trigger_date = trigger_date.isoformat()
        logging.info("Reminderdate {}".format(trigger_date))

        return trigger_date


class ActionUtterGreet(Action):
    def name(self):
        return 'action_utter_greet'

    def run(self, dispatcher, tracker, domain):
        bot_reply_messages = ["Guten Tag!", 'Hallo', 'Hi', "Wie geht's"]
        index = randint(0, len(bot_reply_messages))
        bot_reply_message = bot_reply_messages[index]

        dispatcher.utter_message(bot_reply_message)
        if tts:
            TextToSpeech().utter_voice_message(bot_reply_message)

        return []


class ActionUtterGoodbye(Action):
    def name(self):
        return 'action_utter_goodbye'

    def run(self, dispatcher, tracker, domain):
        bot_reply_message = "Auf Wiedersehen. Hoffentlich sprechen wir bald wieder!"

        dispatcher.utter_message(bot_reply_message)
        if tts:
            TextToSpeech().utter_voice_message(bot_reply_message)

        return []


class ActionHowCanHelp(Action):
    def name(self):
        return 'utter_howcanhelp'

    def run(self, dispatcher, tracker, domain):
        bot_reply_message = "Was möchtest du gerne wissen?"

        dispatcher.utter_message(bot_reply_message)
        if tts:
            TextToSpeech().utter_voice_message(bot_reply_message)

        return []


class ActionRemindToDrink(Action):
    def name(self):
        return 'action_remind_drink'

    def run(self, dispatcher, tracker, domain):
        bot_reply_message = "Möchten Sie vielleicht etwas Wasser trinken?"

        dispatcher.utter_message(bot_reply_message)
        if tts:
            TextToSpeech().utter_voice_message(bot_reply_message)

        return []


class ActionNotUnderstood(Action):
    def name(self):
        return 'action_not_understood'

    def run(self, dispatcher, tracker, domain):
        latest_message = tracker.latest_message
        user_utterance = latest_message.text

        confidence_score = latest_message.intent['confidence']
        intent_name = latest_message.intent['name']
        logging.debug("latest intent {}, confidence {}".format(intent_name, confidence_score))

        if confidence_score > 0.35:
            bot_reply_message = "Ich glaube Sie wollten "
            if intent_name == 'introduce':
                bot_reply_message += 'sich vorstellen. Ist das korrekt?'
            elif intent_name == 'greet':
                bot_reply_message += 'mich begrüßen. Ist das korrekt?'
            elif intent_name == 'goodbye':
                bot_reply_message += 'sich verabschieden. Ist das korrekt?'
            elif intent_name == 'find_appointment':
                bot_reply_message += 'einen Termin finden. Ist das korrekt?'
            elif intent_name == 'make_appointment':
                bot_reply_message += 'einen Termin erstellen. Ist das korrekt?'
            elif intent_name == 'inform':
                bot_reply_message += 'mir Informationen mitteilen. Ist das korrekt?'
            else:
                bot_reply_message = "Ich habe Sie leider nicht verstanden. Was möchten Sie tun?"
        else:
            # Try to get further information out of the utterance
            logging.debug("No intent recognized.")

            bot_reply_message = "Ich habe Sie leider nicht verstanden. Was möchten Sie tun?"

        dispatcher.utter_message(bot_reply_message)
        if tts:
            TextToSpeech().utter_voice_message(bot_reply_message)

        return []
