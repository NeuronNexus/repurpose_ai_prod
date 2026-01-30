# RepurposeAI – Backend Architecture

## Overview

The backend serves as the **core intelligence layer** of RepurposeAI, functioning as an agentic research system rather than a traditional CRUD application. It orchestrates reasoning, validation, and synthesis across multiple specialized agents to deliver structured pharmaceutical research insights.

---

## Technology Stack

- **Runtime**: Python
- **Framework**: FastAPI
- **AI Model**: Google Gemini (via REST API)
- **PDF Generation**: ReportLab
- **Data Persistence**: None (stateless MVP architecture)

---

## System Architecture

### Core Responsibilities

The backend system:
- Receives and interprets high-level user research queries
- Decomposes requests into structured, domain-specific tasks
- Orchestrates execution across specialized agent workflows
- Validates and normalizes all LLM outputs against strict schemas
- Synthesizes cross-domain insights into coherent analyses
- Generates both JSON responses and executive PDF reports

### Design Principles

- **Stateless**: No session or database dependencies
- **Deterministic**: Reproducible outputs within LLM variance bounds
- **Schema-Strict**: All outputs validated against predefined models
- **Traceable**: Clear reasoning chains across agent interactions

---

## Multi-Agent Architecture

The MVP intentionally implements **three specialized agents** to balance capability with maintainability:

### 1. Master Agent
*System orchestrator and synthesis engine*

- Interprets user queries and extracts key entities (drug, indication)
- Defines research objectives and analytical assumptions
- Creates execution plans for specialized agents
- Performs cross-domain synthesis of agent outputs
- Generates hypothesis strength scores and strategic recommendations

**Role**: System brain and final decision synthesizer

### 2. Clinical Evidence Agent
*Scientific credibility evaluator*

- Analyzes biomedical evidence from conceptual frameworks
- Structures findings by study type, outcomes, and statistical signals
- Assesses methodological limitations and confidence levels
- Produces evidence quality ratings and clinical feasibility assessments

**Role**: Scientific rigor and medical validity validator

### 3. Patent Analysis Agent
*Intellectual property landscape analyzer*

- Maps patent coverage across therapeutic applications
- Identifies key patents and potential infringement risks
- Evaluates freedom-to-operate scenarios
- Surfaces white-space opportunities for development

**Role**: IP feasibility and commercial risk assessor

### Design Rationale

This three-agent constraint:
- Reduces integration complexity and debugging overhead
- Maintains traceable reasoning paths
- Keeps the MVP scope defensible and deliverable
- Enables rapid iteration on core workflows

---

## Schema-First Design

### Validation Strategy

All agent outputs must conform to strict Pydantic schemas. The system **never trusts raw LLM output** without validation.

**Key Techniques**:
- Safe JSON extraction with fallback parsing
- List normalization and deduplication
- Nested object flattening for frontend compatibility
- Strict FastAPI response models with type enforcement

**Protection Against**:
- Runtime type errors and exceptions
- Frontend rendering failures
- Hallucinated or malformed data structures
- Silent data corruption

---

## API Endpoints

### Analysis Endpoint
```http
POST /api/analyze
Content-Type: application/json
```

**Request Body**:
```json
{
  "query": "Evaluate Drug X for Indication Y"
}
```

**Response**: Complete multi-agent structured analysis with cross-domain synthesis

---

### PDF Report Generation
```http
POST /api/report/pdf
Content-Type: application/json
```

**Request Body**:
```json
{
  "analysis": { 
    /* Full analysis JSON object */ 
  }
}
```

**Response**: Executive research brief in PDF format

---

## Orchestration Workflow

```
┌─────────────────────────────────────────────────────────┐
│ 1. User Query → /api/analyze                            │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│ 2. Master Agent: Parse intent & create investigation    │
│    plan (drug, indication, objectives)                  │
└──────────────────┬──────────────────────────────────────┘
                   │
         ┌─────────┴─────────┐
         │                   │
┌────────▼─────────┐  ┌──────▼──────────┐
│ 3. Clinical      │  │ 3. Patent       │
│    Evidence      │  │    Analysis     │
│    Agent         │  │    Agent        │
└────────┬─────────┘  └──────┬──────────┘
         │                   │
         └─────────┬─────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│ 4. Master Agent: Synthesize findings & generate         │
│    hypothesis strength score                            │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│ 5. Return validated JSON response                       │
└─────────────────────────────────────────────────────────┘
```

**Note**: No streaming or partial outputs in MVP. Clients receive complete, validated results.

---

## PDF Generation

### Implementation

- **Library**: ReportLab (Platypus layout engine)
- **Output Style**: Consulting-grade executive brief
- **Page Limit**: 1–2 pages maximum
- **Rendering**: Server-side, no browser dependencies

### Design Goals

- Deterministic layout across all platforms
- Offline generation capability
- Professional formatting with clear hierarchy
- Optimized for executive decision-making

---

## Google Gemini Integration

### Configuration

The system uses Google's Gemini API for LLM inference via REST endpoints.

**Client Implementation**: `app/core/gemini_client.py`

**Environment Variables** (set in `backend/.env`):
```bash
GEMINI_API_KEY=your_api_key_here       # Required
GEMINI_MODEL=gemini-flash-latest       # Optional, defaults to gemini-flash-latest
```

### Features

- **Model**: `gemini-flash-latest` (hardcoded default)
- **Retry Logic**: Exponential backoff for rate limit (429) errors
- **Response Parsing**: Automatic Markdown fence stripping and JSON extraction
- **Error Handling**: Graceful degradation with informative error messages

### Migration Note

This project previously used Ollama for local LLM execution. That integration has been fully removed and replaced with Gemini. A legacy file (`app/core/ollama_client.py`) exists as a helpful error message; it can be safely deleted.

---

## CORS Configuration

CORS is enabled for development and demo purposes:

- **Frontend**: `http://localhost:5173` (Vite dev server)
- **Backend**: `http://127.0.0.1:8000` (FastAPI)

**Production Consideration**: Update CORS origins before deploying to production environments.

---

## Local Development Setup

### Prerequisites

- Python 3.9+
- Valid Google Gemini API key

### Installation

1. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   
   Create `backend/.env`:
   ```bash
   GEMINI_API_KEY=your_actual_api_key_here
   GEMINI_MODEL=gemini-flash-latest
   ```

3. **Start the server**:
   ```powershell
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

4. **Verify**:
   - API documentation: `http://127.0.0.1:8000/docs`
   - Health check: `http://127.0.0.1:8000/health`

The frontend requires no changes and will communicate with the same API routes.

---

## Intentional MVP Exclusions

The following capabilities are **deliberately excluded** from the MVP scope:

- ❌ User authentication and authorization
- ❌ Database or persistent storage
- ❌ Model fine-tuning or custom training
- ❌ Streaming token responses
- ❌ Multi-user session management
- ❌ Advanced caching strategies

These exclusions keep the MVP focused, deployable, and technically defensible.

---

## Recommended Cleanup

- **Remove**: `app/core/ollama_client.py` (legacy integration, no longer used)
- **Keep**: `app/core/gemini_client.py` (active LLM client)

---

## Summary

RepurposeAI's backend is a research-grade agentic system designed for structured pharmaceutical analysis. It leverages Google Gemini for intelligent reasoning, enforces strict schema validation, and delivers executive-ready outputs in both JSON and PDF formats.

**Key Strengths**:
- Multi-agent orchestration with clear separation of concerns
- Schema-first architecture preventing runtime failures
- Deterministic, traceable reasoning chains
- Production-ready PDF generation
- Stateless, scalable design

Configure your `GEMINI_API_KEY`, start the server, and begin analyzing drug repurposing opportunities with AI-powered insights.