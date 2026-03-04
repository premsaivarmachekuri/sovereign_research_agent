from fastapi import APIRouter
from app.agents.base_agent import run_agent

router = APIRouter()


@router.post("/agent/run")
async def agent_endpoint(query: str):
    """Run the agentic AI pipeline."""
    result = await run_agent(query)
    return {"result": result}