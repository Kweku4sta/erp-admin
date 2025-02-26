from typing import List 

from fastapi import APIRouter
from schemas.companies import CompanyIn
from controller.companies import CompanyController


company_router = APIRouter()

@company_router.post("/companies")
def onboard_company(data: CompanyIn):
    """Create Company
    This method creates a company
    """
    company = CompanyController.create_company(data.__dict__)
    return company




@company_router.get("/companies/{company_id}")
def get_company(company_id: int):
    """Get Company
    This method gets a company
    """
    company = CompanyController.get_company(company_id)
    return company
