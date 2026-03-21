# 🛡️ Sovereign Research Agent

An autonomous research assistant that takes a topic, searches the web, analyzes multiple PDF documents, and generates a high-quality intelligence newsletter.

---

## 🚀 Concept

The **Sovereign Research Agent** is designed to perform deep research independently. Give it a topic like "Future of Solar Batteries," and it will:
1.  **Search**: Use the **Tavily API** to find current web data.
2.  **Analyze**: Read up to **5 PDF documents** from the search results or local sources.
3.  **Summarize**: Distill complex technical information into concise summaries.
4.  **Compose**: Write a final, formatted research newsletter.

## 🛠️ Tech Stack

*   **[LangGraph](https://python.langchain.com/docs/langgraph)**: Orchestrates the agent's state transitions and complex reasoning loops.
*   **[Tavily API](https://tavily.com/)**: powers real-time web search and information extraction.
*   **Local Llama-3**: Used for private, sovereign reasoning (integrated via **FastMCP**).
*   **[FastMCP](https://github.com/fastmcp/fastmcp)**: Efficient Model Context Protocol server for connecting local LLMs to external tools and knowledge.
*   **[FastAPI](https://fastapi.tiangolo.com/)**: RESTful API backend for interacting with the agent.
*   **[PyMuPDF](https://pymupdf.readthedocs.io/)**: For high-performance PDF parsing and extraction.

---

## ⚙️ Setup

### 1. Environment & Keys
Clone the repository and prepare your environment variables:
```bash
cp .env.example .env
```
Fill in the following in your `.env`:
- `OPENAI_API_KEY`: (Optional) If not using Local Llama-3.
- `TAVILY_API_KEY`: Your key from tavily.com.
- `LLM_BASE_URL`: URL for your local Llama-3 server (integrated via FastMCP).

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Agent
Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

---

## 📁 Structure
```text
app/
├── agent/              # LangGraph state-agent definitions
├── api/v1/             # API routes and endpoints
│   ├── endpoints/      # category-specific routes
│   └── api.py          # root v1 router
├── core/               # Configuration and Settings (Pydantic)
├── schemas/            # Pydantic models for request/response
├── utils/              # PDF parsing, logger, and helper tools
└── main.py             # Entry point for the FastAPI server
```

---

## 👨‍💻 Author
**Premsai Varma Chekuri made with ❤️ **