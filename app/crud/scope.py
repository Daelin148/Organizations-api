from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, joinedload, selectinload

from models import Organization, Scope

from .base import BaseRepository


class ScopeRepository(BaseRepository[Scope]):

    def __init__(self, session: AsyncSession):
        return super().__init__(session, Scope)

    def _get_stmt(self) -> Select:
        return select(self.model)

    async def filter_by_ids_in(self, ids):
        res = await self.session.scalars(
            self._get_stmt().where(self.model.id.in_(ids))
        )
        return res.all()

    async def get_scope_tree_ids(self, scope_name: str):
        scopes = aliased(Scope, name='scopes')
        children_scopes = aliased(Scope, name='children_scopes')

        scope_cte = (
            select(scopes.id)
            .where(scopes.name == scope_name)
            .where(scopes.parent_id.is_(None))
            .cte(recursive=True, name='scope_tree')
        )
        recursive_part = (
            select(children_scopes.id)
            .select_from(children_scopes)
            .join(scope_cte, children_scopes.parent_id == scope_cte.c.id)
        )
        scope_cte = scope_cte.union_all(recursive_part)

        stmt = select(scope_cte.c.id)
        res = await self.session.scalars(stmt)
        return res.all()

    async def get_with_orgs(self, id: int) -> Scope:
        stmt = self._get_stmt().where(Scope.id == id).options(
            selectinload(Scope.organizations).options(
                joinedload(Organization.building),
                selectinload(Organization.scopes),
                selectinload(Organization.phones)
            )
        )
        res = await self.session.scalars(stmt)
        return res.first()
