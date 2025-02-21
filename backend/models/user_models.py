from typing import List
from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    password: str
    date: datetime
    chat_id: str
    interested_in: List[str]


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: str
    chat_id: str

    class Config:
        orm_mode = True
