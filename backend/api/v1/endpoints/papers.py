import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models.citation import Citation
from models.paper import Paper, PaperStatus
from schemas.citation import CitationRead
from schemas.paper import PaperCreate, PaperRead, PaperUpdate

router = APIRouter()


@router.get("", response_model=list[PaperRead])
async def list_papers(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    field: str | None = Query(None),
    agent_id: uuid.UUID | None = Query(None),
    paper_status: PaperStatus | None = Query(None, alias="status"),
    db: AsyncSession = Depends(get_db),
):
    query = select(Paper)
    if field:
        query = query.where(Paper.field == field)
    if agent_id:
        query = query.where(Paper.agent_id == agent_id)
    if paper_status:
        query = query.where(Paper.status == paper_status)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{paper_id}", response_model=PaperRead)
async def get_paper(paper_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    paper = await db.get(Paper, paper_id)
    if not paper:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paper not found")
    paper.reads_count += 1
    await db.flush()
    await db.refresh(paper)
    return paper


@router.post("", response_model=PaperRead, status_code=status.HTTP_201_CREATED)
async def create_paper(payload: PaperCreate, db: AsyncSession = Depends(get_db)):
    paper = Paper(**payload.model_dump())
    db.add(paper)
    await db.flush()
    await db.refresh(paper)
    return paper


@router.patch("/{paper_id}", response_model=PaperRead)
async def update_paper(
    paper_id: uuid.UUID, payload: PaperUpdate, db: AsyncSession = Depends(get_db)
):
    paper = await db.get(Paper, paper_id)
    if not paper:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paper not found")
    updates = payload.model_dump(exclude_none=True)
    if "status" in updates and updates["status"] == PaperStatus.published and not paper.published_at:
        updates["published_at"] = datetime.now(timezone.utc)
    for field, value in updates.items():
        setattr(paper, field, value)
    await db.flush()
    await db.refresh(paper)
    return paper


@router.get("/{paper_id}/citations", response_model=list[CitationRead])
async def get_paper_citations(paper_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    paper = await db.get(Paper, paper_id)
    if not paper:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paper not found")
    result = await db.execute(
        select(Citation).where(Citation.cited_paper_id == paper_id)
    )
    return result.scalars().all()


@router.post("/{paper_id}/flag", response_model=PaperRead)
async def flag_paper(paper_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    paper = await db.get(Paper, paper_id)
    if not paper:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paper not found")
    paper.status = PaperStatus.flagged
    await db.flush()
    await db.refresh(paper)
    return paper
