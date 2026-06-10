from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_pool, close_pool
from routers import webhook

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_pool()
    yield
    await close_pool()

app = FastAPI(
    title="Asistente Bot - Orientación Consular",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(webhook.router)

@app.get("/health")
async def health():
    return {"status": "ok"}
