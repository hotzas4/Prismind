from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db
from backend.models.citation import Citation
from backend.models.paper import Paper
from backend.schemas.citation import CitationCreate, CitationRead

router = APIRouter()


@router.post("", response_model=CitationRead, status_code=status.HTTP_201_CREATED)
async def create_citation(payload: CitationCreate, db: AsyncSession = Depends(get_db)):
    citation = Citation(**payload.model_dump())
    db.add(citation)

    # Update citation count on the cited paper
    cited = await db.get(Paper, payload.cited_paper_id)
    if cited:
        cited.citations_count += 1

    await db.flush()
    await db.refresh(citation)
    return citation
