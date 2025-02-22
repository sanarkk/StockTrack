import asyncio
from uvicorn import run
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.user_routes import router as user_router
from api.chatbot_routes import router as bot_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(bot_router)
