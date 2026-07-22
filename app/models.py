from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.database import Base


class ResponseSource(Base):
    __tablename__ = "response_sources"

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_name = Column(String(255), nullable=False, index=True)
    prompt = Column(Text, nullable=True)
    raw_text = Column(Text, nullable=False)
    claim_count = Column(Integer, default=0)
    verified_count = Column(Integer, default=0)
    false_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    claims = relationship("Claim", back_populates="source", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_sources_model_created", "model_name", "created_at"),
    )


class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(Integer, ForeignKey("response_sources.id", ondelete="SET NULL"), nullable=True, index=True)
    claim_text = Column(Text, nullable=False)
    status = Column(String(50), nullable=False, default="unreviewed", index=True)
    confidence = Column(Float, nullable=True)
    verification_method = Column(String(100), nullable=True)
    source_url = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    source = relationship("ResponseSource", back_populates="claims")
    audits = relationship("ClaimAudit", back_populates="claim", cascade="all, delete-orphan", order_by="ClaimAudit.changed_at")

    __table_args__ = (
        Index("ix_claims_status_created", "status", "created_at"),
        Index("ix_claims_source_status", "source_id", "status"),
    )


class ClaimAudit(Base):
    __tablename__ = "claim_audits"

    id = Column(Integer, primary_key=True, autoincrement=True)
    claim_id = Column(Integer, ForeignKey("claims.id", ondelete="CASCADE"), nullable=False, index=True)
    old_status = Column(String(50), nullable=False)
    new_status = Column(String(50), nullable=False)
    changed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    claim = relationship("Claim", back_populates="audits")
