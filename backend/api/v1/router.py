from fastapi import APIRouter

from backend.api.v1.endpoints import agents, citations, comments, papers, search, users

router = APIRouter()

router.include_router(agents.router, prefix="/agents", tags=["agents"])
router.include_router(papers.router, prefix="/papers", tags=["papers"])
router.include_router(citations.router, prefix="/citations", tags=["citations"])
router.include_router(comments.router, prefix="/comments", tags=["comments"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(search.router, prefix="/search", tags=["search"])
