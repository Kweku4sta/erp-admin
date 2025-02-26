from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from fastapi import UploadFile, File


class Status(str, Enum):
    new = 'new'
    verified = 'verified'
    deactivated = 'deactivated'


class Document(BaseModel, use_enum_values=True):
    document_type: str = Field(..., max_length=100)
    document: UploadFile 
    


class UserIn(BaseModel):
    full_name: str =Field(..., description="Full name of the user", examples=["John Doe"])
    email: EmailStr = Field(..., description="Email of the user")
    password: str = Field(..., description="Password of the user", min_length=8)
    company_id: int = Field(..., description="Company ID of the user")
    is_authorizer: bool = Field(..., description="Is the user an authorizer", examples=[False, True])
