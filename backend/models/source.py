from sqlalchemy import Column, String, Integer, DateTime, JSON
from sqlalchemy.sql import func
from database import Base
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class Source(Base):
    __tablename__ = "sources"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    source_type = Column(String, nullable=False)
    record_count = Column(Integer, default=0)
    imported_at = Column(DateTime, server_default=func.now())
    extra_metadata = Column(JSON, default=dict)
