from typing import Dict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime



from fastapi import UploadFile, HTTPException
from tools.redis import Cacher




from schemas.documents import DocumentIn, VerifyDocument
from models.documents import Document
from services import s3
from utils import session
from services.auditlog import AuditLogger
from models.users import User
from utils.common import nia_verification
from tools.log import Log
from services.s3 import get_s3_client
from utils import sql
from utils.filter import DynamicQuery



cacher = Cacher()
doc_logger = Log(f"{__name__}")

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
        dockument  =  sql.get_object_by_id_from_database(Document, document_id)
        if dockument:
            return dockument.json_data()
        raise HTTPException(status_code=404, detail="Document not found")

    @staticmethod
    async def add_company_document(company_id: int, created_by_id: int,certificate_of_incorporation:UploadFile, director_national_id: UploadFile) -> Dict[str, any]:
        """Create Company Document
        This method creates a company document
        """
        try:
            with session.CreateDBSession() as db_session:
                if certificate_of_incorporation:
                    cert_urls = await s3.upload_to_s3(certificate_of_incorporation, "company")
                    company_document = Document(
                        company_id=company_id,
                        document_type="certificate_of_incorporation",
                        document_url=cert_urls['presigned_url'],
                        s3_key=cert_urls['s3_key'],
                        created_by_id=created_by_id
                    )
                    db_session.add(company_document)

                if director_national_id:
                    dir_nat_id_url = s3.upload_to_s3(director_national_id, "company")
                    company_document = Document(
                        company_id=company_id,
                        document_type="director_national_id",
                        document_url=dir_nat_id_url['dir_nat_id_url'],
                        created_by_id=created_by_id,
                        s3_key=dir_nat_id_url['s3_key']
                    )
                    db_session.add(company_document)
                db_session.commit()
                db_session.refresh(company_document)
                DocumentController.executor.submit(AuditLogger.log_activity, created_by_id, f"Uploaded documents for company:{company_id}", "CREATE")
                return company_document.json_data()
        except Exception as e:
            # s3.delete_from_s3(cert_urls['s3_key']) if cert_urls else None
            raise e

            # delete the document from s3

        

    @staticmethod
    def get_presigned_url(s3_key: str) -> Dict[str, any]:
        """Get Presigned URL
        This method gets a presigned URL
        """

        if cacher.get_value(s3_key):
            presigned_url =  cacher.get_value(s3_key) 
            return {
                "s3_key": s3_key,
                "presigned_url": presigned_url
            }
        with session.CreateDBSession() as db_session:
            existing_s3_key = db_session.query(Document).filter(Document.s3_key == s3_key).first()
            if not existing_s3_key:
                raise HTTPException(status_code=404, detail="Invalid s3 key")
            s3_client = get_s3_client()
            presigned_url =  s3.create_presigned_url(s3_client,s3_key)
            return {
                "presigned_url": presigned_url,
                "s3_key": s3_key,
            }
            
    @staticmethod
    async def upload_user_document(created_by_id : int, company_user_id: int, document: UploadFile, profile_picture: UploadFile) -> Dict[str, any]:
        """Upload User Document
        This method uploads a user document
        """
        with session.CreateDBSession() as db_session:
            company_user = db_session.get(User, company_user_id)
            if not company_user or not company_user.company_id:
                raise HTTPException(status_code=404, detail="User not found")
           
            if document and company_user.nia_verification_status is False:
                nia_response = nia_verification(document, company_user.ghana_card_number)
                if not nia_response:
                    doc_logger.info(f"Document verification failed for {company_user.full_name}")
                company_user.nia_verification_status = True
                db_session.commit()
                db_session.refresh(company_user)
            
            if  profile_picture:
                profile_picture_url = s3.upload_to_s3(profile_picture, "user_profile_pictures")
                user_profile_picture = Document(
                    user_id=created_by_id,
                    document_type="profile_picture",
                    document_url=profile_picture_url['presigned_url'],
                    created_by_id=created_by_id
                )
                db_session.add(user_profile_picture)

            db_session.commit()
            db_session.refresh(user_profile_picture) 
            DocumentController.executor.submit(AuditLogger.log_activity, created_by_id, f"Uploaded document(s) for {company_user.full_name} in company:{company_user.company.name} ", "CREATE")
            return {"message": "Document uploaded successfully"}  

    @staticmethod
    def verify_user_document(user_id: int, data: VerifyDocument) -> Dict[str, any]:
        """Verify Document
        This method verifies a document
        """
        with session.CreateDBSession() as db_session:
            user_document = db_session.query(Document).filter_by(user_id=user_id).first()
            if not user_document:
                raise HTTPException(status_code=404, detail="Document not found")
            if user_document.nia_verification_status is False:
                raise HTTPException(status_code=400, detail="Nia verification not done")
            user_document.verifier = data.verifier_id
            user_document.status = data.status
            user_document.verified_at = datetime.now()
            db_session.commit()
            db_session.refresh(user_document)
            DocumentController.executor.submit(AuditLogger.log_activity, data.verifier_id, f"Verified document for user:{user_document.user.full_name}", "UPDATE")
            return user_document.json_data()
        


    @staticmethod
    def get_all_documents(params: dict) -> Dict[str, any]:
        with session.CreateDBSession() as db_session:
            documents_query = DynamicQuery(db_session=db_session,params=params,model=Document)
            return documents_query.paginate()
        


    @staticmethod
    def get_company_documents(company_id: int):
        with session.CreateDBSession() as db_session:
            company_documents = db_session.query(Document).filter(Document.company_id == company_id).all()
            return [doc.json_data() for doc in company_documents]
        
    @staticmethod
    def get_user_documents(user_id: int):
        with session.CreateDBSession() as db_session:
            user_documents = db_session.query(Document).filter(Document.user_id == user_id).all()
            return [doc.json_data() for doc in user_documents]
        

    

        
        
        


    
        

    
            
                
        