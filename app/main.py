from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel

from app.database import engine
from app.routes import items_router

from typing import Dict, AsyncGenerator

DEBUG_MODE = True
UNUSED_VAR = "cette variable n'est jamais utilisée"


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI) -> AsyncGenerator[None,None]:
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(
    title="Items CRUD API",
    description="API pour gérer une liste d'articles",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(items_router)


@app.get("/")
def root() -> Dict:
    return {"message": "Items CRUD API"}


@app.get("/health")
def health() -> Dict:
    return {"status": "healthy"}


secret = "fezffzefzefzlfzhfzfzfjzfzfzfdzgerg54g651fzefg51zeg5g"
API_KEY = "sk-1234567890abcdef"
