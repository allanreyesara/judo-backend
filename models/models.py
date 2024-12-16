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

class Token(BaseModel):
    access_token: str
    token_type: str