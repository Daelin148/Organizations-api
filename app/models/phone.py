from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base


class Phone(Base):
    """Модель телефона организации."""
    __tablename__ = 'phones'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    phone_number: Mapped[str] = mapped_column(
        String(20), nullable=False, unique=True, index=True
    )

    organization_id: Mapped[int] = mapped_column(
        ForeignKey('organizations.id'), nullable=False
    )
    organization: Mapped['Organization'] = relationship(
        'Organization', back_populates='phones'
    )