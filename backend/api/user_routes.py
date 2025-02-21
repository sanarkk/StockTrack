import uuid

from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from config import SECRET_KEY
from database.dynamodb import users_table
from models.user_models import UserCreate, User
from services.user_services import get_user_by_username, create_user
from auth.auth import get_password_hash, verify_password, create_access_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=SECRET_KEY)


@router.post("/register/", response_model=User)
async def register_user(user: UserCreate):
    hashed_password = get_password_hash(user.password)
    user_data = user.dict()
    user_data["password"] = hashed_password
    user_data["chat_id"] = "default_chat_id"
    user_data["date"] = user_data["date"].strftime("%Y-%m-%d %H:%M:%S")
    user_data["id"] = str(uuid.uuid4())
    create_user(user_data)
    return user_data


@router.post("/token/")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/search/")
async def find_stock(data: str):
    response = users_table.scan(
        FilterExpression="contains(username, :data)",
        ExpressionAttributeValues={":data": data},
    )
    return response
