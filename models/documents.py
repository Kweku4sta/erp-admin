from datetime import datetime


from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


from models.custom_base import CustomBase

class Document(CustomBase):
    __tablename__ = 'documents'

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int | None] = mapped_column(ForeignKey('companies.id', ondelete='CASCADE'), nullable=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    document_type: Mapped[str] = mapped_column(String(100), nullable=False)
    document_url: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default='pending')
    verified_by: Mapped[int | None] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    verified_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company: Mapped['Company'] = relationship(back_populates='documents')
    user: Mapped['User'] = relationship(back_populates='documents')
    verifier: Mapped['User'] = relationship(foreign_keys=[verified_by])

    # Check constraint (ensure document is linked to either a company or a user)
    __table_args__ = (
        CheckConstraint(
            '(company_id IS NOT NULL AND user_id IS NULL) OR (company_id IS NULL AND user_id IS NOT NULL)',
            name='check_company_or_user'
        ),
    )