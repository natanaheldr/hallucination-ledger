from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

VALID_STATUSES = {"unreviewed", "verified", "doubtful", "false"}
VALID_VERIFICATION_METHODS = {"manual", "web_search", "expert_review", "cross_reference", "automated"}


class ClaimCreate(BaseModel):
    source_id: Optional[int] = None
    claim_text: str = Field(..., min_length=5, max_length=2000)
    notes: Optional[str] = Field(None, max_length=5000)

    @field_validator("claim_text")
    @classmethod
    def claim_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("A claim cannot be empty.")
        return v.strip()


class ClaimStatusUpdate(BaseModel):
    status: str = Field(...)
    source_url: Optional[str] = Field(None, max_length=2000)
    notes: Optional[str] = Field(None, max_length=5000)
    verification_method: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        if v not in VALID_STATUSES:
            raise ValueError(f"Invalid status. Choose from: {', '.join(sorted(VALID_STATUSES))}")
        return v


class BulkStatusUpdate(BaseModel):
    claim_ids: list[int] = Field(..., min_length=1, max_length=500)
    status: str = Field(...)

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        if v not in VALID_STATUSES:
            raise ValueError(f"Invalid status. Choose from: {', '.join(sorted(VALID_STATUSES))}")
        return v


class ExtractRequest(BaseModel):
    raw_text: str = Field(..., min_length=10, max_length=50000)
    model_name: str = Field(..., min_length=1, max_length=255)
    prompt: Optional[str] = Field(None, max_length=10000)

    @field_validator("model_name")
    @classmethod
    def model_name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Model name cannot be empty.")
        return v.strip()


class ClaimOut(BaseModel):
    id: int
    source_id: Optional[int]
    claim_text: str
    status: str
    confidence: Optional[float] = None
    verification_method: Optional[str] = None
    source_url: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    model_name: Optional[str] = None

    model_config = {"from_attributes": True}


class ClaimDetailOut(ClaimOut):
    audit_count: int = 0
    audits: list["AuditOut"] = []


class ClaimsResponse(BaseModel):
    claims: list[ClaimOut]
    total: int
    page: int
    per_page: int
    total_pages: int


class StatsResponse(BaseModel):
    total: int
    verified: int
    doubtful: int
    false_count: int
    unreviewed: int
    verified_pct: float
    false_pct: float
    by_model: dict = {}


class SourceOut(BaseModel):
    id: int
    model_name: str
    prompt: Optional[str]
    raw_text: str
    claim_count: int
    verified_count: int
    false_count: int
    created_at: datetime

    model_config = {"from_attributes": True}


class SourceCreate(BaseModel):
    model_name: str = Field(..., min_length=1, max_length=255)
    prompt: Optional[str] = Field(None, max_length=10000)
    raw_text: str = Field(..., min_length=10, max_length=50000)


class AuditOut(BaseModel):
    id: int
    claim_id: int
    old_status: str
    new_status: str
    changed_at: datetime

    model_config = {"from_attributes": True}


class BulkExtractResponse(BaseModel):
    source_id: int
    claims_extracted: int
    claims: list[ClaimOut]
