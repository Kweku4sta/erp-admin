
from typing import Optional
from datetime import datetime

from sqlalchemy import String, Float, DateTime, Integer, Boolean

from sqlalchemy.orm import Mapped, ForeignKey, Mapper
from sqlalchemy.orm import mapped_column, relationship


from models.custom_base import CustomBase


class Payment(CustomBase):
    __tablename__ = "payments"

    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", backref="payments")
    amount: Mapped[float] = mapped_column(Float, default=0.0)
    is_reversed: Mapped[bool] = mapped_column(Boolean, default=False)