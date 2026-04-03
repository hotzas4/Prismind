import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from backend.core.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    paper_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("papers.id"), nullable=False, index=True
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True
    )
    agent_reply: Mapped[str | None] = mapped_column(Text, nullable=True)
    agent_replied_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_flagged: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    paper: Mapped["Paper"] = relationship("Paper", back_populates="comments")  # type: ignore[name-defined]  # noqa: F821
    user: Mapped["User | None"] = relationship("User", back_populates="comments")  # type: ignore[name-defined]  # noqa: F821
