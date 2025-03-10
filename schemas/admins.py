from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr, validator




class AdminIn(BaseModel):
    full_name: str = Field(..., title="Name", description="Name of the admin", examples=["John Doe", "Jane Doe"])
    email: EmailStr = Field(..., title="Email", description="Email of the admin")
    # password: str = Field(..., title="Password", description="Password of the admin", min_length=8)
    role_id: int = Field(..., title="Role ID", description="ID of the role", examples=[1, 2])


    # @validator('password')
    # def password_must_contain_upper(cls, v):
    #     if len(v) < 8 or not any(char.isupper() for char in v):
    #         raise ValueError('Password must contain at least 1 uppercase letter and be at least 8 characters')
    #     return v
    

class RoleIn(BaseModel):
    name: str = Field(..., title="Name", description="Name of the role", examples=["Admin", "User"])
    description: Optional[str] = Field(None, title="Description", description="Description of the role", examples=["Admin role", "User role"])


class RoleOut(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime




class AdminOut(BaseModel):
    id: int
    full_name: str
    email: str
    role_id: int
    created_at: datetime
    updated_at: datetime
    role: str
    reset_password: Optional[bool]


class AdminLogin(BaseModel):
    email: EmailStr = Field(..., title="Email", description="Email of the admin")
    password: str = Field(..., title="Password", description="Password of the admin", min_length=8)
    
    # @validator('password')
    # def password_must_contain_upper(cls, v):
    #     if len(v) < 8 or not any(char.isupper() for char in v):
    #         raise ValueError('Password must contain at least 1 uppercase letter and be at least 8 characters')
    #     return v

class AdminLoginOut(BaseModel):
    token: str
    admin: AdminOut



class AdminUpdateIn(BaseModel):
    full_name: str = Field(..., description="the full name of the user to be updated")
    email: EmailStr


class UpdatePassword(BaseModel):
    password: str