import requests
from newspaper import Article
import os

class NewsAgent:
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2/everything"
        
    def _fetch_articles(self, ticker: str, num_articles=3) -> list:
        params = {
            "q": ticker,
            "apiKey": self.api_key,
            "pageSize": num_articles,
            "sortBy": "publishedAt"
        }
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        return response.json()['articles']

    def get_news_summary(self, ticker: str) -> str:
        """Returns concatenated summaries of top news articles"""
        try:
            articles = self._fetch_articles(ticker)
            summaries = []
            for article in articles:
                a = Article(article['url'])
                a.download()
                a.parse()
                summaries.append(f"- {a.title}: {a.text[:200]}...")
            return "\n".join(summaries)
        except Exception as e:
            return f"News unavailable: {str(e)}"
