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
        return self._calculate_indicators(data)
