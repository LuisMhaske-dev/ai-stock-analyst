import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from orchestration.main_adk import StockOrchestrator
import time

def main():
    st.set_page_config(page_title="AI Stock Analyst", layout="wide")
    
    with st.sidebar:
        st.header("Configuration")
        ticker = st.text_input("Stock Ticker", "AAPL").upper()
        risk_profile = st.selectbox("Risk Profile", ["low", "medium", "high"])
    
    orchestrator = StockOrchestrator()
    
    if st.button("Analyze"):
        with st.spinner("Processing..."):
            start_time = time.time()
            analysis = orchestrator.full_analysis(ticker, risk_profile)
            exec_time = time.time() - start_time
            
            col1, col2 = st.columns(2)
            
            with col1:
                with st.expander("Real-time Data"):
                    st.write(analysis["real_time_data"])
                
                with st.expander("Technical Analysis"):
                    st.line_chart(
                        analysis["technical_analysis"]["moving_averages"], 
                        use_container_width=True
                    )
                    st.metric("Volatility", 
                             f"{analysis['technical_analysis']['volatility']*100:.2f}%")
            
            with col2:
                with st.expander("Latest News"):
                    st.write(analysis["news_summary"])
                
                with st.expander("AI Recommendations"):
                    st.write(analysis["ai_insights"])
                    st.write(analysis["portfolio_recommendation"])
            
            st.caption(f"Analysis completed in {exec_time:.2f} seconds")

if __name__ == "__main__":
    main()
