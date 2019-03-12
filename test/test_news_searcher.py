import re
from news_searcher import NewsSearcher


def test_search_news():
    ns = NewsSearcher()
    news_title, news_url = ns.search_news()

    assert len(news_title.split('\n')) == 6
    assert len(news_url.split('\n')) == 11


def test_search_news_with_topic():
    ns = NewsSearcher()
    topic = 'Sportnachrichten'
    topic = re.sub('nachrichten$', '', topic)
    news_title, news_url = ns.search_news(topic)

    assert len(news_title.split('\n')) == 6
