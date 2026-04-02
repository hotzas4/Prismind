import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy import select

from core.database import AsyncSessionLocal
from models.agent import Agent
from models.paper import Paper, PaperStatus

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def _run_researcher_jobs() -> None:
    """Run researcher agent workflow for all active agents."""
    from agents.researcher import run_researcher_agent

    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Agent).where(Agent.is_active.is_(True)))
        agents = result.scalars().all()

    for agent in agents:
        try:
            logger.info("Running researcher agent: %s", agent.name)
            await run_researcher_agent(agent.id)
        except Exception:
            logger.exception("Researcher agent %s failed", agent.name)


async def _run_reviewer_jobs() -> None:
    """Run reviewer agent on papers that are under review."""
    from agents.reviewer import run_reviewer_agent

    async with AsyncSessionLocal() as db:
        papers_result = await db.execute(
            select(Paper).where(Paper.status == PaperStatus.under_review)
        )
        papers = papers_result.scalars().all()

        agents_result = await db.execute(select(Agent).where(Agent.is_active.is_(True)))
        agents = agents_result.scalars().all()

    if not agents:
        return

    reviewer = agents[0]  # Use the first active agent as reviewer for simplicity
    for paper in papers:
        if str(paper.agent_id) == str(reviewer.id):
            continue  # Skip self-review
        try:
            logger.info("Running reviewer agent on paper: %s", paper.title)
            await run_reviewer_agent(paper.id, reviewer.id)
        except Exception:
            logger.exception("Reviewer agent failed for paper %s", paper.id)


def start_scheduler() -> None:
    """Start the APScheduler with all scheduled jobs."""
    scheduler.add_job(
        _run_researcher_jobs,
        trigger=IntervalTrigger(hours=6),
        id="researcher_heartbeat",
        replace_existing=True,
        misfire_grace_time=300,
    )
    scheduler.add_job(
        _run_reviewer_jobs,
        trigger=IntervalTrigger(hours=2),
        id="reviewer_heartbeat",
        replace_existing=True,
        misfire_grace_time=300,
    )
    scheduler.start()
    logger.info("Prismind scheduler started — researcher every 6h, reviewer every 2h")


def stop_scheduler() -> None:
    """Gracefully stop the scheduler."""
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Prismind scheduler stopped")
