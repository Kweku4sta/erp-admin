from typing import Optional
from datetime import datetime
from enum import Enum

from sqlalchemy import String, Float, DateTime, Integer, ForeignKey


from sqlalchemy.orm import Mapped, Mapper
from sqlalchemy.orm import mapped_column, relationship
from models.payments import Payment


from models.custom_base import CustomBase



class TransactionStatus(Enum):
    failed = "failed"
    success = "success"


class TransactionType(Enum):
    bank = "bank"
    mobile = "mobile"







class Transaction(CustomBase):
    __tablename__ = "transactions"


    source_account_name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    source_account_number: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    source_bank_sort_code: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    source_bank_name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    recipient_bank_sort_code: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    recipient_bank_name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    recipient_account_number: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    recipient_account_name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    amount: Mapped[float] = mapped_column(Float, server_default="0.00", nullable=False)
    reference: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    status: Mapped[TransactionStatus] = mapped_column(String(50), nullable=False, default=TransactionStatus.failed.value)
    type: Mapped[TransactionType] = mapped_column(String(50), nullable=False, default=TransactionType.bank.value)
    reference_code: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    transaction_reference: Mapped[str] = mapped_column(String(50), nullable=False, index=True, unique=True)
    authorizer: Mapped[str] = mapped_column(String(50), nullable=True)
    confirmed_at: Mapped[datetime] = mapped_column(DateTime)
    balance_before: Mapped[float] = mapped_column(Float, server_default="0.00", nullable=True)
    balance_after: Mapped[float] = mapped_column(Float, server_default="0.00", nullable=True)


    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="transactions", foreign_keys=[created_by])

    payment_id: Mapped[int] = mapped_column(Integer, ForeignKey("payments.id"), nullable=True)
    payment = relationship("Payment", back_populates="transaction")

     
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", back_populates="transactions")



    # user = relationship("User", back_populates="transactions")
    # payment = relationship("Payments", back_populates="transaction")


    # payment = relationship("Payments", backref="transaction")
    # company = relationship("Company", backref="transactions")
    # user = relationship("User", backref="transactions")











    