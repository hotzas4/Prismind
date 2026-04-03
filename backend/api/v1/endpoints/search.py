from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db
from backend.models.agent import Agent
from backend.models.paper import Paper
from backend.schemas.agent import AgentRead
from backend.schemas.paper import PaperRead

router = APIRouter()


class SearchResults:
    def __init__(self, papers: list, agents: list):
        self.papers = papers
        self.agents = agents


@router.get("")
async def search(
    q: str = Query(..., min_length=1, description="Search query"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Keyword search across papers (title, abstract, field) and agents (name, bio, specialization)."""
    search_term = f"%{q}%"

    papers_result = await db.execute(
        select(Paper)
        .where(
            or_(
                Paper.title.ilike(search_term),
                Paper.abstract.ilike(search_term),
                Paper.field.ilike(search_term),
            )
        )
        .offset(skip)
        .limit(limit)
    )
    papers = papers_result.scalars().all()

    agents_result = await db.execute(
        select(Agent)
        .where(
            or_(
                Agent.name.ilike(search_term),
                Agent.bio.ilike(search_term),
                Agent.specialization.ilike(search_term),
            )
        )
        .limit(limit)
    )
    agents = agents_result.scalars().all()

    return {
        "query": q,
        "papers": [PaperRead.model_validate(p) for p in papers],
        "agents": [AgentRead.model_validate(a) for a in agents],
        "total_papers": len(papers),
        "total_agents": len(agents),
    }
