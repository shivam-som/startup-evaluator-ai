# Startup Evaluator AI

A **multi-agent AI system** built using **LangGraph** that evaluates startup ideas in real time. Users submit startup concepts via a web-based chat interface, and the system orchestrates multiple specialized agents—**Market Analyst**, **Technical Reviewer**, and **Business Strategist**—to provide structured, actionable insights. The evaluation is streamed back to the user incrementally, ensuring a seamless, interactive experience.


## LangGraph Workflow Diagram

A visual representation of the multi-agent workflow is provided in the repository:  
**`langgraph-workflow-diagram.txt`** ✅

This diagram shows how user input is routed through agents, including conditional branching, context sharing, and streaming of the final evaluation back to the user.


## Features

- **Real-time Streaming Chat Interface**: Powered by FastAPI and a simple web frontend.
- **Multi-Agent System**:  
  - **Market Analyst Agent** – Evaluates market fit, customer demand, and competition.  
  - **Technical Reviewer Agent** – Assesses technical feasibility and architecture.  
  - **Business Strategist Agent** – Reviews business model, pricing strategy, and go-to-market approach.  
- **Adaptive LangGraph Workflow**: Agents share context, adapt based on prior results, and may escalate for clarification.  
- **Streaming Responses**: Incremental, token-by-token responses to the user for a natural chat experience.  
- **Containerized Deployment**: Docker and Docker Compose enable one-command startup.
- **Flexible LLM Usage**: Handles free-tier limits gracefully using multiple Google AI Studio models.

---


## LLM Client (`llm_client.py`)

The `llm_client.py` file provides two approaches to call Google AI Studio models:

1. **Primary Approach** (default):  
   - Uses a **specific model** (`models/gemini-2.5-flash-lite-preview-06-17`) to generate responses.  
   - This approach is **faster** and simpler.  

2. **Fallback Approach** (optional, uncomment when free-tier limit is reached):  
   - Iterates through **all available Google AI Studio models** that support content generation.  
   - Automatically picks the first available model that works.  
   - Ensures the system **never blocks** due to API usage limits.  

This design allows the system to remain **robust and continuously operational**, even if the free quota for a particular model is exhausted.  


---

## Repository Structure

```

├── backend
│   ├── main.py                # FastAPI backend entrypoint
│   ├── my_workflow.py         # LangGraph workflow orchestration
│   ├── requirements.txt       # Backend dependencies
│   ├── agents                 # Specialized AI agents
│   │   ├── business_agent.py
│   │   ├── market_agent.py
│   │   ├── technical_agent.py
│   │   ├── recommendation_agent.py
│   │   └── final_agent.py
│   └── utils                  # Helper utilities (e.g., LLM client)
│       └── llm_client.py
├── frontend
│   ├── index.html             # Web interface
│   ├── script.js              # Frontend logic for chat and streaming
│   └── style.css              # Styles
├── Dockerfile                 # Container image for backend
├── docker-compose.yml         # Run backend + frontend
├── .env                       # Environment variables (e.g., API keys)
├── requirements.txt           # Root Python dependencies (optional)
└── README.md                  # Project documentation

````

---

## Setup & Run Instructions

1. **Clone the repository**

```bash
git clone https://github.com/shivam-som/startup-evaluator-ai.git
cd startup-evaluator-ai
````

2. **Create `.env` file** with your LLM API key, e.g.:

```env
OPENAI_API_KEY=your_api_key_here
GS_MODEL_NAME=models/gemini-2.5-flash-lite-preview-06-17
```

3. **Install dependencies** (optional if using Docker):

pip install -r backend/requirements.txt

4. **Run with Docker Compose** (recommended):

docker compose up

5. **Access the web app**: Open [http://localhost:8000](http://localhost:8000) in your browser.
   Submit a startup idea and see the streaming evaluation in real time.

---

## Example Input & Output

**Input:**

```
I’m building an AI platform that helps small businesses automatically generate product descriptions and marketing copy tailored to different customer segments.
```

**Streamed Output:**

```
Startup Evaluation Report
Market Analysis:
There is increasing demand for AI-assisted content tools in the SMB segment...
Technical Feasibility:
The system is feasible using pre-trained LLMs with light customization...
Business Strategy:
B2B SaaS with tiered pricing is a viable approach. However, customer acquisition could be challenging...
Recommendation: Proceed with MVP; focus initial testing on e-commerce verticals.
```

---

## Architecture Overview

* **Frontend**: Simple HTML/JS interface for real-time streaming chat.
* **Backend**: FastAPI server that orchestrates LangGraph workflow.
* **Agents**: Modular Python classes for Market, Technical, Business, and Recommendation analysis.
* **Workflow**: LangGraph graph manages conditional routing, context sharing, and adaptive agent execution.
* **Streaming**: Backend streams incremental responses via server-sent events (SSE) to the frontend.
* **LLM Client**: Handles Google AI Studio model calls with fallback to ensure uninterrupted responses.

---

## Agents Description

| Agent                | Responsibility                                                |
| -------------------- | ------------------------------------------------------------- |
| Market Analyst       | Evaluates market demand, trends, and competition.             |
| Technical Reviewer   | Checks technical feasibility and architecture considerations. |
| Business Strategist  | Assesses business model, pricing, GTM strategy, risks.        |
| Recommendation Agent | Synthesizes all agent outputs into structured advice.         |
| Final Agent          | Formats and streams the final report to the user.             |

---

## Future Modifications

* Improve LLM agent reasoning with more context-aware prompts.
* Add authentication and user management.
* Enhance frontend UI/UX for better visualization of multi-part responses.
* Extend agents to leverage external APIs for real-time market insights.

---

