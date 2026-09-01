from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class AnalysisRunCreate(BaseModel):
    run_type: str = Field(default="full", pattern="^(full|incremental|stylometry|behavioral|infrastructure)$")


class AnalysisRunResponse(BaseModel):
    id: str
    run_type: str
    identities_processed: int
    relations_found: int
    duration_seconds: float
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True
