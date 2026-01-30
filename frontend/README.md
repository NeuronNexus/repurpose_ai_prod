# AI-Powered Drug Repurposing Assistant

> A multi-agent research pipeline for evaluating drug repurposing opportunities with clinical evidence synthesis and patent landscape analysis.

## System Overview

This MVP is an **AI-powered drug repurposing assistant** built as a **multi-agent system** with strict schema enforcement and offline LLM execution.

**Query Example:**
```
"Evaluate Drug X for Indication Y"
```

**System Output:**
- Structured planning
- Clinical evidence synthesis
- Patent landscape analysis
- Cross-domain reasoning
- Executive PDF report

> **Note:** This is NOT a chatbot. It is an orchestrated, agentic research pipeline.

---

## Architecture

### Frontend
- **Framework:** React (Vite) + Tailwind
- **Port:** `localhost:5173`
- **Purpose:** Pure UI + orchestration layer
- **Design:** No business logic, communicates with backend via REST

### Backend
- **Framework:** FastAPI (Python)
- **Port:** `localhost:8000`
- **Characteristics:** Stateless, schema-strict, multi-agent orchestration

### LLM
- **Engine:** Ollama (local, offline)
- **Model:** `llama3.1:8b`
- **Properties:** Deterministic, private, slow but reliable

---

## Agent System

The system consists of **3 specialized agents**:

### 1. Master Agent
- Converts user query into structured investigation plan
- Extracts drug + indication
- Defines objectives
- Creates tasks routed to other agents
- Uses TRM-style refinement loop
- Outputs strictly validated JSON

### 2. Clinical Evidence Agent
- Analyzes biomedical evidence (PubMed / clinical trials)
- Produces structured study summaries
- Includes: study type, outcome, signal, limitations
- Outputs overall evidence signal
- Schema-safe string normalization

### 3. Patent Analysis Agent
- Analyzes patent landscape (USPTO / EPO / WIPO)
- Extracts key patents
- Determines freedom-to-operate: `high | moderate | low | unclear`
- Identifies risks and white-space opportunities
- Schema-safe, normalized data output

---

## Orchestration Flow
```
1. User enters query in frontend
2. Frontend → POST /api/analyze
3. Backend orchestrator executes:
   ├─ Master Agent (planning)
   ├─ Clinical Agent
   └─ Patent Agent
4. Master Agent performs final synthesis:
   ├─ Aligns clinical + patent signals
   ├─ Identifies risks, contradictions, opportunities
   └─ Produces hypothesis strength score
5. Backend returns single structured JSON response
```

**Key Characteristics:**
- No streaming
- No partial responses
- Strict validation enforced by FastAPI

---

## Critical Engineering Decisions

- ✅ All LLM outputs normalized before returning
- ✅ Lists flattened to `List[str]` to avoid schema failures
- ✅ No `json.loads()` directly on LLM output
- ✅ Safe JSON extraction used throughout
- ✅ Backend never trusts LLM blindly
- ✅ CORS explicitly enabled for Vite frontend
- ✅ Backend fully stateless
- ✅ No database (by design for MVP)

---

## PDF Report Generation

**Endpoint:** `POST /api/report/pdf`

**Input:** Full analysis JSON  
**Output:** Downloadable PDF

**Implementation:**
- Uses `reportlab` (not HTML-to-PDF)
- Produces 1–2 page executive research brief

**Report Contents:**
- Hypothesis strength
- Clinical evidence table
- Patent summary
- Risks and opportunities
- Recommended next steps

**Trigger:** Frontend "Download PDF" button

---

## Frontend Behavior

- Shows agent progression visually
- Handles long-running inference (minutes)
- Displays results only after backend completes
- Does not assume schema beyond documented structure
- Graceful error handling (CORS, network, API failures)

> **Design Philosophy:** Frontend is intentionally thin. All intelligence lives in the backend.

---

## Development Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- Ollama with `llama3.1:8b` model

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Verify Ollama
```bash
ollama run llama3.1:8b
```

---

## Extension & Optimization

This system is designed to be extended. You can:

- ✨ Add new specialized agents
- 🚀 Optimize LLM inference performance
- 🔌 Connect real data sources (PubMed API, USPTO API)
- 📊 Enhance prompt engineering
- ⚡ Reduce latency with caching
- 🌐 Deploy to production infrastructure
- 🧪 Add evaluation metrics

---

## API Endpoints

### Analysis Endpoint
```http
POST /api/analyze
Content-Type: application/json

{
  "query": "Evaluate metformin for Alzheimer's disease"
}
```

### PDF Report Endpoint
```http
POST /api/report/pdf
Content-Type: application/json

{
  "analysis": { ... }
}
```

---

## Project Structure
```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── agents/              # Agent implementations
│   ├── orchestrator.py      # Multi-agent coordination
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── components/      # React components
    │   └── App.jsx          # Main application
    └── package.json
```

---

## Design Principles

1. **Schema-First:** All outputs strictly validated
2. **Offline-First:** No external API dependencies
3. **Agent-Oriented:** Modular, specialized reasoning units
4. **Stateless Backend:** No session management
5. **Deterministic:** Reproducible results

---

## Contributing

When extending this system:
- Maintain strict schema validation
- Keep agents focused and specialized
- Normalize all LLM outputs
- Add comprehensive error handling
- Document new agents in this README

---

