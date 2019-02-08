
from rasa_core.actions.action import Action
from speech_handling.text_to_speech import TextToSpeech
from analytics_engine.analytics import AnalyticsEngine, LANG
from random import randint


class ActionGetToKnow(Action):
    def name(self):
        return 'action_gettoknow'

    def run(self, dispatcher, tracker, domain):
        bot_reply_message = "Wie wäre es wenn wir uns zuerst besser kennen lernen? " \
                            "Wie ist dein Name?"

        dispatcher.utter_message(bot_reply_message)
        #TextToSpeech().utter_voice_message(bot_reply_message)


class ActionAskAge(Action):
    def name(self):
        return 'action_ask_age'

    def run(self, dispatcher, tracker, domain):
        bot_reply_message = 'Wie alt bist Du?'

        dispatcher.utter_message(bot_reply_message)
        #TextToSpeech().utter_voice_message(bot_reply_message)


class ActionAskName(Action):
    def name(self):
        return 'action_ask_name'

    def run(self, dispatcher, tracker, domain):
        bot_reply_messages = ['Wie heißen sie?', 'Wie ist sein Name?']

        index = randint(0, len(bot_reply_messages))
        bot_reply_message = bot_reply_messages[index]
        dispatcher.utter_message(bot_reply_message)
        #TextToSpeech().utter_voice_message(bot_reply_message)


class ActionAskRelatives(Action):
    def name(self):
        return 'action_ask_relatives'

    def run(self, dispatcher, tracker, domain):
        bot_reply_messages = ['Erzähl mir was von deinen Angehörigen. Hast du Geschwister oder Kinder?',
                              'Ich würde gerne mehr über dich Erfahren. Hast du Angehörige? ']

        index = randint(0, len(bot_reply_messages))
        dispatcher.utter_message(bot_reply_messages[index])


class ActionExtractRelations(Action):
    def name(self):
        return 'action_extract_relations'

    def run(self, dispatcher, tracker, domain):
        utterance = tracker.latest_message()

        ae = AnalyticsEngine(lang=LANG.DE)
        ae.analyze_utterance(utterance)
