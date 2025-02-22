import uuid
import requests

from typing import Dict
from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from config import SECRET_KEY
from services.token import verify_token, get_current_user
from database.dynamodb import users_table, stock_tickers_name, articles_table
from models.user_models import UserCreate, User, LoginRequest
from services.user_services import get_user_by_username, create_user
from auth.auth import get_password_hash, verify_password, create_access_token


router = APIRouter()


class Article(BaseModel):
    url: str
    title: str
    publish_date: str
    article_text: str
    stock_ticker: str
    news_source: str
    index_key: str
    parsing_date: str


@router.post("/send_message/")
async def send_message_to_user(
    article: Article,
):
    print("here1")

    users = users_table.scan(ConsistentRead=True)
    users_db = users.get("Items", [])
    for user in users_db:
        print("here1")
        try:
            print("here2")
            if user["chat_id"] != "":
                print("here3")
                for item in user["interested_in"]:
                    print(user["interested_in"])
                    print(item)
                    is_same = False
                    if isinstance(item, dict):
                        print("INSIDE USER DICT")
                        if item["ticker"] == article.stock_ticker:
                            is_same = True
                    else:
                        print("NOT INSIDE")
                        if item == article.stock_ticker:
                            is_same = True
                    if is_same:
                        data = {
                            "chat_id": user["chat_id"],
                            "article": article.dict(),
                        }
                        print("before response")
                        response = requests.post(
                            "http://127.0.0.1:8004/send_telegram_message/",
                            json=data,
                        )
                        return "Message was sent"
        except KeyError as e:
            pass
    return "User does not have chat assigned"
