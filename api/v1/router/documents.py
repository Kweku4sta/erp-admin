from typing import List, Annotated, Optional

from fastapi import APIRouter, Form, Depends, UploadFile, File

from schemas.documents import DocumentIn, TestDocument, DocumentType
from controller.documents import DocumentController



documents_router = APIRouter()
@documents_router.post("/documents")
def add_document(
    document_type: Annotated[DocumentType, Form()],
    document: UploadFile = Annotated[File(None, title="Document", description="Document to be uploaded"), Form()]

) -> dict:
    """Create Document
    This method creates a document
    """
    print(document_type, document)
    return {"message": "Document created successfully"}	



@documents_router.post("/company_documents/{company_id}")
async def add_company_documents(
    company_id: int,
    created_by_id: int = Form(...),
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
):
    """Create User Document
    This method creates a user document
    """
    document = await DocumentController.upload_user_document(created_by_id,company_user_id, ghana_card)
    return document

@documents_router.put("/user_documents/verify/{user_id}")
async def verify_user_document(
    user_id: int,
    verifier_id: int 
):
    """Verify User Document
    This method verifies a user document
    """
    document =  DocumentController.verify_user_document(user_id,verifier_id)
    return document

