from typing import Optional

from sqlalchemy import String, Float, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, relationship, Mapped


from models.custom_base import CustomBase, BaseWithCreator


class KycAccount(CustomBase, BaseWithCreator):
    __tablename__ = "kyc_accounts"
    __table_args__ = (UniqueConstraint('company_id', name="unique_company_kyc"), )
    


    account_type: Mapped[str] = mapped_column(String, nullable=False)
    max_amount: Mapped[float] = mapped_column(Float, default=20000.00)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("companies.id"))



# ------------------------------Relationships------------------------------
    company: Mapped["Company"] = relationship("Company", back_populates='kyc_account')

    def json_data(self):
        return {
            "id": self.id,
            "account_type": self.account_type,
            "max_amount": self.max_amount,
            "company_id": self.company_id,
            "created_by":{
                "id": self.created_by.id,
                "email": self.created_by.email,
                "full_name": self.created_by.full_name,
                # "company": self.created_by.company.name,
                "company": {
                            "name": self.created_by.company.name if self.created_by else None,
                            "id": self.created_by.company.id if self.created_by else None
                },
                "company_id": self.created_by.company_id	

            }
        }

