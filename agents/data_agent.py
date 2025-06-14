import yfinance as yf
from datetime import datetime

class DataAgent:
    def get_real_time_data(self, ticker: str) -> dict:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            "price": info.get("currentPrice", info.get("regularMarketPrice")),
            "currency": info.get("currency"),
            "updated_at": datetime.now().isoformat(),
            "volume": info.get("regularMarketVolume")
        }
