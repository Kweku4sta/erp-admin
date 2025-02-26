from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from fastapi import UploadFile, File



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
