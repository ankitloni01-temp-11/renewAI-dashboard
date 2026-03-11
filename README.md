# Project RenewAI — Suraksha Life Insurance

## Demo Setup

### Requirements
- Python 3.11+
- Node.js 20+
- Google AI Studio API Key (free at aistudio.google.com)
- LangSmith API Key (free at smith.langchain.com — optional)

### Quick Start

```bash
# 1. Clone and configure
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# 2. Backend
cd backend
pip install -r requirements.txt
python -m scripts.generate_seed_data    # generates seed data
uvicorn main:app --reload --port 8000

# 3. Frontend (new terminal)
cd frontend
npm install
npm run dev
```

Open http://localhost:3000

### Docker Quick Start (Recommended)
The easiest way to run the full stack (Frontend + Backend + MCP Servers) is using Docker Compose.

```bash
# 1. Clone the repository
git clone https://github.com/ankitloni01-temp-11/renewAI-dashboard.git
cd renewAI-dashboard

# 2. Configure environment
cp .env.example .env
# Open .env and add your GOOGLE_API_KEY (from aistudio.google.com)

# 3. Launch the stack
docker compose up --build -d
```

Once the build is complete:
- **Dashboard**: [http://localhost:3000](http://localhost:3000)
- **API (Backend)**: [http://localhost:8005](http://localhost:8005)

### Demo Walkthrough
1. Login as **Renewal Head** → View Executive KPI Dashboard
2. Click **T-45 Scan (5)** → Watch journeys start
3. Click **Run Journey: Rajesh** → Open WhatsApp Sim → Type "Can I pay in two instalments?"
4. Click **Run Journey: Meenakshi** → Open WhatsApp Sim → Type "My husband passed away last month"
5. Watch distress detected → Case appears in Queue → Login as Senior RRM → Resolve case
6. Login as **Compliance Handler** → Trace Investigation → See full agent audit trail

### Architecture
- 6 AI Agents: Orchestrator, Planner, Email, WhatsApp, Voice, Human Queue Manager
- 5 Critique Agents paired with execution agents
- 1 Content Safety Gate (deterministic, no LLM)
- LangGraph state machine for journey orchestration
- ChromaDB for RAG (objection library + policy documents)
- FastAPI backend, React + TypeScript frontend

### API Keys Cost
- Gemini 2.0 Flash: ~$5 total for full demo
- LangSmith: Free tier (5K traces/month)
