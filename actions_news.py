import re

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet

from news_searcher import NewsSearcher


class ActionOfferFeatures(Action):
    def name(self):
        return 'action_offer_features'

    def run(self, dispatcher, tracker, domain):
        buttons = [{"title": '5 aktuelle Schlagzeilen', "payload": "/read_news"},
                   {"title": 'Bestimmtes Thema', "payload": "/ask_topic"}]
        bot_reply_message = "Wollen Sie die fünf aktuellen Schlagzeilen hören oder ein bestimmtes Thema suchen?"

        dispatcher.utter_button_message(text=bot_reply_message, buttons=buttons)


class ActionAskTopic(Action):
    def name(self):
        return 'action_ask_topic'

    def run(self, dispatcher, tracker, domain):
        bot_reply_message = "Zu welchem Thema möchte Sie Nachrichten hören?"

        dispatcher.utter_message(bot_reply_message)


class ActionReadNews(Action):
    def name(self):
        return 'action_read_news'

    def run(self, dispatcher, tracker, domain):
        bot_reply_message = 'Hier sind die fünf aktuellen Schlagzeilen: \n'
        ns = NewsSearcher()

        if tracker.get_slot('news_type'):
            topic = tracker.get_slot('news_type')
            topic = re.sub('nachrichten$', '', topic)
            bot_reply_message += 'zum Thema' + topic

            news_titles, news_urls = ns.search_news(topic)
        else:
            news_titles, news_urls = ns.search_news()

        bot_reply_message += news_titles
        dispatcher.utter_message(bot_reply_message)

        return [SlotSet('news', '')]
