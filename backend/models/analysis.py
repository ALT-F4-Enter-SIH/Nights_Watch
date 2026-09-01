from sqlalchemy import Column, String, Integer, Float, DateTime
from sqlalchemy.sql import func
from database import Base
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class AnalysisRun(Base):
    __tablename__ = "analysis_runs"

    id = Column(String, primary_key=True, default=generate_uuid)
    run_type = Column(String, default="full")
    identities_processed = Column(Integer, default=0)
    relations_found = Column(Integer, default=0)
    duration_seconds = Column(Float, default=0.0)
    status = Column(String, default="pending")
    created_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime, nullable=True)
