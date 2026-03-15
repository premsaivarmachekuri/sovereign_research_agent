# 🛡️ Sovereign Research Agent — Build Planning Checklist

> A step-by-step guide to build the **Sovereign Research Agent** from scratch on your own machine.
> Based on the [README.md](./README.MD) and the existing project structure.

---

## Phase 1: Prerequisites & Environment Setup

- [ ] **Install Python** (≥ 3.10 recommended)
  - Verify: `python --version`
- [ ] **Install pip** (comes with Python, verify with `pip --version`)
- [ ] **Install Git** and verify: `git --version`
- [ ] *(Optional)* Install **Docker Desktop** if you plan to use Docker for deployment
- [ ] *(Optional but recommended)* Install **Ollama** for running Local Llama-3 on your machine
  - Download from: https://ollama.com
  - Pull the model: `ollama pull llama3:8b`
  - Start the Ollama server: Ollama runs at `http://localhost:11434` by default

---

## Phase 2: Clone & Project Setup

- [ ] **Clone the repository**
  ```bash
  git clone https://github.com/premsaivarmachekuri/sovereign_research_agent.git
  cd sovereign_research_agent
  ```
- [ ] **Create a virtual environment**
  ```bash
  python -m venv .venv
  ```
- [ ] **Activate the virtual environment**
  - Windows: `.venv\Scripts\activate`
  - macOS/Linux: `source .venv/bin/activate`

---

## Phase 3: Configuration & API Keys

- [ ] **Copy the example environment file**
  ```bash
  cp .env.example .env
  ```
- [ ] **Get your Tavily API key**
  - Sign up at https://tavily.com and copy your key
- [ ] **Get your OpenAI API Key** *(optional — only if NOT using local Llama-3)*
  - Get it from https://platform.openai.com
- [ ] **Edit `.env`** and fill in the following values:
  ```
  OPENAI_API_KEY=sk-your-openai-key-here      # optional
  TAVILY_API_KEY=tvly-your-tavily-key-here     # required
  LLM_BASE_URL=http://localhost:11434           # for local Llama-3 via Ollama
  LLM_MODEL=llama3:8b
  LOG_LEVEL=INFO
  ENVIRONMENT=development
  ```

---

## Phase 4: Install Dependencies

- [ ] **Install all required Python packages**
  ```bash
  pip install -r requirements.txt
  ```
- [ ] Verify key packages are installed:
  - `fastapi`, `uvicorn` — API server
  - `langgraph`, `langchain-core` — Agent orchestration
  - `openai` — LLM client (works with Ollama too via `LLM_BASE_URL`)
  - `tavily-python` — Web search
  - `PyMuPDF` — PDF parsing
  - `fastmcp` — Model Context Protocol for local LLMs
  - `pydantic`, `pydantic-settings` — Config & validation

---

## Phase 5: Understand the Project Architecture

Review each component and understand its role before building it out:

- [ ] **`main.py`** — FastAPI entry point; mounts all routes under `/api/v1`
- [ ] **`app/core/config.py`** — Pydantic settings that load from `.env`
- [ ] **`app/utils/logger.py`** — Centralized logger used across the app
- [ ] **`app/api/v1/routes.py`** — API route definitions (triggers the agent)
- [ ] **`app/agent/base_agent.py`** — LangGraph state machine / agent definition

---

## Phase 6: Build the Core Agent Components

Work through each component in dependency order:

### 6a. Configuration Layer (`app/core/`)
- [x] Understand `config.py` — how it reads `TAVILY_API_KEY`, `LLM_BASE_URL`, etc.
- [x] Add any new settings you need

### 6b. Utilities (`app/utils/`)
- [x] Review `logger.py` — ensure logging is working
- [x] *(If not present)* Create `pdf_parser.py` — a utility using **PyMuPDF** to extract text from PDF files
  ```python
  import fitz  # PyMuPDF
  def parse_pdf(path: str) -> str:
      doc = fitz.open(path)
      return "\n".join(page.get_text() for page in doc)
  ```

### 6c. LangGraph Agent (`app/agent/`)
- [x] Understand `base_agent.py` — current agent state and graph structure
- [x] Define the **AgentState** (TypedDict) with fields:
  - `topic` (str) — research topic
  - `search_results` (list) — Tavily results
  - `pdf_texts` (list) — extracted PDF content
  - `summaries` (list) — per-document summaries
  - `newsletter` (str) — final output
- [x] Build the **LangGraph nodes**:
  - [x] `search_node` — calls Tavily API to fetch web results
  - [x] `pdf_reader_node` — downloads/reads up to 5 PDFs from results
  - [x] `summarizer_node` — uses LLM to summarize each PDF/document
  - [x] `composer_node` — writes the final newsletter from all summaries
- [x] Connect nodes into a **StateGraph** with proper edges
- [x] Compile the graph: `graph = workflow.compile()`

### 6d. API Routes (`app/api/v1/`)
- [x] Review `routes.py`
- [x] Ensure there is a `POST /analyze` endpoint that:
  - Accepts `{ "topic": "..." }` as JSON body
  - Invokes the LangGraph agent
  - Returns the generated newsletter

---

## Phase 7: Run the Application

- [x] **Start the FastAPI server**
  ```bash
  uvicorn main:app --reload
  ```
- [x] Open the auto-generated docs in your browser:
  `http://127.0.0.1:8000/docs`
- [x] **Test the health endpoint**
  ```bash
  curl http://127.0.0.1:8000/health
  # Expected: {"status": "ok", "project": "sovereign_research_agent"}
  ```
- [x] **Test the agent endpoint**
  ```bash
  curl -X POST http://127.0.0.1:8000/api/v1/analyze \
    -H "Content-Type: application/json" \
    -d "{\"topic\": \"Future of Solar Batteries\"}"
  ```
  *(On PowerShell, use single-line JSON or a `.json` file)*

---

## Phase 8: Verify Agent Behavior End-to-End

- [ ] Given a topic, the agent **searches** using Tavily and returns results
- [ ] The agent **reads PDFs** (up to 5) from the search results or local files
- [ ] The agent **summarizes** each document using the LLM
- [ ] The agent **composes** a coherent research newsletter
- [ ] The newsletter is **returned via the API** response

---

## Phase 9: (Optional) Docker Deployment

- [ ] Review `Dockerfile` and `docker-compose.yml`
- [ ] Build the Docker image:
  ```bash
  docker-compose build
  ```
- [ ] Start with Docker Compose:
  ```bash
  docker-compose up
  ```
- [ ] Access at `http://localhost:8000`

---

## Phase 10: Polish & Iteration

- [ ] Add proper **error handling** in each node (network errors, PDF parse failures)
- [ ] Add **input validation** on the `/analyze` route (e.g., topic length limits)
- [ ] Add **logging** at each agent step using `get_logger`
- [ ] *(Optional)* Add a **feedback loop** node that refines the newsletter if it is too short
- [ ] *(Optional)* Stream the newsletter output using FastAPI `StreamingResponse`
- [ ] *(Optional)* Write unit tests for individual nodes using `pytest`
- [ ] Update `README.md` with any new features or changes

---

## 🔑 Key Concepts to Learn Along the Way

| Concept | Resource |
|---|---|
| LangGraph state graphs | https://python.langchain.com/docs/langgraph |
| Tavily Search API | https://docs.tavily.com |
| FastMCP (local LLM bridge) | https://github.com/fastmcp/fastmcp |
| PyMuPDF PDF parsing | https://pymupdf.readthedocs.io |
| FastAPI basics | https://fastapi.tiangolo.com |
| Pydantic settings | https://docs.pydantic.dev/latest/concepts/pydantic_settings |

---

*Author: Premsai Varma Chekuri*
