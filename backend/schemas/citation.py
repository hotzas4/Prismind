import uuid
from datetime import datetime

from pydantic import BaseModel


class CitationCreate(BaseModel):
    citing_paper_id: uuid.UUID
    cited_paper_id: uuid.UUID


class CitationRead(CitationCreate):
    id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}
