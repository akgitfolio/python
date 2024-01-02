import feedparser
from textblob import TextBlob
from typing import List, Dict

class NewsAggregator:
    def __init__(self, topics: List[str]):
        self.topics = topics
        self.sources = [f"https://news.google.com/rss/search?q={topic}" for topic in topics]

    def fetch_news(self) -> List[Dict[str, str]]:
        news_items = []
        for source in self.sources:
            try:
                feed = feedparser.parse(source)
                if feed.bozo:
                    print(f"Error parsing feed: {source}")
                    continue
                for entry in feed.entries:
                    summary = entry.get("summary", "")
                    news_items.append({
                        "title": entry.title,
                        "link": entry.link,
                        "summary": summary
                    })
            except Exception as e:
                print(f"Failed to fetch news from {source}: {e}")
        return news_items

    def analyze_sentiment(self, text: str) -> str:
        analysis = TextBlob(text)
        if analysis.sentiment.polarity > 0:
            return "Positive"
        elif analysis.sentiment.polarity == 0:
            return "Neutral"
        else:
            return "Negative"

    def generate_digest(self) -> List[Dict[str, str]]:
        news_items = self.fetch_news()
        for item in news_items:
            combined_text = f"{item['title']} {item['summary']}"
            item["sentiment"] = self.analyze_sentiment(combined_text)

        print("**Personalized News Digest**")
        for item in news_items:
            print(f"* **{item['title']}** ({item['sentiment']})")
            print(f"\t- Link: {item['link']}")

        return news_items

    def filter_by_sentiment(self, sentiment: str) -> None:
        filtered_news = [item for item in self.generate_digest() if item["sentiment"].lower() == sentiment.lower()]
        print(f"\n**News with {sentiment.upper()} Sentiment:**")
        for item in filtered_news:
            print(f"* **{item['title']}**")
            print(f"\t- Link: {item['link']}")

# Example usage
topics = ["technology", "sports", "business"]  
aggregator = NewsAggregator(topics)
aggregator.generate_digest() 
aggregator.filter_by_sentiment("positive") 
