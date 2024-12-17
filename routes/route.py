from http.client import HTTPException
from typing import List
from controllers.user_manager import retrieve_users, get_password_hash, verify_password, log_user

import logging


import re
from fastapi import APIRouter, HTTPException

from models import User, Login
from infrastructure.mongo_repository import user_collection

router = APIRouter()


#GET Request Method
@router.get("/v1/users")
async def get_users() -> List[User]:
    users = retrieve_users()
    return users

#POST Request Method

@router.post("/v1/users")
async def create_user(user: User)->None:
    existing_user = user_collection.find_one({"username": user.username})
    email_pattern = r"^\S+@\S+\.\S+$"

    if not re.match(email_pattern, user.email):
        raise HTTPException(status_code=400, detail="Enter a valid email address.")
    if existing_user :
        raise HTTPException(status_code=400, detail="Username already exists")
    if len(user.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long.")

    user.password = get_password_hash(user.password)
    user_collection.insert_one(dict(user))

@router.post("/v1/login")
async def login_user(login: Login) -> User:
    return log_user(login)
