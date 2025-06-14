from vertexai.preview.generative_models import GenerativeModel
import os

class InsightsAgent:
    def __init__(self):
        self.model = GenerativeModel("gemini-pro")
        self.system_prompt = """You're a senior financial analyst. Consider:
        - News sentiment
        - Technical indicators (MA, RSI, Volatility)
        - Market conditions
        Output format: 
        VERDICT: [Buy/Hold/Sell]
        CONFIDENCE: [0-100%]
        REASON: [2-sentence explanation]"""
        
    def generate_advice(self, news: str, trends: dict) -> str:
        try:
            analysis_request = f"""
            NEWS SUMMARY:
            {news}
            
            TECHNICAL ANALYSIS:
            {trends}"""
            
            response = self.model.generate_content(
                system_instruction=self.system_prompt,
                contents=analysis_request
            )
            return response.text
        except Exception as e:
            return f"Analysis unavailable: {str(e)}"
