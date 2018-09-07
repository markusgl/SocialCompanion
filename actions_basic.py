
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet, AllSlotsReset, Restarted, UserUttered
from speech_handling.text_to_speech import TextToSpeech


class ActionUtterGreet(Action):
    def name(self):
        return 'action_utter_greet'

    def run(self, dispatcher, tracker, domain):
        bot_reply_message = "Guten Tag, ich bin Carina. Ich kann für dich Termine finden oder dich über aktuelle " \
                            "Nachrichten informieren. Sag mir einfach was zu tun möchtest.\n" \
                            "Um uns besser kennen zu lernen würde ich gerne deinen Namen erfahren. Wie heißt du?"

        dispatcher.utter_message(bot_reply_message)
        TextToSpeech().utter_voice_message(bot_reply_message)


class ActionUtterGoodbye(Action):
    def name(self):
        return 'action_utter_goodbye'

    def run(self, dispatcher, tracker, domain):
        bot_reply_message = "Auf wiederhören. Hoffentlich sprechen wir bald wieder!"

        dispatcher.utter_message(bot_reply_message)
        TextToSpeech().utter_voice_message(bot_reply_message)


class ActionHowCanHelp(Action):
    def name(self):
        return 'utter_howcanhelp'

    def run(self, dispatcher, tracker, domain):
        bot_reply_message = "Wie kann ich dir helfen?"

        dispatcher.utter_message(bot_reply_message)
        TextToSpeech().utter_voice_message(bot_reply_message)

class ActionNotUnderstood(Action):
    def name(self):
        return 'utter_not_understood'

    def run(self, dispatcher, tracker, domain):
        bot_reply_message = "Ich habe dich leider nicht verstanden. Kannst du das wiederholen?"

        dispatcher.utter_message(bot_reply_message)
        TextToSpeech().utter_voice_message(bot_reply_message)