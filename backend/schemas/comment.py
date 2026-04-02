import uuid
from datetime import datetime

from pydantic import BaseModel


class CommentCreate(BaseModel):
    content: str
    paper_id: uuid.UUID
    user_id: uuid.UUID | None = None


class CommentRead(CommentCreate):
    id: uuid.UUID
    agent_reply: str | None
    agent_replied_at: datetime | None
    is_flagged: bool
    created_at: datetime

    model_config = {"from_attributes": True}
