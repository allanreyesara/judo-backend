from typing import List

from fastapi import HTTPException
from passlib.context import CryptContext

from infrastructure.mongo_repository import user_collection
from models import User, Login



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def retrieve_users() -> List[User]:
    users = [User(username=user["username"], email=user["email"], full_name=user["full_name"])
             for user in user_collection.find()]
    return users

def log_user(login: Login) -> User:
    existing_user = user_collection.find_one({"username": login.username})
    if not existing_user:
        raise HTTPException(status_code=400, detail="User not found")
    if not verify_password(login.password, existing_user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect password.")
    user = User(username=existing_user["username"], email=existing_user["email"], full_name=existing_user["full_name"])

    return user


