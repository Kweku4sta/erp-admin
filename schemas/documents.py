from typing import Optional, Annotated
from enum import Enum

from pydantic import BaseModel, EmailStr, Field
from fastapi import UploadFile, File, Form, Body


class CreatorCompany(BaseModel):
    name: str
    id: int



class Creator (BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    role_id: int
    # company: str
    # company_id: int
    # company: CreatorCompany


class DocumentType(str, Enum):
    ghana_card = 'ghana_card'

class TestDocument(BaseModel):
    name: str
    email: str

class DocumentIn(BaseModel):
    document_type: Annotated[DocumentType, Form()]
    testdocument: TestDocument
    document: UploadFile = Annotated[File(..., title="Document", description="Document to be uploaded"), Form()]

    @classmethod
    def as_form(cls, document_type, document) -> "DocumentIn":	
        return cls(document_type=document_type, document=document)
    

class Status(str, Enum):
    new = 'new'
    verified = 'verified'
    deactivated = 'deactivated'

class VerifyBy(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    role_id: int



class DocumentOut(BaseModel):
    id: int
    document_type: DocumentType
    status: Status
    s3_key: str
    document_url: str
    created_by: Creator
    company_id: Optional[int]
    user_id: Optional[int]
    verified_by: Optional[VerifyBy]


class VerifyDocument(BaseModel, use_enum_values=True):
    verifier_id: int = Field(..., title="Verifier ID", description="ID of the user verifying the document")
    status: Status = Field(..., title="Status", description="Status of the document")



class PresignedUrl(BaseModel):
    presigned_url: str
    s3_key: str


class DocumentParams(BaseModel):
    page: Optional[int] = Field(1, title="Page", description="Page number")
    size: Optional[int] = Field(50, title="Page Size", description="Number of items per page")
    company_id: Optional[int] = Field(None, title="Company ID", description="ID of the company")
    user_id: Optional[int] = Field(None, title="User ID", description="ID of the user")
    created_by_id: Optional[int] = Field(None, title="Creator ID", description="ID of the admin creating the document")
    document_type: Optional[DocumentType] = Field(None, title="Document Type", description="Type of the document")
    status: Optional[Status] = Field(None, title="Status", description="Status of the document")
    verifier_id: Optional[int] = Field(None, title="Verifier ID", description="ID of the user verifying the document")


    