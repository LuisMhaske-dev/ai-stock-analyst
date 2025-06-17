from newsapi import NewsApiClient
import os


class NewsAgent:
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")
        self.newsapi = NewsApiClient(api_key=self.api_key)

    def get_news_summary(self, ticker: str, region: str) -> str:
        try:
            # Add region keyword to make search more targeted
            search_term = f"{ticker} stock {region}"

            articles = self.newsapi.get_everything(
                q=search_term,
                language='en',
                sort_by='publishedAt',
                page_size=3
            )

            if not articles['articles']:
                return "No recent news found."

            summaries = []
            for article in articles['articles']:
                summaries.append(f"- {article['title']}: {article['description'] or 'No summary available.'}")
            return "\n".join(summaries)

        except Exception as e:
            return f"News unavailable: {str(e)}"