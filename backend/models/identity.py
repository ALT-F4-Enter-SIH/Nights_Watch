from sqlalchemy import Column, String, DateTime, Text, JSON
from sqlalchemy.sql import func
from database import Base
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class Identity(Base):
    __tablename__ = "identities"

    id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String, nullable=False, index=True)
    aliases = Column(JSON, default=list)
    email = Column(String, nullable=True)
    pgp_fingerprint = Column(String, nullable=True, index=True)
    crypto_wallets = Column(JSON, default=list)
    platform = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    writing_samples = Column(JSON, default=list)
    posting_hours = Column(JSON, default=list)
    categories = Column(JSON, default=list)
    extra_metadata = Column(JSON, default=dict)
    source_id = Column(String, nullable=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
