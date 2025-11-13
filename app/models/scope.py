from typing import Optional

from core.db import Base
from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Scope(Base):
    """Модель деятельности."""
    __tablename__ = 'scopes'
    __table_args__ = (
        UniqueConstraint('name', 'parent_id', name='uix_name_parent_id'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(125),
        nullable=False
    )

    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('scopes.id'), nullable=True
    )
    parent: Mapped[Optional['Scope']] = relationship(
        'Scope',
        remote_side=[id],
        back_populates='children'
    )
    children: Mapped[list['Scope']] = relationship(
        'Scope',
        back_populates='parent',
        cascade='all, delete-orphan'
    )
    organizations: Mapped[list['Organization']] = relationship(
        'Organization',
        secondary='organization_scope',
        back_populates='scopes'
    )
