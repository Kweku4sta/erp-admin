from typing import Dict
from concurrent.futures import ThreadPoolExecutor

from schemas.companies import CompanyIn
from utils import sql
from models.companies import Company
from services.auditlog import AuditLogger

class CompanyController:
    executor = ThreadPoolExecutor(max_workers=10)

    @staticmethod
    def create_company(company_data : CompanyIn) -> Dict[str, any]:
        """Create Company
        This method creates a company
        """
        company = Company(**company_data)
        sql.add_object_to_database(company)
        CompanyController.executor.submit(AuditLogger.log_activity, company_data["created_by_id"], f"Created the company:{company_data['name']}", "CREATE")
        return company.json_data()
    


    @staticmethod
    def get_company(company_id: int) -> Dict[str, any]:
        """Get Company
        This method gets a company
        """
        company = sql.get_object_by_id_from_database(Company, company_id)
        return company.json_data()