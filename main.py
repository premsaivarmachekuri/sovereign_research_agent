from fastapi import FastAPI
from app.api.v1.routes import router
from app.utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="sovereign_research_agent",
    description="An Agentic AI Application",
    version="0.1.0",
)

app.include_router(router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    logger.info("Health check called")
    return {"status": "ok", "project": "sovereign_research_agent"}