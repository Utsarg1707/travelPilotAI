# TravelPilot AI 🚀✈️

**TravelPilot AI** is a production-oriented, free-first, multi-agent travel planning and decision-support system built with **LangGraph**, **Groq LLM (Free Tier)**, **Model Context Protocol (MCP)**, **FastAPI**, **React + TypeScript**, and **Human-in-the-Loop (HITL)** controls.

---

## 🌟 Key Architecture Highlights

- **Multi-Agent Orchestration**: Powered by **LangGraph** with a Supervisor Agent routing dynamically to specialist agents (Flight, Hotel, Weather, Budget, Itinerary).
- **Free-First Engineering**: Built around **Groq API (Free Tier)**, open APIs (Open-Meteo for weather), and deterministic demo providers for flights/hotels.
- **Model Context Protocol (MCP)**: Decoupled tool execution via structured MCP clients and servers.
- **Deterministic Guardrails**: Strict input/output guardrails with prompt-injection defense and budget calculation in pure Python.
- **Human-in-the-Loop (HITL)**: Stateful interrupt/resume graph design enabling approval, editing, and plan revisions.
- **Production Observability**: Local structured logging (`structlog`) with optional zero-overhead **LangSmith** tracing.

---

## 📁 Repository Structure

```
travelpilot-ai/
├── backend/                  # FastAPI Application & LangGraph Agents
│   ├── app/
│   │   ├── api/             # REST endpoints (Plan, Session, HITL)
│   │   ├── agents/          # Supervisor & Specialist agents
│   │   ├── graph/           # LangGraph state machine & routing
│   │   ├── guardrails/      # Input & output safety & prompt injection
│   │   ├── mcp/             # MCP client abstractions
│   │   ├── models/          # Database models (SQLAlchemy)
│   │   ├── schemas/         # Pydantic schemas & TravelState
│   │   ├── services/        # Business logic services
│   │   ├── memory/          # Checkpointing & session memory
│   │   ├── providers/       # Flight/Hotel/Weather provider adapters
│   │   ├── observability/   # Structlog & LangSmith configuration
│   │   ├── config/          # Centralized configuration & LLM factory
│   │   └── main.py          # FastAPI server entrypoint
│   └── tests/               # Backend automated test suite
├── mcp_servers/              # Model Context Protocol server tools
├── frontend/                 # React + TypeScript user interface
├── evaluation/               # Agent evaluation suite & benchmarks
├── docs/                     # Architecture & system design specs
├── scripts/                  # Development & utility scripts
├── .env.example              # Environment variables blueprint
├── pyproject.toml            # Dependencies & project metadata
└── README.md
```

---

## 🚀 Quick Start (Development Mode)

### 1. Environment Setup
```bash
cp .env.example .env
# Add your free Groq API key in .env (optional for Demo mode)
```

### 2. Install Dependencies
```bash
pip install -e .[dev]
```

### 3. Run Tests
```bash
pytest backend/tests
```

---

## 🛡️ License
MIT License
