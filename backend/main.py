import asyncio
from uvicorn import run
from fastapi import FastAPI

from api.user_routes import router as user_router

app = FastAPI()

app.include_router(user_router)
