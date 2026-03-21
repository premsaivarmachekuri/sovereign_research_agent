from fastapi import APIRouter, HTTPException
from app.agent.base_agent import run_agent
from app.schemas.analyzer import AnalyzeRequest, AnalyzeResponse
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_topic(request: AnalyzeRequest):
    """
    Run the agentic AI pipeline to generate a newsletter on the given topic.
    """
    logger.info(f"Received analysis request for topic: {request.topic}")
    
    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty")
    
    try:
        newsletter = await run_agent(request.topic)
        return AnalyzeResponse(newsletter=newsletter)
    except Exception as e:
        logger.error(f"Error in analyze_topic: {e}")
        raise HTTPException(status_code=500, detail=f"Agent Error: {str(e)}")
