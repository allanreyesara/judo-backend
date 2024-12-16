from models.models import User


def list_serial(user) -> list:
    return [User(id =str(user["_id"]), username=user["username"], email=user["email"], full_name=user["full_name"]) for user in user]