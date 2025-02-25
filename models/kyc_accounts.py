from typing import Optional

from sqlalchemy import String, Float, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped


from models.custom_base import CustomBase


class KycAccount(CustomBase):
    __tablename__ = "kyc_accounts"


    account_type: Mapped[str] = mapped_column(String, nullable=False)
    max_amount: Mapped[float] = mapped_column(Float, default=20000.00)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("companies.id"))



# ------------------------------Relationships------------------------------
    company: Mapped["Company"] = relationship("Company", back_populates='kyc_accounts')

