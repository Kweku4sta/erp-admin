from typing import Optional, List
from datetime import datetime

from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped


from models.custom_base import CustomBase


class Admin(CustomBase):
  
  __tablename__="admins"

  email: Mapped[str] = mapped_column(String, unique=True)
  full_name: Mapped[str] = mapped_column(String)
  role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id"))
  role = relationship("Role", back_populates="admins", passive_deletes="all")
  password: Mapped[str] = mapped_column(String)
  reset_password: Mapped[bool] = mapped_column(Boolean, default=True)



  def json_data(self):
    return {
      "id": self.id,
      "email": self.email,
      "full_name": self.full_name,
      "created_at": self.created_at,
      "updated_at": self.updated_at,
      "role": self.role.name if self.role else None,
      "role_id": self.role_id,
      "reset_password": self.reset_password
    }



  