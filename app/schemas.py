from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ClaimCreate(BaseModel):
    source_id: Optional[int] = None
    claim_text: str


class ClaimStatusUpdate(BaseModel):
    status: str
    source_url: Optional[str] = None
    notes: Optional[str] = None


class ExtractRequest(BaseModel):
    raw_text: str
    model_name: str
    prompt: Optional[str] = None


class ClaimOut(BaseModel):
    id: int
    source_id: Optional[int]
    claim_text: str
    status: str
    source_url: Optional[str]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    model_name: Optional[str] = None

    model_config = {"from_attributes": True}


class ClaimsResponse(BaseModel):
    claims: list[ClaimOut]
    total: int
    page: int
    per_page: int


class StatsResponse(BaseModel):
    total: int
    verified: int
    doubtful: int
    false_count: int
    unreviewed: int
    by_model: dict


class SourceOut(BaseModel):
    id: int
    model_name: str
    prompt: Optional[str]
    raw_text: str
    created_at: datetime

    model_config = {"from_attributes": True}


class SourceCreate(BaseModel):
    model_name: str
    prompt: Optional[str] = None
    raw_text: str
