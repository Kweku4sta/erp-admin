from typing import List, Annotated, Optional

from fastapi import APIRouter, Form, Depends, UploadFile, File

from schemas.documents import  DocumentType, VerifyDocument
from controller.documents import DocumentController



documents_router = APIRouter()

@documents_router.post("/company_documents/{company_id}")
async def add_company_documents(
    company_id: int,
    created_by_id: int ,
    certificate_of_incorporation: Optional[UploadFile] = File( title="Certificate of Incorporation", description="Certificate of Incorporation to be uploaded"),
    director_national_id: Optional[UploadFile] = File(None, title="Director National ID", description="Director National ID to be uploaded"),
):
    """Create Company Document
    This method creates a company document
    """
     
    document = await DocumentController.add_company_document(company_id, created_by_id, certificate_of_incorporation, director_national_id)
    return document



@documents_router.post("/user_documents/{user_id}")
async def add_user_documents(
    company_user_id: int, 
    created_by_id: int = Form(...),
    ghana_card: Optional[UploadFile] = File(..., title="Ghana Card", description="Ghana Card to be uploaded"),
    profile_picture: Optional[UploadFile] = File(None, title="Profile Picture", description="Profile Picture to be uploaded")
): 
    """Create User Document
    This method creates a user document
    """
    print("this is the user id",company_user_id)
    document = await DocumentController.upload_user_document(created_by_id,company_user_id, ghana_card, profile_picture)
    return document

@documents_router.put("/user_documents/verify/{user_id}")
async def verify_user_document(
    user_id: int,
    data: VerifyDocument
):
    """Verify User Document
    This method verifies a user document
    """
    document =  DocumentController.verify_user_document(user_id,data)
    return document



@documents_router.get("/company_documents")
async def get_company_document(s3_key: str):
    """Get Company Document
    This method gets a company document
    """
    print("this is the s3 key",s3_key)
    document = DocumentController.get_presigned_url(s3_key)
    return document

