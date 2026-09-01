from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class EvidenceItem(BaseModel):
    type: str
    value: str
    timestamp: str


class InvestigationBase(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    status: str = Field(default="open", pattern="^(open|in_review|closed|suspended)$")
    priority: str = Field(default="medium", pattern="^(low|medium|high|critical)$")
    linked_identities: list[str] = []
    evidence_items: list[EvidenceItem] = []
    notes: Optional[str] = None


class InvestigationCreate(InvestigationBase):
    pass


class InvestigationUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(open|in_review|closed|suspended)$")
    priority: Optional[str] = Field(None, pattern="^(low|medium|high|critical)$")
    linked_identities: Optional[list[str]] = None
    evidence_items: Optional[list[EvidenceItem]] = None
    notes: Optional[str] = None


class InvestigationResponse(InvestigationBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
