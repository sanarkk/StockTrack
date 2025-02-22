import uuid
import requests

from typing import Dict
from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from config import SECRET_KEY,
from services.token import verify_token, get_current_user
from database.dynamodb import users_table, stock_tickers_name, articles_table
from models.user_models import UserCreate, User, LoginRequest
from services.user_services import get_user_by_username, create_user
from auth.auth import get_password_hash, verify_password, create_access_token


router = APIRouter()

@router.post("/send_message/")
async def login_user(
    article: dict,
    current_user: str = Depends(get_current_user)
):
    user = get_user_by_username(current_user)
    if user["chat_id"] != "":
        data = {
            "chat_id": user["chat_id"],
            "article": article
        }
        requests.post("http://0.0.0.0:8001/send_message/", data)
        return "Message was sent"
    return "User does not have chat assigned"
