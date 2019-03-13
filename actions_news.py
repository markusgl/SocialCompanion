import re

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet

from news_searcher import NewsSearcher


class ActionOfferFeatures(Action):
    def name(self):
        return 'action_offer_features'

    def run(self, dispatcher, tracker, domain):
        buttons = [{"title": 'Aktuelle Schlagzeilen', "payload": "/read_news"},
                   {"title": 'Termine verwalten', "payload": "/cal_mgmt"}]
        bot_reply_message = "Ich kann dir aktuelle Nachrichten zeigen oder deine Termine verwalten. Was möchtest du tun?"

        dispatcher.utter_button_message(text=bot_reply_message, buttons=buttons)


class ActionReadNews(Action):
    def name(self):
        return 'action_read_news'

    def run(self, dispatcher, tracker, domain):

        ns = NewsSearcher()

        if tracker.get_slot('news_type'):
            topic = tracker.get_slot('news_type')
            topic = re.sub('nachrichten$', '', topic)
            bot_reply_message = 'Hier sind die fünf aktuellen Schlagzeilen zum Thema ' + topic.title() + ':\n'

            news_titles, news_urls = ns.search_news(topic)
        else:
            bot_reply_message = 'Hier sind die fünf aktuellen Schlagzeilen: \n'
            news_titles, news_urls = ns.search_news()

        bot_reply_message += news_titles
        dispatcher.utter_message(bot_reply_message)

        return [SlotSet('news', '')]
