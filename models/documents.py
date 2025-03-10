from datetime import datetime
from enum import Enum


from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship


from models.custom_base import CustomBase,BaseWithCreator


class Status(Enum):
    new = 'new'
    verified = 'verified'
    deactivated = 'deactivated'




class Document(CustomBase, BaseWithCreator ):
    __tablename__ = 'documents'

    company_id: Mapped[int | None] = mapped_column(ForeignKey('companies.id', ondelete='CASCADE'), nullable=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    verifier_id: Mapped[int | None] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    document_type: Mapped[str] = mapped_column(String(100), nullable=False)
    document_url: Mapped[str] = mapped_column(String, nullable=False)
    s3_key: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[Status] = mapped_column(String(50), default="new")
    verified_at: Mapped[datetime | None] = mapped_column(DateTime)
    
    # Relationships
    company: Mapped['Company'] = relationship(back_populates='documents')
    user: Mapped['User'] = relationship(back_populates='documents', foreign_keys=[user_id])
    verifier: Mapped['User'] = relationship(foreign_keys=[verifier_id])

    # Check constraint (ensure document is linked to either a company or a user)
    __table_args__ = (
        CheckConstraint(
            '(company_id IS NOT NULL AND user_id IS NULL) OR (company_id IS NULL AND user_id IS NOT NULL)',
            name='check_company_or_user'
        ),
    )

    def json_data(self):
        return {
            "id": self.id,
            "document_type": self.document_type,
            "document_url": self.document_url,
            "s3_key": self.s3_key,
            "status": self.status,
            "verified_by": self.verifier.json_data() if self.verifier else None,
            "verified_at": self.verified_at,
            "created_by": {
                "id": self.created_by.id,
                "email": self.created_by.email,
                "full_name": self.created_by.full_name,
                "role": self.created_by.role.name if self.created_by.role else None,
                "role_id": self.created_by.role_id,
                # # "company": self.created_by.company.name if self.created_by.company else None,
                # "company": {
                #             "name": self.created_by.company.name if self.created_by else None,
                #             "id": self.created_by.company.id if self.created_by else None
                # },
                # "company_id": self.created_by.company_id
            },
        }