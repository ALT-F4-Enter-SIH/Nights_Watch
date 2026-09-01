"""Correlation analysis request/response schemas."""
from pydantic import BaseModel, Field
from typing import Optional


class CorrelationRequest(BaseModel):
    identity_ids: list[str] = Field(..., min_length=2, max_length=50)
    methods: Optional[list[str]] = Field(
        default=None,
        description="Correlation methods to use. Defaults to all. "
                    "Options: username, alias, pgp, wallet, behavioral, stylometry, infrastructure",
    )
    min_confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class CorrelationMatch(BaseModel):
    source_id: str
    target_id: str
    correlation_type: str
    confidence_score: float
    evidence: dict
    explanation: str


class CorrelationResult(BaseModel):
    pair_count: int
    identities_analyzed: int
    correlations_found: int
    correlations: list[CorrelationMatch]
    analysis_methods_used: list[str]
    duration_ms: float


class StylometryRequest(BaseModel):
    text_a: str = Field(..., min_length=10, max_length=10000)
    text_b: str = Field(..., min_length=10, max_length=10000)


class WritingSignature(BaseModel):
    avg_word_length: float
    punctuation_density: float
    vocabulary_diversity: float
    sentence_length_avg: float
    ngram_signature: dict[str, float]


class StylometryResult(BaseModel):
    similarity_score: float  # 0-1
    text_a_signature: WritingSignature
    text_b_signature: WritingSignature
    shared_ngrams: int
    vocabulary_overlap: float
    analysis_method: str = "char_trigram_embedding"
    duration_ms: float
