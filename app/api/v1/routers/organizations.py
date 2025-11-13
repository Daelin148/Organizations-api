from typing import List, Optional
from fastapi import APIRouter, Query, status

from api.v1.dependencies import UOWDep
from schemas.organization import (
    OrganizationRead, OrganizationCreate
)

from services import OrganizationService

router = APIRouter()


@router.get('/', response_model=list[OrganizationRead])
async def get_orgs(
    uow: UOWDep
) -> list[OrganizationRead]:
    """Список всех организаций."""
    organizations = await OrganizationService().get_all(uow)
    return organizations


@router.get('/search/by_name', response_model=OrganizationRead)
async def search_by_name(
    uow: UOWDep,
    name: str = Query(..., description='Название организации'),
) -> OrganizationRead:
    """Поиск организации по названию или виду деятельности."""
    organization = await OrganizationService().get_by_name(uow, name)
    return organization


@router.get('/search/by_scope', response_model=list[OrganizationRead])
async def search_by_scope(
    uow: UOWDep,
    scope_name: str = Query(
        ..., description='Название вида деятельности'
    )
) -> list[OrganizationRead]:
    """Поиск организации по названию или виду деятельности."""
    organization = await OrganizationService().get_by_scope_tree(
        uow, scope_name
    )
    return organization


@router.get('/{organization_id}', response_model=OrganizationRead)
async def get_organization(
    organization_id: int,
    uow: UOWDep
) -> OrganizationRead:
    """Вывод информации об организации по ID."""
    organization = await OrganizationService().get_organization_by_id(
        uow, organization_id
    )
    return organization


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_organization(
    org_data: OrganizationCreate,
    uow: UOWDep
) -> OrganizationRead:
    """Создание организации."""
    organization = await OrganizationService().create_organization(
        uow, org_data
    )
    return organization


@router.get('/within_radius/', response_model=list[OrganizationRead])
async def get_organizations_within_radius(
    uow: UOWDep,
    lat: float = Query(..., description="Широта центральной точки"),
    lon: float = Query(..., description="Долгота центральной точки"),
    radius: float = Query(..., description="Радиус в метрах"),
) -> List[OrganizationRead]:
    """
    Поиск организаций в заданном радиусе от точки
    """
    organizations = await OrganizationService().get_organizations_in_radius(
        uow, lon, lat, radius
    )
    return organizations


@router.get('/within_rectangle/', response_model=list[OrganizationRead])
async def get_organizations_within_rectangle(
    uow: UOWDep,
    lat_min: float = Query(..., description="Минимальная широта"),
    lon_min: float = Query(..., description="Минимальная долгота"),
    lat_max: float = Query(..., description="Максимальная широта"),
    lon_max: float = Query(..., description="Максимальная долгота"),
) -> List[OrganizationRead]:
    """
    Поиск организаций в прямоугольной области
    """
    organizations = await OrganizationService().get_organizations_in_rectangle(
        uow, lat_min, lon_min, lat_max, lon_max
    )
    return organizations
