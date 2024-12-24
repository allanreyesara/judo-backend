from email.header import Header
from http.client import HTTPException
from random import randint
from typing import List, Annotated

from bson import ObjectId

from controllers.user_manager import retrieve_users, get_password_hash, verify_password, log_user, touch_session, \
    get_logged_in_user

import logging


import re
from fastapi import APIRouter, HTTPException

from models import User, Login, UserWithSession
from infrastructure.mongo_repository import user_collection, session_collection

router = APIRouter()


#GET Request Method
@router.get("/v1/users")
async def get_users() -> List[User]:
    users = retrieve_users()
    return users

#GET Me
@router.get("/v1/getMe")
async def get_me(session_id: Annotated[str | None, Header()]= None):
    session = session_collection.find_one({"_id": ObjectId(session_id)})
    if not session:
        raise HTTPException(status_code=404, detail="User not authenticated")
    get_logged_in_user(session.user_id)


#POST Request Method
@router.post("/v1/signup")
async def create_user(user: User)->User:
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
    return user

@router.post("/v1/login")
async def login_user(login: Login) -> UserWithSession:
    return log_user(login)
