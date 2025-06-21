import sys
import os
import time
import streamlit as st
import pandas as pd

# Ensure project root is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from orchestration.main_adk import StockOrchestrator


def interpret_volume(volume):
    try:
        volume = int(volume)
        if volume > 50_000_000:
            return f"{volume:,} (📈 High)"
        elif volume > 10_000_000:
            return f"{volume:,} (↗️ Moderate)"
        else:
            return f"{volume:,} (📉 Low)"
    except (ValueError, TypeError):
        return "N/A"


def display_real_time_data(data: dict):
    price = data.get("price", "N/A")
    currency = data.get("currency", "")
    updated_at = data.get("updated_at", "N/A")
    volume_raw = data.get("volume", "N/A")
    volume = interpret_volume(volume_raw)

    st.metric("Price", f"{price} {currency}")
    st.metric("Volume", volume)
    st.caption(f"Last updated at: {updated_at}")

def main():
    st.set_page_config(page_title="AI Stock Analyst", layout="wide")

    # Sidebar configuration
    with st.sidebar:
        region = st.selectbox("Region", ["USA", "India", "UK", "Germany", "Japan"])
        st.header("Configuration")
        ticker = st.text_input("Stock Ticker", "AAPL").upper()
        risk_profile = st.selectbox("Risk Profile", ["low", "medium", "high"])

    orchestrator = StockOrchestrator()

    if st.button("Analyze"):
        with st.spinner("Running analysis..."):
            start_time = time.time()
            analysis = orchestrator.full_analysis(ticker, risk_profile, region)
            exec_time = time.time() - start_time

            # Two-column layout
            col1, col2 = st.columns(2)

            with col1:
                with st.expander("📊 Real-Time Data", expanded=True):
                    display_real_time_data(analysis["real_time_data"])

                with st.expander("📈 Technical Analysis", expanded=True):
                    price_df = pd.DataFrame(analysis["technical_analysis"]["prices"])

                    if not price_df.empty and "date" in price_df.columns:
                        # Price trend line chart
                        st.line_chart(price_df.set_index("date")["price"])

                        # Display RSI and Volatility
                        st.metric("RSI", f'{analysis["technical_analysis"]["rsi"]}')
                        st.metric("Volatility", f'{analysis["technical_analysis"]["volatility"]}%')

                        # Show Moving Averages
                        st.subheader("Moving Averages")
                        st.write(analysis["technical_analysis"]["moving_averages"])
                    else:
                        st.warning("📉 No trend data available for this ticker and region.")

            with col2:
                with st.expander("📰 Latest News", expanded=True):
                    st.write(analysis["news_summary"])

                with st.expander("🤖 AI Recommendations", expanded=True):
                    st.write(analysis["ai_insights"])
                    st.write("📁 Portfolio Suggestion")
                    st.write(analysis["portfolio_recommendation"])

            st.caption(f"✅ Analysis completed in {exec_time:.2f} seconds")

if __name__ == "__main__":
    main()