from dotenv import load_dotenv
load_dotenv()
from agents import NewsAgent, TrendsAgent, DataAgent, InsightsAgent, PortfolioAdvisor


class StockOrchestrator:
    def __init__(self):
        self.news_agent = NewsAgent()
        self.trends_agent = TrendsAgent()
        self.data_agent = DataAgent()
        self.insights_agent = InsightsAgent()
        self.portfolio_advisor = PortfolioAdvisor()
        
    def full_analysis(self, ticker: str, risk_profile: str) -> dict:  # Remove async
        return {
            "real_time_data": self.data_agent.get_real_time_data(ticker),
            "news_summary": self.news_agent.get_news_summary(ticker),
            "technical_analysis": self.trends_agent.analyze(ticker),
            "ai_insights": self.insights_agent.generate_advice(
                self.news_agent.get_news_summary(ticker),
                self.trends_agent.analyze(ticker)
            ),
            "portfolio_recommendation": self.portfolio_advisor.recommend_allocation(
                risk_profile,
                self.insights_agent.generate_advice(
                    self.news_agent.get_news_summary(ticker),
                    self.trends_agent.analyze(ticker)
                )
            )
        }
