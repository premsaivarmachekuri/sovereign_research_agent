from fastapi import APIRouter
from app.schemas.health import Status
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/", response_model=Status)
async def health_check():
    """Check the application's health status."""
    logger.info("Health check endpoint reached.")
    return Status(status="ok", project="sovereign_research_agent")
