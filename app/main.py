from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="Sovereign Research Agent",
    description="An AI ensemble for generating professional research newsletters.",
    version="1.0.0",
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API router
app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the Sovereign Research Agent API server...")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the Sovereign Research Agent API server...")
