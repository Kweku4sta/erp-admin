from typing import List 

from fastapi import APIRouter
from schemas.kyc_accounts import KycAccountIn
from controller.kyc_accounts import KycAccountController


company_router = APIRouter()



@company_router.post("/kyc_accounts")
def onboard_kyc_account(data: KycAccountIn):
    """Create Kyc Account
    This method creates a kyc account
    """
    kyc_account = KycAccountController.create_kyc_account(data.__dict__)
    return kyc_account

