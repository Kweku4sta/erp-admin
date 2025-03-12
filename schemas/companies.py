from enum import Enum
from typing import Optional,List

from pydantic import BaseModel, EmailStr, Field
from fastapi import UploadFile, File


from schemas.kyc_accounts import KycAccountOut
from schemas.documents import DocumentOut
from schemas.users import UserOut



class CompanyIn(BaseModel):
    name: str  = Field(..., title="Name", description="Name of the company", examples=["company1", "company2"])
    description: str  = Field(..., title="Description", description="Description of the company", examples=["description1", "description2"])
    street: str  = Field(..., title="Street", description="Street of the company", examples=["street1", "street2"])
    city: str  = Field(..., title="City", description="City of the company", examples=["city1", "city2"])
    state: str  = Field(..., title="State", description="State of the company", examples=["state1", "state2"])
    postal_code: str  = Field(..., title="Postal Code", description="Postal Code of the company", examples=["postal_code1", "postal_code2"])
    phone_number: str  = Field(..., title="Phone Number", description="Phone Number of the company", examples=["phone_number1", "phone_number2"])
    email: EmailStr  = Field(..., title="Email", description="Email of the company")
    ghana_card_number: Optional[str]  = Field(None, title="Ghana Card Number", description="Ghana Card Number of the company", examples=["ghana_card_number1", "ghana_card_number2"])
    created_by_id: int  = Field(..., title="Creator ID", description="ID of the admin creating onboarding the company", examples=[1, 2])
    website: Optional[str]  = Field(None, title="Website", description="Website of the company", examples=["www.company1.com", "www.company2.com"])
    transactional_currency: str  = Field("GHS", title="Transactional Currency", description="Currency of the company", examples=["GHS", "USD"])


class CreatorCompany(BaseModel):
    name: str
    id: int

class Creator (BaseModel):
    id: int | None
    email: str | None
    full_name: str | None
    role: str | None
    role_id: int | None
    # company: str | None
    # company_id: int | None
    # company: CreatorCompany









class Address(BaseModel):
    street: str
    city: str
    state: str
    postal_code: str



class CompanyOut(BaseModel):
    id: int
    name: str
    description: str
    phone_number: str
    email: EmailStr
    nia_verification: bool
    active: bool
    created_by: Optional[Creator] 
    address: Address
    website: Optional[str]
    transactional_currency: Optional[str]
    kyc_account: Optional[KycAccountOut]
    documents:Optional[List[DocumentOut]]


class MultiCreator(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role_id: int




class MultiCompanyOut(BaseModel):
    id: int
    name: str
    description: str
    phone_number: str
    email: EmailStr
    nia_verification: bool
    active: bool
    address: Address
    website: Optional[str]
    transactional_currency: Optional[str]
    created_by: Optional[MultiCreator]
    # kyc_account: Optional[KycAccountOut]
    # documents:Optional[List[DocumentOut]]

    



class SingleCompanyOut(CompanyOut):
    
    users:Optional[List[UserOut]]

    

class CompanyUpdate(BaseModel):
    name: Optional[str]  = Field(None, title="Name", description="Name of the company", examples=["company1", "company2"])
    description: Optional[str]  = Field(None, title="Description", description="Description of the company", examples=["description1", "description2"])
    street: Optional[str]  = Field(None, title="Street", description="Street of the company", examples=["street1", "street2"])
    city: Optional[str]  = Field(None, title="City", description="City of the company", examples=["city1", "city2"])
    state: Optional[str]  = Field(None, title="State", description="State of the company", examples=["state1", "state2"])
    postal_code: Optional[str]  = Field(None, title="Postal Code", description="Postal Code of the company", examples=["postal_code1", "postal_code2"])
    phone_number: Optional[str]  = Field(None, title="Phone Number", description="Phone Number of the company", examples=["phone_number1", "phone_number2"])
    ghana_card_number: Optional[str]  = Field(None, title="Ghana Card Number", description="Ghana Card Number of the company", examples=["ghana_card_number1", "ghana_card_number2"])
    created_by_id: int  = Field(None, title="Creator ID", description="ID of the admin creating onboarding the company", examples=[1, 2])
    website: Optional[str]  = Field(None, title="Website", description="Website of the company", examples=["www.company1.com", "www.company2.com"])
    transactional_currency: Optional[str]  = Field(None, title="Transactional Currency", description="Currency of the company", examples=["GHS", "USD"])

class CompanyParams(BaseModel):
    size: int = Field(50, title="Page Size", description="Number of items to return per page", examples=[10, 20])
    page: int = Field(1, title="Page", description="Page number to return", examples=[1, 2])
    name: Optional[str] = Field(None, title="Name", description="Name of the company")
    email: Optional[str] = Field(None, title="Email", description="Email of the company")
    phone_number: Optional[str] = Field(None, title="Phone Number", description="Phone Number of the company")
    active: Optional[bool] = Field(None, title="Active", description="Is the company active")
    nia_verification: Optional[bool] = Field(None, title="NIA Verification", description="Is the company NIA verified")
    ghana_card_number: Optional[str] = Field(None, title="Ghana Card Number", description="Ghana Card Number of the company")
    created_by_id: Optional[int] = Field(None, title="Creator ID", description="ID of the admin creating onboarding the company")