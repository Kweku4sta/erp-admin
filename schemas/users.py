from enum import Enum
from typing import Optional
from datetime import datetime

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
    created_by_id: int = Field(..., description="ID of the admin creating the user", examples=[1, 2])


class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    # company_id: int
    is_authorizer: bool
    flag: bool
    created_at: datetime
    updated_at: datetime

class UserUpdate(BaseModel):
    full_name: Optional[str] =Field(None, description="Full name of the user", examples=["John Doe"])
    password: Optional[str] = Field(None, description="Password of the user", min_length=8)


    
    
