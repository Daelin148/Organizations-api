from fastapi import HTTPException, status
from models import Building
from schemas import BuildingRead, BuildingCreate, BuildingOrganizations
from utils.unitofwork import UnitOfWork


class BuildingService:

    async def get_buildings(self, uow: UnitOfWork) -> list[BuildingRead]:
        async with uow:
            buildings = await uow.buildings.get_all()
            return [
                BuildingRead.model_validate(building) for building in buildings
            ]

    async def create_building(
        self, uow: UnitOfWork, building_data: BuildingCreate
    ) -> Building:
        async with uow:
            building = await uow.buildings.add_one(building_data.model_dump())
            await uow.commit()
            return building

    async def get_with_orgs(
        self, uow: UnitOfWork, building_id: int
    ) -> list[BuildingOrganizations]:
        async with uow:
            building = await uow.buildings.get_with_orgs(building_id)
            if not building:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Здание не найдено'
                )
            return BuildingOrganizations.model_validate(building)
