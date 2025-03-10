
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from schemas.admins import AdminIn, AdminOut, RoleIn, RoleOut, AdminLogin, AdminLoginOut, UpdatePassword
from controller.admins import AdminController
from utils.auth import get_current_admin_and_role
from errors.exception import AuthException


admins_router = APIRouter()

# admins_router.dependencies = [Depends(get_current_admin_and_role)]


@admins_router.post("/admins", response_model=AdminOut)
def onboard_admins(admin: AdminIn, current_admin: dict = Depends(get_current_admin_and_role)) -> dict:
    """Onboard Users
    This method onboards admins in the remcash system
    """
    if current_admin['role'] in ['system_admin']:
        admin = AdminController.create_admin(admin.__dict__)
        return admin
    raise AuthException(code=400, msg="You are not authorized to perform this action")	
    admin = AdminController.create_admin(admin.__dict__)
    return admin



@admins_router.delete("/admins/{admin_id}")
def delete_admin(admin_id: int, current_admin: dict = Depends(get_current_admin_and_role)):
    """Delete User
    This method deletes a user
    """
    if current_admin['role'] in ['system_admin']:
        admin = AdminController.delete_admin(admin_id)
        return admin
    raise AuthException(code=400, msg="You are not authorized to perform this action")



@admins_router.get("/admins", response_model=list[AdminOut])
def get_all_admin():
    admins = AdminController.get_all_admins()
    return admins






@admins_router.post("/roles", response_model=RoleOut)
def add_role(role: RoleIn) -> dict:
    """Add Role
    This method adds a role
    """
    role = AdminController.add_role(role.__dict__)
    return role

@admins_router.put("/roles/{role_id}", response_model=RoleOut)
def update_role(role_id: int, role: RoleIn) -> dict:
    """Update Role
    This method updates a role
    """
    role = AdminController.update_role(role_id, role.__dict__)
    return role

@admins_router.get("/roles/{role_id}", response_model=RoleOut)
def get_role(role_id: int):
    """Get Role
    This method gets a role
    """
    role = AdminController.get_role_by_id(role_id)
    return role

@admins_router.get("/roles", response_model=List[RoleOut])
def get_roles():
    """Get Roles
    This method gets all roles
    """
    roles = AdminController.get_all_roles()
    return roles

@admins_router.delete("/roles/{role_id}")
def delete_role(role_id: int):
    """Delete Role
    This method deletes a role
    """
    admin = AdminController.delete_role(role_id)
    return admin




@admins_router.get("/admins/{admin_id}", response_model=AdminOut)
def get_admin(admin_id: int):
    """Get User
    This method gets a user
    """
    admin = AdminController.get_admin(admin_id)
    return admin


@admins_router.post("/login", response_model=AdminLoginOut)
def login(admin: AdminLogin):
    """Login
    This method logs in an admin
    """
    admin = AdminController.login(admin.__dict__)
    return admin


@admins_router.put("/admins/{admin_id}", response_model=AdminOut)
def update_admin_data(admin_id: int,data: AdminIn):
    return AdminController.update_admin(admin_id,data.__dict__)


@admins_router.put("/admin/password-reset/{admin_id}", response_model=AdminOut)
def reset_password(admin_id: int, data:UpdatePassword):
    return AdminController.reset_default_password(admin_id, data.__dict__)