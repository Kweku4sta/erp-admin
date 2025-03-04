from typing import Optional, List
from datetime import datetime
import dataclasses


from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, Mapper
from sqlalchemy.orm import mapped_column, relationship, composite


from models.custom_base import CustomBase, BaseWithCreator
from models.kyc_accounts import KycAccount


@dataclasses.dataclass
class Address:
    street: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None






class Company(CustomBase, BaseWithCreator):
    __tablename__ = "companies"

    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    street: Mapped[str] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(100))
    state: Mapped[str] = mapped_column(String(100))
    postal_code: Mapped[str] = mapped_column(String(20))
    address: Mapped[Address] = composite(Address, street, city, state, postal_code)
    phone_number: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    ghana_card_number: Mapped[str | None] = mapped_column(String(20), nullable=True)
    nia_verification: Mapped[bool] = mapped_column(default=False)
    

    # -------------------------------relationship-------------------------------------
    kyc_account: Mapped["KycAccount"] = relationship("KycAccount", back_populates='company')
    # creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # creator: Mapped["User"] = relationship("User", foreign_keys="[Company.creator_id]")
    documents: Mapped[List['Document']] = relationship(back_populates='company')
    users: Mapped[List['User']] = relationship("User", back_populates="company", foreign_keys="[User.company_id]", passive_deletes="all")


    def json_data(self):
        print(self.created_by)
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "phone_number": self.phone_number,
            "nia_verification": self.nia_verification,
            "active": self.active,
            "email": self.email,
            "created_by":{
                "id": self.created_by.id if self.created_by else None,
                "email": self.created_by.email if self.created_by else None,
                "full_name": self.created_by.full_name if self.created_by else None,
                "company": {
                            "name": self.created_by.company.name if self.created_by else None,
                            "id": self.created_by.company.id if self.created_by else None
                },
                "company_id": self.created_by.company_id if self.created_by else None,
            },
            "kyc_account": self.kyc_account.json_data() if self.kyc_account else None,
            "users": [user.json_data() for user in self.users],
            "documents": [document.json_data() for document in self.documents] if self.documents else None,
        }
    

    


