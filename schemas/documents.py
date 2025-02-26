from typing import Optional, Annotated
from enum import Enum

from pydantic import BaseModel, EmailStr, Field
from fastapi import UploadFile, File, Form, Body


class DocumentType(str, Enum):
    passport = 'passport'
    national_id = 'national_id'
    driver_license = 'driver_license'
    voter_id = 'voter_id'
    ghana_card = 'ghana_card'
    utility_bill = 'utility_bill'

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




