"""
searches news using News API (https://newsapi.org/docs)
"""
import os
import json
import requests

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class NewsSearcher:
    def __init__(self):
        keys_file = ROOT_DIR + '/keys.json'
        with open(keys_file, 'r', encoding='utf-8') as f:
            self.api_key = json.load(f)['news-api-key']

    def get_topic_news(self, topic):
        url = ('https://newsapi.org/v2/everything?'
                'language=de&'
                'pageSize=5&'
               'q=' + topic + '&'
               'from=2019-02-06&'
               'sortBy=popularity&'
               'apiKey=' + self.api_key)
        response = requests.get(url)

        return response.json()

    def get_top_headlines(self):
        url = ('https://newsapi.org/v2/top-headlines?country=de&pageSize=5&apiKey=' + self.api_key)
        response = requests.get(url)

        return response.json()

    def search_news(self, topic=""):
        if topic:
            raw_news = self.get_topic_news(topic)
        else:
            raw_news = self.get_top_headlines()

        news_titles = ''
        news_titles_w_url = ''

        for article in raw_news['articles']:
            news_titles += article['title'] + '\n'
            news_titles_w_url += article['title'] + '\n' + article['url'] + '\n'

        return news_titles, news_titles_w_url

