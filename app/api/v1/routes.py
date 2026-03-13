from fastapi import APIRouter
from app.agent.base_agent import run_agent

router = APIRouter()


@router.post("/analyze")
async def agent_endpoint(data: dict):
    """Run the agentic AI pipeline."""
    topic = data.get("topic")
    if not topic:
        return {"error": "topic is required"}
    result = await run_agent(topic)
    return {"result": result}