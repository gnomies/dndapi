from fastapi import FastAPI
from .routers import characters

app = FastAPI()

app.include_router(characters.router, prefix="/api/v1", tags=["characters"])
