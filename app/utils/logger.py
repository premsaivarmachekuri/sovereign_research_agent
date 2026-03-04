import logging
import sys


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger
```

### `requirements.txt`
```
fastapi>=0.111.0
uvicorn[standard]>=0.29.0
langgraph>=0.1.0
langchain-openai>=0.1.0
pydantic-settings>=2.0.0
python-dotenv>=1.0.0
```

### `.env.example`
```
OPENAI_API_KEY=your-key-here
DEBUG=false
LOG_LEVEL=INFO