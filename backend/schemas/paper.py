import uuid
from datetime import datetime

from pydantic import BaseModel

from backend.models.paper import PaperStatus


class PaperBase(BaseModel):
    title: str
    abstract: str = ""
    introduction: str = ""
    methodology: str = ""
    results: str = ""
    discussion: str = ""
    conclusion: str = ""
    references: list[str] = []
    field: str = ""
    keywords: list[str] = []
    language: str = "en"
    language_english_translation: bool = False


class PaperCreate(PaperBase):
    agent_id: uuid.UUID


class PaperUpdate(BaseModel):
    title: str | None = None
    abstract: str | None = None
    introduction: str | None = None
    methodology: str | None = None
    results: str | None = None
    discussion: str | None = None
    conclusion: str | None = None
    references: list[str] | None = None
    field: str | None = None
    keywords: list[str] | None = None
    status: PaperStatus | None = None
    peer_reviewed: bool | None = None
    peer_review_notes: str | None = None
    confidence_score: float | None = None
    reproducibility_score: float | None = None


class PaperRead(PaperBase):
    id: uuid.UUID
    reads_count: int
    citations_count: int
    confidence_score: float
    peer_reviewed: bool
    peer_review_notes: str
    reproducibility_score: float
    status: PaperStatus
    agent_id: uuid.UUID
    created_at: datetime
    published_at: datetime | None

    model_config = {"from_attributes": True}
