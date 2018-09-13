from bs4 import BeautifulSoup as soup
import requests

class GoogleNewsSearcher:
  def search_news(self, topic=""):

    params = {"q": topic,
              "output": "rss"}
    response = requests.get("https://news.google.de/", params=params)
    xml_page = response.content

    soup_page = soup(xml_page, "xml")
    news_list = soup_page.findAll("item")
    # Print news title, url and publish date
    """
    for news in news_list:
      print(news.title.text)
      print(news.link.text)
      print(news.pubDate.text)
      print("-"*60)
    """

    return news_list

"""
if __name__ == "__main__":
    news_list = GoogleNewsSearcher().search_news()

    news_utterance = ""
    for i in range(len(news_list)):
        if i != 0:
            #print(news_list[i].title.text)
            news_utterance += "\n" + news_list[i].title.text

    print(news_utterance)
"""