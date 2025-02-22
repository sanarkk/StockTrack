import uuid

from typing import Dict
from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from config import SECRET_KEY
from database.dynamodb import users_table, stock_tickers_name
from models.user_models import UserCreate, User, LoginRequest
from services.user_services import get_user_by_username, create_user
from auth.auth import get_password_hash, verify_password, create_access_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=SECRET_KEY)


@router.post("/register/", response_model=User)
async def register_user(user: UserCreate):
    user_data = user.dict()
    is_registered = get_user_by_username(user_data["username"])
    if is_registered:
        raise HTTPException(
            status_code=409, detail="Current username is in use"
        )
    hashed_password = get_password_hash(user.password)
    user_data["password"] = hashed_password
    user_data["chat_id"] = "default_chat_id"
    user_data["date"] = user_data["date"].strftime("%Y-%m-%d %H:%M:%S")
    user_data["id"] = str(uuid.uuid4())
    create_user(user_data)
    return user_data


@router.post("/token/")
async def login_user(form_data: LoginRequest):
    user = get_user_by_username(form_data.username)
    print(user)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": form_data.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user["username"],
        "interested_in": user["interested_in"],
    }


@router.post("/search/")
async def find_stock(data: str):
    response = stock_tickers_name.scan(
        FilterExpression="begins_with(ticker, :data)",
        ExpressionAttributeValues={":data": data},
    )
    return response


@router.post("/stock_preferences/")
async def save_stock_preferences(username: str, data: list[str]):
    user = get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=401, detail="Account does not exist")
    update_response = users_table.update_item(
        Key={"user_id": user["user_id"]},  # Primary Key
        UpdateExpression="SET interested_in = :new_list",
        ExpressionAttributeValues={":new_list": data},
        ReturnValues="UPDATED_NEW",
    )
    return update_response


@router.get("/get_tickers/")
async def get_user_tickers(username: str):
    user = get_user_by_username(username)
    return user["interested_in"]
