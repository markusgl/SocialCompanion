from rasa_core.actions.action import Action
from rasa_core.events import SlotSet

from analytics_engine.analytics import AnalyticsEngine
from analytics_engine.relation_extractor import LANG


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
            bot_reply_message = 'Wie heißen sie?'

        dispatcher.utter_message(bot_reply_message)

        return [SlotSet('relativescount', relatives_count)]


class ActionExtractRelations(Action):
    def name(self):
        return 'action_extract_relations'

    def run(self, dispatcher, tracker, domain):
        utterance = tracker.latest_message()

        ae = AnalyticsEngine(lang=LANG.DE)
        result, response_mesage = ae.analyze_utterance(utterance, persist=True)

        if response_mesage:
            dispatcher.utter_message(response_mesage)
