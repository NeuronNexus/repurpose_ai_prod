# RepurposeAI
**Evidence & IP-Aware Drug Repurposing Assistant**

RepurposeAI is a research-grade, multi-agent AI system that evaluates drug repurposing opportunities by combining clinical evidence analysis and patent landscape reasoning into a single, structured assessment.

Unlike generic LLM chat tools, RepurposeAI is built as an agentic research pipeline that:
* plans investigations,
* reasons across domains,
* validates outputs against strict schemas, and
* produces decision-ready executive reports.

---

## 🚀 What We Are Building

RepurposeAI answers questions like:

**"Evaluate Metformin for inflammatory conditions"**

and returns:
* a structured investigation plan,
* summarized clinical evidence,
* patent/IP feasibility insights,
* cross-domain synthesis with risks and opportunities,
* a quantified hypothesis strength score,
* and a downloadable executive PDF report.

**This is not a chatbot.** It is an AI research assistant designed to behave like a junior scientific & IP analyst.

---

## 🧪 Project Status

**Stage:** ✅ Functional MVP (Hackathon-ready)

### What works today:
* Multi-agent backend (Master + Clinical + Patent agents)
* Offline local LLM execution (Ollama)
* Strict schema validation & normalization
* React frontend with agent progression
* Executive PDF report generation

### What's intentionally excluded (for MVP):
* Authentication
* Database / persistence
* External API integrations (PubMed, USPTO – mocked conceptually)
* Deployment / scaling

---

## 🧠 High-Level Architecture

### Frontend
* React (Vite) + Tailwind
* Pure UI & orchestration
* No business logic
* Talks to backend via REST

### Backend
* FastAPI (Python)
* Multi-agent orchestration
* Schema-strict outputs
* Stateless design

### LLM
* Ollama (local, offline)
* Model: `llama3.1:8b`
* Used for all reasoning steps

---

## ⚙️ Prerequisites

Before running the app, you need Ollama installed.

### 1. Install Ollama
Download from: 👉 [https://ollama.com](https://ollama.com)

After installation, verify:
```bash
ollama --version
```

### 2. Pull the Required Model
```bash
ollama pull llama3.1:8b
```

⚠️ **This model is intentionally large and slow. Long inference times (3–6 minutes) are expected.**

---

## 🖥️ How to Run the Application

### Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs at:
```
http://127.0.0.1:8000
```

### Frontend (React)
```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:
```
http://localhost:5173
```

---

## 🔍 How to Use the App

1. Open the frontend in your browser
2. Enter a query (examples below)
3. Click **Run Analysis**
4. Wait while agents execute (3–6 minutes)
5. Review structured results
6. Click **Download PDF** to get the executive report

---

## 🧾 Example Queries (Recommended)

Use single-drug, single-indication queries.

### Good Queries
```
Evaluate Metformin for inflammatory conditions
```
```
Assess Aspirin for neuroinflammation
```
```
Analyze Atorvastatin for autoimmune disorders
```
```
Explore repurposing Propranolol for anxiety disorders
```

### Avoid (for MVP)
* Vague queries: `Find new uses for drugs`
* Multiple drugs in one query: `Evaluate Metformin and Aspirin together`
* Market or financial questions: `Is Metformin profitable`

---

## 📄 PDF Report Output

RepurposeAI can generate a 1–2 page executive research brief including:
* hypothesis strength score,
* clinical evidence table,
* patent/IP feasibility summary,
* risks, opportunities, and next steps.

PDFs are generated server-side using `reportlab` and downloaded directly from the UI.

---

## 🎯 Design Philosophy

* **Schema-first:** backend never trusts raw LLM output
* **Agentic:** reasoning is decomposed, not monolithic
* **Offline-first:** no external API dependency
* **Minimal UI:** clarity over dashboards
* **Deterministic MVP:** fewer moving parts, stronger narrative

---

## 🧩 Future Extensions (Out of Scope for MVP)

* Real PubMed / ClinicalTrials.gov integration
* Real patent database connectors
* Market and regulatory agents
* Caching and performance optimization
* Cloud deployment

---

## 📌 Final Note

RepurposeAI is built to demonstrate how AI systems should reason, not just respond.

It shows:
* planning before execution,
* cross-domain synthesis,
* and structured, auditable outputs.

**That is the core contribution of this MVP.**
