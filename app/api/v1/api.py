from fastapi import APIRouter
from app.api.v1.endpoints import analyzer, health

api_router = APIRouter()
api_router.include_router(analyzer.router, tags=["analyzer"])
api_router.include_router(health.router, prefix="/health", tags=["utils"])
