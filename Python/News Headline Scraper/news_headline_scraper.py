import json
from datetime import datetime
import feedparser
import sys

def fetch_headlines(feed):
    headlines = {}
    for name, url in feed.items():
        print(f"Fetching: {name}")
        feed = feedparser.parse(url)
        # print("FEED", feed)
        temp_list=[]
        for entry in feed.entries:
            article = {
                "title": entry.title,
                "link": entry.link,
                "published": entry.get("published", None)
            }
            temp_list.append(article)
        headlines[name]= temp_list
    return headlines



def save_to_json(data, filename="news_headlines.json"):
    timestamp = datetime.now().isoformat()
    output = {"timestamp": timestamp, "sources": data}
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)
    print("Headlines saved to the file")

if __name__=="__main__":
    
    feed={
        "BBC": "https://feeds.bbci.co.uk/news/rss.xml",
        "Reuters": "https://feeds.reuters.com/reuters/topNews",
        "CNN": "http://rss.cnn.com/rss/edition.rss",
        "NYTimes": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "HackerNews": "https://hnrss.org/frontpage"
    }

    headlines=fetch_headlines(feed)
    save_to_json(headlines)