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
    index_key: int
    parsing_date: str


@router.post("/send_message/")
async def send_message_to_user(
    article: Article | None,
):
    users = users_table.scan(ConsistentRead=True)
    users_db = users.get("Items", [])
    for user in users_db:
        data = {
            "chat_id": user["chat_id"],
            "article": {
                "url": "https://markets.businessinsider.com/news/stocks/kepler-capital-keeps-their-buy-rating-on-imi-plc-imi-1034394075",
                "title": "Kepler Capital  Keeps Their Buy Rating on IMI plc (IMI)",
                "publish_date": "2025-02-21T19:37:00",
                "article_text": "Kepler Capital  analyst   maintained a Buy rating on IMI plc (  \u2013  ) on February 20 and set a price target of p2,290.00. The company\u2019s shares closed yesterday at p1,906.00. According to  , Jones is a 5-star analyst with an average return of   and a 78.72% success rate. The word on The Street in general, suggests a Strong Buy analyst consensus rating for IMI plc with a p2,265.00 average price target.\n\t\t Based on IMI plc\u2019s latest earnings release for the quarter ending June 30, the company reported a quarterly revenue of p1.1 billion and a net profit of p125.3 million. In comparison, last year the company earned a revenue of p1.08 billion and had a net profit of p109.3 million Based on the recent corporate insider activity of 18 insiders, corporate insider sentiment is positive on the stock. This means that over the past quarter there has been an increase of insiders buying their shares of IMI in relation to earlier this year.",
                "stock_ticker": "IMIAF",
                "news_source": "TipRanks",
                "index_key": 2,
                "parsing_date": "2025-02-22T15:11:59.909677",
            },
        }
        response = requests.post(
            "http://127.0.0.1:8004/send_telegram_message/",
            json=data,
        )
        try:
            if user["chat_id"] != "":
                for item in user["interested_in"]:
                    is_same = False
                    if isinstance(item, dict):
                        if item["ticker"] == article.stock_ticker:
                            is_same = True
                    else:
                        if item == article.stock_ticker:
                            is_same = True
                    if is_same:
                        data = {
                            "chat_id": user["chat_id"],
                            "article": {
                                "url": "https://markets.businessinsider.com/news/stocks/kepler-capital-keeps-their-buy-rating-on-imi-plc-imi-1034394075",
                                "title": "Kepler Capital  Keeps Their Buy Rating on IMI plc (IMI)",
                                "publish_date": "2025-02-21T19:37:00",
                                "article_text": "Kepler Capital  analyst   maintained a Buy rating on IMI plc (  \u2013  ) on February 20 and set a price target of p2,290.00. The company\u2019s shares closed yesterday at p1,906.00. According to  , Jones is a 5-star analyst with an average return of   and a 78.72% success rate. The word on The Street in general, suggests a Strong Buy analyst consensus rating for IMI plc with a p2,265.00 average price target.\n\t\t Based on IMI plc\u2019s latest earnings release for the quarter ending June 30, the company reported a quarterly revenue of p1.1 billion and a net profit of p125.3 million. In comparison, last year the company earned a revenue of p1.08 billion and had a net profit of p109.3 million Based on the recent corporate insider activity of 18 insiders, corporate insider sentiment is positive on the stock. This means that over the past quarter there has been an increase of insiders buying their shares of IMI in relation to earlier this year.",
                                "stock_ticker": "IMIAF",
                                "news_source": "TipRanks",
                                "index_key": 2,
                                "parsing_date": "2025-02-22T15:11:59.909677",
                            },
                        }
                        response = requests.post(
                            "http://127.0.0.1:8004/send_telegram_message/",
                            json=data,
                        )
                        return "Message was sent"
        except KeyError as e:
            pass
    return "User does not have chat assigned"
