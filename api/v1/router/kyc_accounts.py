from typing import List 

from fastapi_pagination import Page
from fastapi import Depends

from fastapi import APIRouter
from schemas.kyc_accounts import KycAccountIn, KycAccountUpdate, KycAccountOut, KycParams, MultiKycAccount
from controller.kyc_accounts import KycAccountController
from schemas.common import DelResponse



company_router = APIRouter()



@company_router.post("/kyc_accounts", response_model=KycAccountOut)
def onboard_kyc_account(data: KycAccountIn):
    """Create Kyc Account
    This method creates a kyc account
    """
    kyc_account = KycAccountController.create_kyc_account(data.__dict__)
    return kyc_account


@company_router.get("/kyc_accounts/{kyc_account_id}", response_model=KycAccountOut)
def get_kyc_account(kyc_account_id: int):
    """Get Kyc Account
    This method gets a kyc account
    """
    kyc_account = KycAccountController.get_kyc_account(kyc_account_id)
    return kyc_account


@company_router.delete("/kyc_accounts/{kyc_account_id}", response_model=DelResponse)
def delete_kyc_account(kyc_account_id: int, created_by_id: int):
    """Delete Kyc Account
    This method deletes a kyc account
    """
    kyc_account = KycAccountController.delete_kyc_account(kyc_account_id, created_by_id)
    return kyc_account


@company_router.put("/kyc_accounts/{kyc_account_id}", response_model=KycAccountOut)
def update_kyc_account(kyc_account_id: int, data: KycAccountUpdate):
    """Update Kyc Account
    This method updates a kyc account
    """
    kyc_account = KycAccountController.update_kyc_account(kyc_account_id, data.__dict__)
    return kyc_account


@company_router.get("/kyc_accounts", response_model=Page[MultiKycAccount])
def get_kyc_accounts(params: KycParams = Depends()):
    """Get Kyc Accounts
    This method gets all kyc accounts
    """
    kyc_accounts = KycAccountController.get_kyc_accounts(params)
    return kyc_accounts



