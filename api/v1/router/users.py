from typing import List 

from fastapi import APIRouter, Depends
from fastapi_pagination import Page

from schemas.users import UserIn, UserOut, UserUpdate, UsersParams, MultiUserOut
from controller.users import UserController
from schemas.common import DelResponse




users_router = APIRouter()


@users_router.post("/users", response_model=UserOut)
def onboard_users(user: UserIn) -> dict:
    """Onboard Users
    This method onboards users in a company
    """
    user = UserController.create_user(user.__dict__)
    return user


@users_router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    """Get User
    This method gets a user
    """
    user = UserController.get_user(user_id)
    return user


@users_router.get("/users", response_model=Page[MultiUserOut])
def get_users(users_params: UsersParams = Depends()):
    """Get Users
    This method gets all users
    """
    users = UserController.get_users(users_params)
    return users


@users_router.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, user: UserUpdate):
    """Update User
    This method updates a user
    """
    user = UserController.update_user(user_id, user.__dict__)
    return user

@users_router.delete("/users/{user_id}", response_model=DelResponse)
def delete_user(user_id: int, created_by_id: int):
    """Delete User
    This method deletes a user
    """
    user = UserController.delete_user(user_id, created_by_id)
    return user




@users_router.delete("/users/deactivate/{user_id}", response_model=DelResponse)
def deactivate_user(user_id: int, created_by_id: int):
    """Deactivate User
    This method deactivates a user
    """
    user = UserController.deactivate_user(user_id, created_by_id)
    return user