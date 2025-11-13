from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from geoalchemy2 import Geography

from core.db import Base


class Building(Base):
    """Модель здания."""
    __tablename__ = 'buildings'

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    geog: Mapped[str] = mapped_column(
        (Geography('POINT')), nullable=False
    )

    organizations: Mapped[list['Organization']] = relationship(
        'Organization',
        back_populates='building',
        cascade='all, delete-orphan'
    )
