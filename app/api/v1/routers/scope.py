from fastapi import APIRouter, status, Query

from api.v1.dependencies import UOWDep
from schemas import (
    ScopeBase, ScopeRead, ScopeOrganizations
)
from services import ScopeService


router = APIRouter()


@router.get('/', response_model=list[ScopeRead])
async def get_scopes(
    uow: UOWDep
) -> list[ScopeRead]:
    """Вывод информации о видах деятельности."""
    async with uow:
        scopes = await ScopeService().get_all_scopes(uow)
        return scopes


@router.post(
    '/', response_model=ScopeRead, status_code=status.HTTP_201_CREATED
)
async def create_scope(
    uow: UOWDep,
    scope_data: ScopeBase
) -> ScopeRead:
    """Создание вида деятельности."""
    async with uow:
        scope = await ScopeService().create_scope(uow, scope_data)
        return scope


@router.get(
    '/{scope_id}/organizations', response_model=ScopeOrganizations
)
async def get_organizations_by_scope(
    scope_id: int,
    uow: UOWDep
) -> ScopeOrganizations:
    """Список всех организаций в конкретном здании."""
    scope = await ScopeService().get_with_orgs(
        uow, scope_id
    )
    return scope
