from sqlalchemy import select, Select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from crud.base import BaseRepository
from models import Building
from geoalchemy2.functions import ST_DWithin, ST_GeomFromText
from geoalchemy2 import WKTElement


class BuildingRepository(BaseRepository[Building]):

    def __init__(self, session: AsyncSession):
        return super().__init__(session, Building)

    def _get_stmt(self) -> Select:
        return select(self.model)

    async def get_with_orgs(self, id: int) -> Building:
        stmt = self._get_stmt().where(Building.id == id).options(
            selectinload(Building.organizations)
        )
        res = await self.session.scalars(stmt)
        return res.first()

    async def get_with_radius_ids(self, lon: float, lat: float, radius):
        point = ST_GeomFromText(f"POINT({lon} {lat})")
        stmt = (
            select(Building.id)
            .where(ST_DWithin(Building.geog, point, radius))
        )
        res = await self.session.scalars(stmt)
        return res.all()

    async def get_with_rectangle(
        self,
        lat_min: float,
        lon_min: float,
        lat_max: float,
        lon_max: float
    ):
        envelope = WKTElement(
            f'POLYGON(({lon_min} {lat_min}, {lon_max} {lat_min}, {lon_max} {lat_max}, {lon_min} {lat_max}, {lon_min} {lat_min}))', srid=4326  # noqa
        )
        stmt = (
            select(Building.id)
            .where(Building.geog.ST_Intersects(envelope))
        )
        res = await self.session.scalars(stmt)
        return res.all()
