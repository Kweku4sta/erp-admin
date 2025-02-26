from typing import List 

from fastapi import APIRouter

from schemas.users import UserIn
from controller.users import UserController


users_router = APIRouter()


@users_router.post("/users")
def onboard_users(user: UserIn) -> dict:
    """Onboard Users
    This method onboards users in a company
    """
    user = UserController.create_user(user.__dict__)
    return user