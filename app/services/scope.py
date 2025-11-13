from fastapi import HTTPException, status

from models import Scope
from schemas import ScopeBase, ScopeOrganizations, ScopeRead
from utils.unitofwork import UnitOfWork


class ScopeService:

    async def get_all_scopes(
        self, uow: UnitOfWork
    ) -> list[ScopeRead]:
        async with uow:
            scopes = await uow.scopes.get_all()
            return [ScopeRead.model_validate(scope) for scope in scopes]

    async def create_scope(
        self, uow: UnitOfWork,
        scope_data: ScopeBase
    ) -> Scope:
        async with uow:
            parent_scope_id = scope_data.parent_id
            if parent_scope_id is not None:
                parent_scope = await uow.scopes.get_one(
                    id=scope_data.parent_id
                )
                if not parent_scope:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail='Родительская активность не найдена'
                    )
                scopes = await uow.scopes.get_all()
                self._validate_depth(scopes, parent_scope_id)
            scope = await uow.scopes.add_one(
                scope_data.model_dump()
            )
            await uow.commit()
            return scope

    def _validate_depth(
        self,
        all_scopes: list[Scope],
        parent_id: int, max_depth: int = 3
    ) -> None:
        """Проверка что глубина вложенности не превышает лимит."""
        depth = self._calculate_depth(all_scopes, parent_id) + 1
        if depth >= max_depth:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Вложенность активностей ограничена 3 уровнями'
            )

    async def get_with_orgs(
        self, uow: UnitOfWork, scope_id: int
    ) -> list[ScopeOrganizations]:
        async with uow:
            scope = await uow.scopes.get_with_orgs(scope_id)
            if not scope:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Вид деятельности не найден'
                )
            return ScopeOrganizations.model_validate(scope)

    def _calculate_depth(
        self,
        all_scopes: list[Scope],
        scope_id: int
    ) -> int:
        """Вычисление глубины активности от корня"""
        scope_map = {scope.id: scope for scope in all_scopes}

        depth = 0
        current_id = scope_id

        while current_id in scope_map and scope_map[current_id].parent_id:
            depth += 1
            current_id = scope_map[current_id].parent_id
        return depth
