from typing import Optional
from datetime import datetime

from sqlalchemy import String, Float, DateTime, Integer, ForeignKey

from sqlalchemy.orm import Mapped, Mapper
from sqlalchemy.orm import mapped_column, relationship


from models.custom_base import CustomBase



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
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    reference_code: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    transaction_reference: Mapped[str] = mapped_column(String(50), nullable=False, index=True, unique=True)
    authorizer: Mapped[str] = mapped_column(String(50), nullable=True)
    company_id: Mapped[int] = mapped_column(Integer, nullable=False)
    company = relationship("Company", backref="transactions")
    user = relationship("User", backref="transactions")
    confirmed_at: Mapper[datetime] = mapped_column(DateTime)
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    payment_id: Mapped[int] = mapped_column(Integer, ForeignKey("payments.id"), nullable=True)
    payment = relationship("Payments", backref="transaction")






    # source_account_name = Column(String, index=True)
    # source_account_number = Column(String, index=True) 
    # source_bank_sort_code = Column(String, index=True)
    # source_bank_name = Column(String, index=True)
    # recipient_bank_sort_code = Column(String, index=True)
    # recipient_bank_name = Column(String, index=True)
    # recipient_account_number = Column(String, index=True)
    # recipient_account_name = Column(String, index=True)
    # amount = Column(Float, server_default="0.00", index=True, nullable=False)
    # # Here naration is referred to as reference
    # reference = Column(String, index=True)
    # status = Column(
    #     Enum(TransactionStatus), nullable=False, default=TransactionStatus.failed.value
    # )
    # type = Column(
    #     Enum(TransactionType), nullable=False, default=TransactionType.bank.value
    # )
    # reference_code = Column(String, index=True)
    # transaction_reference = Column(String, index=True, unique=True)
    # authorizer = Column(String, nullable=True)
    # company_id = Column(Integer, ForeignKey("companies.id"))
    # company = relationship(
    #     "Company", backref=backref("transactions", passive_deletes="all")
    # )
    # user = relationship("User", backref=backref("transactions", passive_deletes="all"))
    # confirmed_at = Column(DateTime)
    # created_at = Column(DateTime, default=datetime.utcnow)
    # updated_at = Column(DateTime, default=datetime.utcnow)
    # balance_before = Column(Float, nullable=True)
    # balance_after = Column(Float, nullable=True)
    # created_by = Column(Integer, ForeignKey("users.id"))
    # payment_id = Column(Integer, ForeignKey("payments.id"), nullable=True)
    # payment = relationship("Payments", backref=backref("transaction", uselist=False))

