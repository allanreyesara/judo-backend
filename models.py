from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    username: str
    full_name: str
    password: Optional[str] = None
    email: str

class Login(BaseModel):
    username: str
    password: str

class Session(BaseModel):
    session_id: str
    user_id: str
    created_at: datetime
    finished_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str