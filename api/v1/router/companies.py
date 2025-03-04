from typing import List 

from fastapi import APIRouter, Depends
from fastapi_pagination import Page

from schemas.companies import CompanyIn, CompanyOut, SingleCompanyOut, CompanyParams
from controller.companies import CompanyController
from schemas.common import DelResponse




company_router = APIRouter()

@company_router.post("/companies", response_model=CompanyOut)
def onboard_company(data: CompanyIn):
    """Create Company
    This method creates a company
    """
    company = CompanyController.create_company(data.__dict__)
    return company



@company_router.get("/companies/{company_id}", response_model=SingleCompanyOut)
def get_company(company_id: int):
    """Get Company
    This method gets a company
    """
    company = CompanyController.get_company(company_id)
    return company

@company_router.get("/companies", response_model=Page[CompanyOut])
def get_companies(params: CompanyParams = Depends()):
    """Get Companies
    This method gets all companies
    """
    companies = CompanyController.get_companies(params)
    return companies


@company_router.put("/companies/{company_id}", response_model=SingleCompanyOut)
def update_company(company_id: int, data: CompanyIn):
    """Update Company
    This method updates a company
    """
    company = CompanyController.update_company(company_id, data.__dict__)
    return company


@company_router.delete("/companies/{company_id}", response_model=DelResponse)
def delete_company(company_id: int, created_by_id: int):
    """Delete Company
    This method deletes a company
    """
    company = CompanyController.delete_company(company_id, created_by_id)
    return company

@company_router.delete("/companies/deactivate/{company_id}", response_model=DelResponse)
def deactivate_company(company_id: int, created_by_id: int):
    """Delete Company
    This method deactivates a company
    """
    company = CompanyController.deactivate_company(company_id, created_by_id)
    return company

