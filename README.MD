# {{PROJECT_NAME}}

{{DESCRIPTION}}

## Setup
```bash
cp .env.example .env
# Add your OPENAI_API_KEY to .env

pip install -r requirements.txt
uvicorn main:app --reload
```

## Structure
```
app/
├── api/v1/routes.py     # API endpoints
├── agents/base_agent.py # Your LangGraph agent
├── core/config.py       # Settings via .env
└── utils/logger.py      # Structured logging
```

## Author

{{AUTHOR}}
```

---

## Step 7 — Empty `__init__.py` files

Create empty `__init__.py` in every `app/` subdirectory so Python treats them as modules:
```
app/__init__.py
app/api/__init__.py
app/api/v1/__init__.py
app/agents/__init__.py
app/core/__init__.py
app/utils/__init__.py