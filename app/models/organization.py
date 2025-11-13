from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base


class Organization(Base):
    """Модель организации."""
    __tablename__ = 'organizations'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    building_id: Mapped[int] = mapped_column(
        ForeignKey('buildings.id'), nullable=False
    )
    building: Mapped['Building'] = relationship(
        'Building', back_populates='organizations'
    )
    scopes: Mapped[list['Scope']] = relationship(
        'Scope',
        secondary='organization_scope',
        back_populates='organizations',
        lazy="selectin"
    )

    phones: Mapped[list['Phone']] = relationship(
        'Phone',
        back_populates='organization',
        cascade='all, delete-orphan',
        lazy="selectin"
    )
