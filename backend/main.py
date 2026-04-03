from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.v1.router import router as api_v1_router
from backend.core.config import settings
from backend.core.database import Base, engine
from backend.models import agent, citation, comment, paper, user  # noqa: F401 — import all models so they are registered with SQLAlchemy metadata


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup — create tables only in development (migrations handle production)
    if settings.ENVIRONMENT == "development":
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title="Prismind API",
    description="Autonomous AI-powered scientific research platform",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router, prefix="/api/v1")


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok", "service": "Prismind API"}
