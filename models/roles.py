from typing import Optional, List


from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.custom_base import CustomBase

class Role(CustomBase):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    admins: Mapped[List["Admin"]] = relationship("Admin", back_populates="role", passive_deletes="all")


    def json_data(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }