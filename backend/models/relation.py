from sqlalchemy import Column, String, Float, DateTime, Text, JSON
from sqlalchemy.sql import func
from database import Base
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class Relation(Base):
    __tablename__ = "relations"

    id = Column(String, primary_key=True, default=generate_uuid)
    source_identity_id = Column(String, nullable=False, index=True)
    target_identity_id = Column(String, nullable=False, index=True)
    correlation_type = Column(String, nullable=False)
    confidence_score = Column(Float, nullable=False)
    evidence = Column(JSON, default=dict)
    explanation = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
