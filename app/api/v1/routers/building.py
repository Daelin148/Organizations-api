from fastapi import APIRouter, status

from api.v1.dependencies import UOWDep
from schemas import BuildingRead, BuildingCreate, BuildingOrganizations
from services import BuildingService


router = APIRouter()


@router.get('/', response_model=list[BuildingRead])
async def get_buildings(
    uow: UOWDep
) -> list[BuildingRead]:
    """Вывод информации о зданиях."""
    async with uow:
        buildings = await BuildingService().get_buildings(uow)
        return buildings


@router.post(
    '/', response_model=BuildingRead, status_code=status.HTTP_201_CREATED
)
async def create_scope(
    uow: UOWDep,
    scope_data: BuildingCreate
) -> BuildingRead:
    """Создание здания."""
    async with uow:
        building = await BuildingService().create_building(uow, scope_data)
        return building


@router.get(
    '/{building_id}/organizations', response_model=BuildingOrganizations
)
async def get_organizations_by_building(
    building_id: int,
    uow: UOWDep
) -> BuildingOrganizations:
    """Список всех организаций в конкретном здании."""
    building = await BuildingService().get_with_orgs(
        uow, building_id
    )
    return building
