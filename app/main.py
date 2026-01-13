from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1.api import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(title="Gemini SQL + Local LLaMA", lifespan=lifespan)
app.include_router(api_router)
