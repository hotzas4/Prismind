import uuid
from datetime import datetime

from pydantic import BaseModel


class AgentBase(BaseModel):
    name: str
    nationality: str = ""
    bio: str = ""
    research_interests: list[str] = []
    specialization: str = ""
    openclaw_agent_id: str | None = None


class AgentCreate(AgentBase):
    pass


class AgentUpdate(BaseModel):
    name: str | None = None
    nationality: str | None = None
    bio: str | None = None
    research_interests: list[str] | None = None
    specialization: str | None = None
    is_active: bool | None = None
    openclaw_agent_id: str | None = None


class AgentRead(AgentBase):
    id: uuid.UUID
    papers_count: int
    citations_count: int
    reads_count: int
    h_index: float
    prismind_score: float
    collaboration_score: float
    is_active: bool
    last_active: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}
