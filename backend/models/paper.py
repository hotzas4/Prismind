import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from backend.core.database import Base

import enum


class PaperStatus(str, enum.Enum):
    draft = "draft"
    under_review = "under_review"
    published = "published"
    flagged = "flagged"


class Paper(Base):
    __tablename__ = "papers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    abstract: Mapped[str] = mapped_column(Text, nullable=False, default="")
    introduction: Mapped[str] = mapped_column(Text, nullable=False, default="")
    methodology: Mapped[str] = mapped_column(Text, nullable=False, default="")
    results: Mapped[str] = mapped_column(Text, nullable=False, default="")
    discussion: Mapped[str] = mapped_column(Text, nullable=False, default="")
    conclusion: Mapped[str] = mapped_column(Text, nullable=False, default="")
    references: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    field: Mapped[str] = mapped_column(String(255), nullable=False, default="", index=True)
    keywords: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    language: Mapped[str] = mapped_column(String(50), nullable=False, default="en")
    language_english_translation: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    reads_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0, index=True)
    citations_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0, index=True)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    peer_reviewed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    peer_review_notes: Mapped[str] = mapped_column(Text, nullable=False, default="")
    reproducibility_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    status: Mapped[PaperStatus] = mapped_column(
        Enum(PaperStatus), nullable=False, default=PaperStatus.draft, index=True
    )
    agent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("agents.id"), nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    agent: Mapped["Agent"] = relationship("Agent", back_populates="papers")  # type: ignore[name-defined]  # noqa: F821
    citations_received: Mapped[list["Citation"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "Citation", foreign_keys="Citation.cited_paper_id", back_populates="cited_paper"
    )
    citations_made: Mapped[list["Citation"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "Citation", foreign_keys="Citation.citing_paper_id", back_populates="citing_paper"
    )
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="paper")  # type: ignore[name-defined]  # noqa: F821
