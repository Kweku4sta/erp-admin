
from typing import Optional
from datetime import datetime

from sqlalchemy import String, Float, DateTime, Integer, Boolean, ForeignKey, CheckConstraint

from sqlalchemy.orm import Mapped, Mapper
from sqlalchemy.orm import mapped_column, relationship
from utils import session


from models.custom_base import CustomBase, BaseWithCreator


class Payment(CustomBase, BaseWithCreator):
    __tablename__ = "payments"


    __table_args__ = (
        CheckConstraint(
            '(company_id IS NOT NULL AND user_id IS NULL) OR (company_id IS NULL AND user_id IS NOT NULL)',
            name='check_company_or_user_payment'
        ),
    )
    
    amount: Mapped[float] = mapped_column(Float, default=0.0)
    is_reversed: Mapped[bool] = mapped_column(Boolean, default=False)


    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("companies.id"), nullable=True)
    company: Mapped["Company"] = relationship("Company", back_populates="payments")
    transaction = relationship("Transaction", back_populates="payment", uselist=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    user: Mapped["User"] = relationship("User", back_populates="payments", foreign_keys="[Payment.user_id]")



    def save(self):
        with session.CreateDBSession() as db_session:
            db_session.add(self)
            db_session.commit()
            db_session.refresh(self)
            return self


    def json_data(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "is_reversed": self.is_reversed,
            "created_at": self.created_at,
            "company_id": self.company_id,
            # "company": self.company.json_data() if self.company else None,
            # "user": self.user.json_data() if self.user else None,
            # "transaction": self.transaction.json_data() if self.transaction else None
        }
    

    