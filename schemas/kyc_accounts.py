

from pydantic import BaseModel, Field


class CreatorCompany(BaseModel):
    name: str
    id: int





class KycAccountIn(BaseModel):
    account_type: str  = Field(..., title="Account Type", description="Type of the account", examples=["account_type1", "account_type2"])
    max_amount: float  = Field(..., title="Max Amount", description="Maximum amount allowed in the account", examples=[20000.00, 30000.00])
    company_id: int  = Field(..., title="Company ID", description="ID of the company the account belongs to", examples=[1, 2])
    created_by_id: int  = Field(..., title="Creator ID", description="ID of the admin creating the account", examples=[1, 2])

class CreatorDetails(BaseModel):
    id: int 
    email: str 
    full_name: str
    role: str
    role_id: int
    # company: str 
    # company_id: int 
    # company:CreatorCompany




class KycAccountOut(BaseModel):
    account_type: str
    max_amount: float
    company_id: int
    id: int
    created_by: CreatorDetails 


class KycAccountUpdate(BaseModel):
    account_type: str  = Field(None, title="Account Type", description="Type of the account", examples=["account_type1", "account_type2"])
    max_amount: float  = Field(None, title="Max Amount", description="Maximum amount allowed in the account", examples=[20000.00, 30000.00])
    company_id: int  = Field(None, title="Company ID", description="ID of the company the account belongs to", examples=[1, 2])
    created_by_id: int  = Field(None, title="Creator ID", description="ID of the admin creating the account", examples=[1, 2])


class KycParams(BaseModel):
    page_size: int = Field(10, title="Page Size", description="Number of items to return per page", examples=[10, 20])
    page: int = Field(1, title="Page", description="Page number to return", examples=[1, 2])





