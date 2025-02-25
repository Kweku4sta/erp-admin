from typing import Optional
from datetime import datetime
import dataclasses


from sqlalchemy import String, Float, DateTime, Integer

from sqlalchemy.orm import Mapped, ForeignKey, Mapper
from sqlalchemy.orm import mapped_column, relationship, composite


from models.custom_base import CustomBase


@dataclasses.dataclass
class Address:
    street: str | None = None
    city: str
    state: str | None = None
    postal_code: str | None = None






class Company(CustomBase):
    __tablename__ = "companies"

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    street: Mapped[str] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(100))
    state: Mapped[str] = mapped_column(String(100))
    postal_code: Mapped[str] = mapped_column(String(20))
    address: Mapped[Address] = composite(Address, street, city, state, postal_code)
    phone_number: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    

    # -------------------------------relationship-------------------------------------
    kyc_account_id: Mapped[int] = mapped_column(Integer, ForeignKey("kyc_accounts.id"))
    kyc_account = relationship("KycAccount", back_populates="company")
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    creator: Mapped["User"] = relationship("User", back_populates="company")
    

    


