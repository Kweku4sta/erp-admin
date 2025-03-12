from enum import Enum
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field
from fastapi import UploadFile, File
from schemas.documents import DocumentOut


class Status(str, Enum):
    new = 'new'
    verified = 'verified'
    deactivated = 'deactivated'


class Title(str, Enum):
  mr = "Mr"
  mrs = "Mrs"
  miss = "Miss"
  dr = "Dr"
  prof = "Prof"
  sir = "Sir"
  lady = "Lady"
  lord = "Lord"
  rev = "Rev"


class Document(BaseModel, use_enum_values=True):
    document_type: str = Field(..., max_length=100)
    document: UploadFile 
    


class UserIn(BaseModel):
    full_name: str =Field(..., description="Full name of the user", examples=["John Doe"])
    email: EmailStr = Field(..., description="Email of the user")
    company_id: int = Field(..., description="Company ID of the user")
    is_authorizer: bool = Field(..., description="Is the user an authorizer", examples=[False, True])
    created_by_id: int = Field(..., description="ID of the admin creating the user", examples=[1, 2])
    title: Optional[Title] = Field(None, description="Title of the user")
    job_position: Optional[str] = Field(None, description="Job position of the user", examples=["Software Engineer", "Data Analyst"])
    is_transact_portal_user: bool = Field(False, description="Is the user a transact portal user")




class CreatedBy(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    role_id: int
    created_at: datetime


class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    company_id: int
    is_authorizer: bool
    flag: bool
    created_at: datetime
    updated_at: datetime
    company: Optional[str] = None
    is_transact_portal_user: Optional[bool]
    title: Optional[Title] = None
    job_position: Optional[str] = None
    active: bool
    created_by: CreatedBy
    documents: Optional[DocumentOut] = None



# class UsersParams(BaseModel):
#     page: Optional[int] = Field(1, description="The page number")
#     size: Optional[int] = Field(10, description="The number of items per page")


class UsersParams(BaseModel):
    size: int = Field(50, title="Page", description="Page number to return", examples=[1, 2])
    page: Optional[int] = Field(1, description="The page number")
    name: Optional[str] = Field(None, description="The name of the user")
    email: Optional[str] = Field(None, description="The email of the user")
    company_id: Optional[int] = Field(None, description="The company ID of the user")
    is_authorizer: Optional[bool] = Field(None, description="Is the user an authorizer")
    active: Optional[bool] = Field(None, description="Is the user active")
    flag: Optional[bool] = Field(None, description="Flag for the user")
    is_transact_portal_user: Optional[bool] = Field(None, description="Has portal access")


class MultiCreatedBy(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role_id: int
    created_at: datetime



class MultiUserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    company_id: int
    is_authorizer: bool
    flag: bool
    created_at: datetime
    updated_at: datetime
    is_transact_portal_user: Optional[bool]
    active: bool
    created_by: MultiCreatedBy
    documents: Optional[DocumentOut] = None






class UserUpdate(BaseModel):
    full_name: Optional[str] =Field(None, description="Full name of the user", examples=["John Doe"])
    email: Optional[EmailStr] = Field(None, description="Email of the user")
    company_id: Optional[int] = Field(None, description="Company ID of the user")
    is_authorizer: Optional[bool] = Field(None, description="Is the user an authorizer", examples=[False, True])
    flag: Optional[bool] = Field(None, description="Flag for the user")
    is_transact_portal_user: Optional[bool] = Field(None, description="Has portal access")
    active: Optional[bool] = Field(None, description="Is the user active")
    created_by_id: int = Field(..., description="ID of the admin updating the user", examples=[1, 2])



    
    
