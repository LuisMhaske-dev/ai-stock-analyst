# ai-stock-analyst
Google ADK Hackathon (Jun-2025)

# Project Structure
/ai-stock-analyst  

├── agents/  

│ ├── news\_agent.py # News scraping/summarization  

│ ├── trends\_agent.py # Technical analysis  

│ ├── data\_agent.py # Real-time data fetching  

│ ├── insights\_agent.py # Investment advice generation  

│ └── portfolio\_agent.py # Risk-based recommendations  

├── orchestration/  

│ └── main\_adk.py # Agent coordination logic  

├── frontend/  

│ ├── app.py # Streamlit/Flask interface  

│ └── templates/ # HTML templates (if web UI)  

├── tests/ # Unit/integration tests  

├── infrastructure/  

│ ├── Dockerfile # Containerization  

│ └── cloudbuild.yaml # CI/CD pipeline  

├── docs/  

│ ├── ARCHITECTURE.md # System diagram explanation  

│ └── SETUP.md # Installation instructions  

└── requirements.txt # Python dependencies
