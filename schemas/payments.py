from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class PaymentIn(BaseModel):
    company_id: int  = Field(..., title="Company ID", description="ID of the company", examples=[1, 2])
    amount: float = Field(..., title="Amount", description="Amount to be paid", examples=[100.00, 200.00])
    created_at: datetime = Field(..., title="Created At", description="Date and time the payment was created", examples=["2021-08-01T00:00:00"])
    created_by_id: int = Field(..., title="Creator ID", description="ID of the admin creating the payment", examples=[1, 2])



class PaymentUpdateFields(BaseModel):
    company_id: Optional[int] = Field(None, title="Company ID", description="ID of the company", examples=[1, 2])
    amount: Optional[float] = Field(None, title="Amount", description="Amount to be paid", examples=[100.00, 200.00])
    created_at: Optional[datetime] = Field(None, title="Created At", description="Date and time the payment was created", examples=["2021-08-01T00:00:00"])
    created_by_id: int = Field(..., title="Updator ID", description="ID of the admin creating the payment", examples=[1, 2])




class PaymentOut(BaseModel):
    id: int
    company_id: int
    amount: float
    created_at: datetime
    is_reversed: bool

class PaymentUpdate(BaseModel):
    amount: float  = Field(None, title="Amount", description="Amount to be paid", examples=[100.00, 200.00])
    is_reversed: bool  = Field(None, title="Is Reversed", description="Is the payment reversed", examples=[False, True])
