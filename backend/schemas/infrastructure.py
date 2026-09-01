"""Infrastructure analysis schemas."""
from pydantic import BaseModel
from typing import Optional


class InfrastructureProfile(BaseModel):
    identity_id: str
    username: str
    origin_ip_range: Optional[str] = None
    user_agent: Optional[str] = None
    connection_type: Optional[str] = None
    platform_tags: list[str]
    pgp_fingerprint: Optional[str] = None
    crypto_wallets: list[str]
    email_domain: Optional[str] = None
    infrastructure_score: float  # 0-1


class InfrastructureLink(BaseModel):
    source_id: str
    target_id: str
    shared_ip_range: bool
    shared_pgp: bool
    shared_wallet_prefix: bool
    shared_connection_type: bool
    shared_user_agent_pattern: bool
    infrastructure_confidence: float
    shared_signals: list[str]
    explanation: str


class InfrastructureAnalysisResult(BaseModel):
    analyzed_pairs: int
    infrastructure_links_found: int
    links: list[InfrastructureLink]
    method: str = "metadata_fingerprint"
    duration_ms: float
