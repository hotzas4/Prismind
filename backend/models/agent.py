import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from backend.core.database import Base


class Agent(Base):
    __tablename__ = "agents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    nationality: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    bio: Mapped[str] = mapped_column(Text, nullable=False, default="")
    research_interests: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    specialization: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    papers_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    citations_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    reads_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    h_index: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    prismind_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    collaboration_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    last_active: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    openclaw_agent_id: Mapped[str | None] = mapped_column(String(255), nullable=True, unique=True)

    papers: Mapped[list["Paper"]] = relationship("Paper", back_populates="agent")  # type: ignore[name-defined]  # noqa: F821
