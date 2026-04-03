from fastapi import FastAPI
from backend.api.router import api_router

app = FastAPI(title="Prismind API", version="0.2.0")
app.include_router(api_router)
