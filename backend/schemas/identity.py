from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class IdentityBase(BaseModel):
    username: str = Field(..., min_length=1, max_length=200)
    aliases: List[str] = Field(default_factory=list)
    email: Optional[str] = Field(None, max_length=320)
    pgp_fingerprint: Optional[str] = Field(None, max_length=200)
    crypto_wallets: List[str] = Field(default_factory=list)
    platform: Optional[str] = Field(None, max_length=50)
    bio: Optional[str] = None
    writing_samples: List[str] = Field(default_factory=list)
    posting_hours: List[int] = Field(default_factory=list)
    categories: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class IdentityCreate(IdentityBase):
    source_id: Optional[str] = None


class IdentityUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=1, max_length=200)
    aliases: Optional[List[str]] = None
    email: Optional[str] = None
    pgp_fingerprint: Optional[str] = None
    crypto_wallets: Optional[List[str]] = None
    platform: Optional[str] = None
    bio: Optional[str] = None
    writing_samples: Optional[List[str]] = None
    posting_hours: Optional[List[int]] = None
    categories: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class IdentityResponse(IdentityBase):
    id: str
    source_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
