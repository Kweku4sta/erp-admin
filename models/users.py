from typing import Optional
from datetime import datetime

from sqlalchemy import String, Float, DateTime, Integer, Boolean, ForeignKey


from sqlalchemy.orm import mapped_column, relationship, Mapped


from models.custom_base import CustomBase


class User(CustomBase):
  
  __tablename__="users"

  email: Mapped[str] = mapped_column(String, unique=True)
  full_name: Mapped[str] = mapped_column(String, nullabe=False)
  password: Mapped[str] = mapped_column(String, nullable=False)
  token: Mapped[Optional[str]] = mapped_column(String, nullable=True)
  is_authorizer: Mapped[bool] = mapped_column(Boolean, default=False)
  company_id: Mapped[int] = mapped_column(Integer, ForeignKey("companies.id"))
  company = relationship("Company", backpopulates="users", passive_deletes="all")
  role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id"))
  role = relationship("Role", backpopulates="users", passive_deletes="all")

  