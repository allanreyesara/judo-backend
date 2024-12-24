import datetime
import uuid
from email.header import Header
from random import randint, random
from typing import List, Annotated

from bson import ObjectId
from fastapi import HTTPException
from passlib.context import CryptContext

from infrastructure.mongo_repository import user_collection, session_collection
from models import User, Login, Session, UserWithSession

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def retrieve_users() -> List[User]:
    users = [User(username=user["username"], email=user["email"], full_name=user["full_name"])
             for user in user_collection.find()]
    return users

def get_logged_in_user(user_id):
    user_collection.find_one({"_id": ObjectId(user_id)})



def log_user(login: Login) -> UserWithSession:
    existing_user = user_collection.find_one({"username": login.username})
    if not existing_user:
        raise HTTPException(status_code=400, detail="User not found")
    if not verify_password(login.password, existing_user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect password.")
    user = User(id=str(existing_user["_id"]),username=existing_user["username"], email=existing_user["email"], full_name=existing_user["full_name"])
    session_id = generate_session(user)
    userwithsession = UserWithSession(id=str(existing_user["_id"]),username=existing_user["username"], email=existing_user["email"], full_name=existing_user["full_name"], session_id=session_id)
    return userwithsession

def generate_session(user) -> str:
    session = Session(
        session_id=str(uuid.uuid4()), user_id=user.id,
        created_at= datetime.datetime.now(), updated_at= datetime.datetime.now())
    session_collection.insert_one(dict(session))
    return session.session_id


def touch_session(session_id):
    session  = session_collection.find_one({"session_id": session_id})
    if session["updated_at"] < datetime.datetime.now()- datetime.timedelta(minutes=10):
        session["finished_at"] = session["updated_at"]
    else:
        session["updated_at"] = datetime.datetime.now()
    session_collection.update(session)


