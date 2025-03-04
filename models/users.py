from typing import Optional
from datetime import datetime

from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped
from models.documents import Document


from models.custom_base import CustomBase


class User(CustomBase):
  
  __tablename__="users"

  email: Mapped[str] = mapped_column(String, unique=True)
  full_name: Mapped[str] = mapped_column(String, nullable=False)
  password: Mapped[str] = mapped_column(String, nullable=False)
  token: Mapped[Optional[str]] = mapped_column(String, nullable=True)
  is_authorizer: Mapped[bool] = mapped_column(Boolean, default=False)
  company_id: Mapped[int] = mapped_column(Integer, ForeignKey("companies.id"))
  company: Mapped["Company"] =relationship("Company", back_populates="users", passive_deletes="all", foreign_keys="[User.company_id]")
  # role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id"))
  # role = relationship("Role", back_populates="users", passive_deletes="all")
  flag: Mapped[bool] = mapped_column(Boolean, default=False)

  # --------------------------relationship---------------------
  documents: Mapped['Document'] = relationship("Document",back_populates='user', foreign_keys="[Document.user_id]", passive_deletes="all")


  def json_data(self):
    return {
      "id": self.id,
      "email": self.email,
      "full_name": self.full_name,
      "company": self.company.name if self.company else None,
      "flag": self.flag,
      "is_authorizer": self.is_authorizer,
      "created_at": self.created_at,
      "updated_at": self.updated_at,
      "documents": [document.json_data() for document in self.documents] if self.documents else None,
      "token": self.token
    }



  