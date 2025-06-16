import sys
import os
import time
import streamlit as st
import pandas as pd

# Ensure project root is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from orchestration.main_adk import StockOrchestrator

def main():
    st.set_page_config(page_title="AI Stock Analyst", layout="wide")

    # Sidebar configuration
    with st.sidebar:
        st.header("Configuration")
        ticker = st.text_input("Stock Ticker", "AAPL").upper()
        risk_profile = st.selectbox("Risk Profile", ["low", "medium", "high"])

    orchestrator = StockOrchestrator()

    if st.button("Analyze"):
        with st.spinner("Running analysis..."):
            start_time = time.time()
            analysis = orchestrator.full_analysis(ticker, risk_profile)
            exec_time = time.time() - start_time

            # Two-column layout
            col1, col2 = st.columns(2)

            with col1:
                with st.expander("📊 Real-Time Data", expanded=True):
                    st.write(analysis["real_time_data"])

                with st.expander("📈 Technical Analysis", expanded=True):
                    # Price trend line chart
                    price_df = pd.DataFrame(analysis["technical_analysis"]["prices"])
                    st.line_chart(price_df.set_index("date")["price"])

                    # Display RSI and Volatility
                    st.metric("RSI", f'{analysis["technical_analysis"]["rsi"]}')
                    st.metric("Volatility", f'{analysis["technical_analysis"]["volatility"]}%')

                    # Show Moving Averages
                    st.subheader("Moving Averages")
                    st.write(analysis["technical_analysis"]["moving_averages"])

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