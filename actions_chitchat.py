from random import randint
from rasa_core.actions.action import Action
from rasa_core.events import SlotSet

from analytics_engine.analytics import AnalyticsEngine
from analytics_engine.relation_extractor import LANG


class ActionGetToKnow(Action):
    def name(self):
        return 'action_gettoknow'

    def run(self, dispatcher, tracker, domain):
        bot_reply_message = "Wie wäre es wenn wir uns zuerst besser kennen lernen? " \
                            "Wie ist dein Name?"

        dispatcher.utter_message(bot_reply_message)


class ActionAskAge(Action):
    def name(self):
        return 'action_ask_age'

    def run(self, dispatcher, tracker, domain):
        bot_reply_message = 'Wie alt bist Du?'

        dispatcher.utter_message(bot_reply_message)


class ActionAskName(Action):
    def name(self):
        return 'action_ask_name'

    def run(self, dispatcher, tracker, domain):
        bot_reply_messages = ['Wie heißen sie?', 'Wie ist sein Name?']

        index = randint(0, len(bot_reply_messages))
        bot_reply_message = bot_reply_messages[index]
        dispatcher.utter_message(bot_reply_message)


class ActionAskRelatives(Action):
    def name(self):
        return 'action_ask_relatives'

    def run(self, dispatcher, tracker, domain):
        bot_reply_messages = ['Erzähl mir was von deinen Angehörigen. Hast du Geschwister oder Kinder?',
                              'Ich würde gerne mehr über dich Erfahren. Hast du Angehörige? ']

        index = randint(0, len(bot_reply_messages))
        dispatcher.utter_message(bot_reply_messages[index])


relatives_count = {'einen': 1, 'eine': 1, 'keine': 0, 'viele': 10, 'mehrere': 10, 'zwei': 2, 'drei': 3, 'vier': 4,
                   'fünf': 5, 'sechs': 6, 'sieben': 7, 'acht': 8, 'neun': 9, 'zehn': 10}


class ActionAskRelativesNames(Action):
    def name(self):
        return 'action_ask_relatives_names'

    def run(self, dispatcher, tracker, domain):
        relatives_count = tracker.get_slot('relativescount')

        if relatives_count < 2:
            bot_reply_message = 'Wie heißt er oder sie?'
        elif relatives_count < 1:
            bot_reply_message = 'Wer steht dir sonst nahe?'
        else:
            bot_reply_messages = ['Wie heißen sie?',
                                  'Wie ist deren Name?']
            index = randint(0, len(bot_reply_messages))
            bot_reply_message = bot_reply_messages[index]

        dispatcher.utter_message(bot_reply_message)

        return [SlotSet('relativescount', relatives_count)]


class ActionAskAmount(Action):
    def name(self):
        return 'action_ask_amount'

    def run(self, dispatcher, tracker, domain):
        bot_reply_messages = ['Wie viele?']

        index = randint(0, len(bot_reply_messages))
        dispatcher.utter_message(bot_reply_messages[index])


class ActionExtractRelations(Action):
    def name(self):
        return 'action_extract_relations'

    def run(self, dispatcher, tracker, domain):
        utterance = tracker.latest_message()

        ae = AnalyticsEngine(lang=LANG.DE)
        ae.analyze_utterance(utterance, persist=True)
