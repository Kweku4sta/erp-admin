from typing import Dict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime


from fastapi import UploadFile
from schemas.documents import DocumentIn
from models.documents import Document
from services.s3 import upload_to_s3
from utils import session
from services.auditlog import AuditLogger
from models.users import User


class DocumentController:
    executor = ThreadPoolExecutor(max_workers=10)

    @staticmethod
    def add_document(document_data: DocumentIn) -> Dict[str, any]:
        """Create Document
        This method creates a document
        """
        # iterate through the document data and create a document object
        # add the document object to the database
        # return the document object as a dictionary
        pass

    @staticmethod
    def get_document(document_id: int) -> Dict[str, any]:
        """Get Document
        This method gets a document
        """
        pass

    @staticmethod
    async def add_company_document(company_id: int, created_by_id: int,certificate_of_incorporation:UploadFile, director_national_id: UploadFile) -> Dict[str, any]:
        """Create Company Document
        This method creates a company document
        """
        with session.CreateDBSession() as db_session:
            if certificate_of_incorporation:
                certificate_of_incorporation_url = upload_to_s3(certificate_of_incorporation, "remcash", "company_documents")
                company_document = Document(
                    company_id=company_id,
                    document_type="certificate_of_incorporation",
                    document_url=certificate_of_incorporation_url,
                    created_by_id=created_by_id
                )
                db_session.add(company_document)

            if director_national_id:
                director_national_id_url = upload_to_s3(director_national_id, "remcash", "company_documents")
                company_document = Document(
                    company_id=company_id,
                    document_type="director_national_id",
                    document_url=director_national_id_url,
                    created_by_id=created_by_id
                )
                db_session.add(company_document)
            db_session.commit()
            db_session.refresh(company_document)
            DocumentController.executor.submit(AuditLogger.log_activity, created_by_id, f"Uploaded documents for company:{company_id}", "CREATE")
            return company_document.json_data()
        
    @staticmethod
    async def upload_user_document(created_by_id, company_user_id, document: UploadFile) -> Dict[str, any]:
        """Upload User Document
        This method uploads a user document
        """
        with session.CreateDBSession() as db_session:
            company_user = db_session.get(User, company_user_id)
            if not company_user or company_user.company_id:
                return {"message": "User not found"}
            document_url = upload_to_s3(document, "remcash", "user_documents")
            user_document = Document(
                user_id=created_by_id,
                document_type="user_document",
                document_url=document_url,
                created_by_id=created_by_id
            )
            # do nia verification here
            db_session.add(user_document)
            db_session.commit()
            db_session.refresh(user_document)
            DocumentController.executor.submit(AuditLogger.log_activity, created_by_id, f"Uploaded document(s) for {company_user.full_name} in company:{company_user.company.name} ", "CREATE")
            return user_document.json_data()

    @staticmethod
    def verify_user_document(user_id: int, verifier_id: int) -> Dict[str, any]:
        """Verify Document
        This method verifies a document
        """
        with session.CreateDBSession() as db_session:
            user_document = db_session.query(Document).filter_by(user_id=user_id).first()
            if not user_document:
                return {"message": "Document not found"}
            user_document.verifier = verifier_id
            user_document.status = "verified"
            user_document.verified_at = datetime.now()
            db_session.commit()
            db_session.refresh(user_document)
            DocumentController.executor.submit(AuditLogger.log_activity, verifier_id, f"Verified document for user:{user_document.user.full_name}", "UPDATE")
            return user_document.json_data()
        
        
        


    
        

    
            
                
        