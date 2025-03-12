from typing import Dict
from concurrent.futures import ThreadPoolExecutor

from fastapi_pagination import Page
from fastapi import HTTPException

from schemas.companies import CompanyIn, CompanyUpdate, CompanyParams
from utils import sql
from models.companies import Company
from services.auditlog import AuditLogger
from utils import session, filter
from services.stream import KafkaStreamProducer


class CompanyController:
    executor = ThreadPoolExecutor(max_workers=10)

    @staticmethod
    def create_company(company_data : CompanyIn) -> Dict[str, any]:
        """Create Company
        This method creates a company
        """
        company = Company(**company_data)
        db_company = sql.add_object_to_database(company)
        CompanyController.executor.submit(KafkaStreamProducer.send_json_data_to_topic, "remcashtransactcompany", db_company.json_kafka())
        CompanyController.executor.submit(AuditLogger.log_activity, company_data["created_by_id"], f"Created the company:{company_data['name']}", "CREATE")
        return db_company.json_data()
    


    @staticmethod
    def get_company(company_id: int) -> Dict[str, any]:
        """Get Company
        This method gets a company
        """
        company = sql.get_object_by_id_from_database(Company, company_id)
        if company:
            return company.json_data()
        raise HTTPException(status_code=404, detail="Company not found")
    
    @staticmethod
    def get_companies(params: CompanyParams) -> Page[Company]:
        """Get Companies
        This method gets all companies

        Args:
            params (CompanyParams): [description]
        

        Returns:
            Page[Company]: [description]
            return the list of companies


        """
        with session.CreateDBSession() as db_session:
            companies_query = filter.DynamicQuery(db_session,params, Company)
            companies_query.add_joined_loads()
            return companies_query.paginate()
    

    @staticmethod
    def update_company(company_id: int, company_data: CompanyUpdate) -> Dict[str, any]:
        """Update Company
        This method updates a company
        """
        user_updating = company_data["created_by_id"]
        company_data.pop("created_by_id")
        company_data = {k: v for k, v in company_data.items() if v is not None}
        company = sql.update_object_in_database(Company, company_data, company_id)
        if company:
            CompanyController.executor.submit(AuditLogger.log_activity, user_updating, f"Updated the company:{company_data['name']}", "UPDATE")
            return company.json_data()
        raise HTTPException(status_code=404, detail="Company not found")


    @staticmethod
    def delete_company(company_id: int, created_by_id: int) -> Dict[str, any]:
        """Delete Company
        This method deletes a company

        Args:
            company_id (int): [description]
            the id of the company to delete
            created_by_id (int): [description]
            the id of the user deleting the company
        
        Returns: [description]
            Dict[str, any: [description]
            return the message that the company has been deleted or error message if the company is not found
        """
        company = sql.hard_delete_object_from_database(Company, company_id)
        if company:
            CompanyController.executor.submit(AuditLogger.log_activity, created_by_id, f"Deleted the company:{company_id}", "DELETE")
            return {"message": "Company deleted successfully",
                    "status" : True
                    }
        raise HTTPException(status_code=404, detail="Company not found")
    

    @staticmethod
    def deactivate_company(company_id: int, created_by_id) -> Dict[str, any]:
        """Deactivate Company
        This method deactivates a company

        Args:
            company_id (int): [description]
            the id of the company to deactivate
            created_by_id (int): [description]
            the id of the user deactivating the company        
        Returns:
            Dict[str, any]: [description]
            return the message that the company has been deactivated or error message if the company is not found
        """
        company = sql.deactivate_object_in_database(Company, company_id)
        if company:
            CompanyController.executor.submit(AuditLogger.log_activity, created_by_id, f"Deactivated the company:{company_id}", "DEACTIVATE")
            return {"message": "Company deactivated successfully",
                    "status" : True 
                    }
        raise HTTPException(status_code=404, detail="Company not found")
    

        