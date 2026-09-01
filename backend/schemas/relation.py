from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime


class RelationBase(BaseModel):
    source_identity_id: str = Field(..., min_length=1)
    target_identity_id: str = Field(..., min_length=1)
    correlation_type: str = Field(..., min_length=1, max_length=100)
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    evidence: Dict[str, Any] = Field(default_factory=dict)
    explanation: Optional[str] = None


class RelationCreate(RelationBase):
    pass


class RelationResponse(RelationBase):
    id: str
    source_username: Optional[str] = None
    target_username: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
