from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from fastapi import UploadFile, File



class KycAccountIn(BaseModel):
    account_type: str  = Field(..., title="Account Type", description="Type of the account", examples=["account_type1", "account_type2"])
    max_amount: float  = Field(..., title="Max Amount", description="Maximum amount allowed in the account", examples=[20000.00, 30000.00])
    company_id: int  = Field(..., title="Company ID", description="ID of the company the account belongs to", examples=[1, 2])


class KycAccountOut(BaseModel):
    account_type: str
    max_amount: float
    company_id: int
    id: int


