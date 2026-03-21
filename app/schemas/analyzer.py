from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    topic: str = Field(..., description="The research topic to investigate", example="Future of Solar Batteries")


class AnalyzeResponse(BaseModel):
    newsletter: str = Field(..., description="The generated research newsletter content")
