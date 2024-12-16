from http.client import HTTPException
from typing import List

from passlib.context import CryptContext
import logging


import re
from fastapi import APIRouter, HTTPException

from models.models import User, Login, Token
from config.mongo_repository import user_collection

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logging.getLogger('passlib').setLevel(logging.ERROR)

router = APIRouter()

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

#GET Request Method

@router.get("/v1/users")
async def get_users() -> List[User]:
    users = [User(username=user["username"], email=user["email"], full_name=user["full_name"])
             for user in user_collection.find()]
    return users

#POST Request Method

@router.post("/v1/users")
async def create_user(user: User):
    existing_user = user_collection.find_one({"username": user.username})
    email_pattern = r"^\S+@\S+\.\S+$"

    if not re.match(email_pattern, user.email):
        raise HTTPException(status_code=400, detail="Enter a valid email address.")
    if existing_user :
        raise HTTPException(status_code=400, detail="Username already exists")
    if len(user.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long.")

    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    user_collection.insert_one(dict(user))

@router.post("/v1/login")
async def login_user(login: Login) -> User:
    existing_user = user_collection.find_one({"username": login.username})
    if not existing_user:
        raise HTTPException(status_code=400, detail="User not found")
    if not verify_password(login.password, existing_user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect password.")
    user = User(username=existing_user["username"], email=existing_user["email"], full_name=existing_user["full_name"])
    return user
