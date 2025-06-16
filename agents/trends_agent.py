import yfinance as yf
import pandas as pd
import numpy as np

class TrendsAgent:
    def __init__(self):
        self.window_sizes = [7, 30]  # Days
    
    def _calculate_indicators(self, data: pd.DataFrame) -> dict:
        return {
            "moving_averages": {
                f"{window}d": data['Close'].rolling(window).mean().iloc[-1]
                for window in self.window_sizes
            },
            "volatility": data['Close'].pct_change().std(),
            "rsi": self._calculate_rsi(data)
        }
    
    def _calculate_rsi(self, data: pd.DataFrame, window=14) -> float:
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs.iloc[-1]))

    def analyze(self, ticker: str) -> dict:
        data = yf.Ticker(ticker).history(period="3mo")
        indicators = self._calculate_indicators(data)

        trend_data = data[['Close']].reset_index()
        trend_data.columns = ['date', 'price']
        trend_data['date'] = trend_data['date'].dt.strftime('%Y-%m-%d')  # Make it JSON serializable

        return {
            "prices": trend_data.to_dict(orient="records"),
            "volatility": round(indicators["volatility"] * 100, 2),
            "rsi": round(indicators["rsi"], 2),
            "moving_averages": {
                k: round(v, 2) for k, v in indicators["moving_averages"].items()
            }
        }
