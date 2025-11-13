from sqlalchemy import select
from sqlalchemy import Select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from models import Organization, Scope
from .base import BaseRepository


class OrganizationRepository(BaseRepository[Organization]):

    def __init__(self, session: AsyncSession):
        return super().__init__(session, Organization)

    async def filter_by_buildings_id(
        self, ids: list[int]
    ):
        stmt = self._get_stmt().where(Organization.building_id.in_(ids))
        res = await self.session.scalars(stmt)
        return res.all()

    async def filter_by_scopes_id(
        self, ids: list[int]
    ):
        stmt = self._get_stmt().filter(
            Organization.scopes.any(Scope.id.in_(ids))
        )
        res = await self.session.scalars(stmt)
        return res.all()

    def _get_stmt(self) -> Select:
        return select(self.model).options(
                joinedload(self.model.building),
                selectinload(self.model.phones),
                selectinload(self.model.scopes)
            )
