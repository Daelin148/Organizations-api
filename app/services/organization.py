from models import Organization
from schemas.organization import OrganizationCreate, OrganizationRead
from utils.unitofwork import UnitOfWork
from fastapi import HTTPException, status


class OrganizationService:

    async def get_all(self, uow: UnitOfWork) -> list[OrganizationRead]:
        async with uow:
            organizations = await uow.organizations.get_all()
            return [
                OrganizationRead.model_validate(
                    organization
                ) for organization in organizations
            ]

    async def get_by_name(
        self, uow: UnitOfWork, name: str
    ) -> OrganizationRead:
        async with uow:
            organization = await uow.organizations.get_one(name=name)
            if not organization:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Организация с таким именем не найдена'
                )
            return OrganizationRead.model_validate(organization)

    async def get_by_scope_tree(
        self, uow: UnitOfWork, scope_name: str
    ) -> list[OrganizationRead]:
        async with uow:
            scopes_ids = await uow.scopes.get_scope_tree_ids(scope_name)
            if not scopes_ids:
                return []
            organizations = await uow.organizations.filter_by_scopes_id(
                scopes_ids
            )
            return [
                OrganizationRead.model_validate(
                    organization
                ) for organization in organizations
            ]

    async def create_organization(
        self, uow: UnitOfWork, org_data: OrganizationCreate
    ) -> Organization:
        async with uow:
            building = await uow.buildings.get_one(id=org_data.building_id)
            if not building:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Здание {org_data.building_id} не найдено'
                )
            scopes = await uow.scopes.filter_by_ids_in(org_data.scopes)
            found_ids = {a.id for a in scopes}
            not_found = set(org_data.scopes) - found_ids
            if not_found:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Виды деятельности {not_found} не найдены'
                )
            organization = await uow.organizations.add_one(
                {
                    'name': org_data.name,
                    'building_id': org_data.building_id
                }
            )
            phones = [
                {
                    'phone_number': phone_number,
                    'organization_id': organization.id
                } for phone_number in org_data.phones
            ]
            await uow.phones.add_multiple(phones)
            organization.scopes = scopes
            await uow.commit()
            await uow.refresh(organization, ['building', 'phones', 'scopes'])
            return OrganizationRead.model_validate(organization)

    async def get_organization_by_id(
        self, uow: UnitOfWork, org_id: int
    ) -> OrganizationRead:
        async with uow:
            organization = await uow.organizations.get_one(id=org_id)
            if not organization:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Организация с таким id не найдена'
                )
            return OrganizationRead.model_validate(organization)

    async def search_by_scopes(
        self, uow: UnitOfWork
    ) -> list[Organization]:
        pass

    async def search_by_name(
        self, uow: UnitOfWork, name: str
    ) -> list[Organization]:
        async with uow:
            organizations = await uow.organizations.get_one(
                name=name
            )
            if not organizations:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Организации по виду деятельности не найдены'
                )
            return organizations

    async def get_organizations_in_radius(
        self, uow: UnitOfWork, lon: float, lat: float, radius: float
    ) -> list[OrganizationRead]:
        async with uow:
            building_ids = await uow.buildings.get_with_radius_ids(lon, lat, radius)
            organizations = await uow.organizations.filter_by_buildings_id(building_ids)
            if not organizations:
                if not organizations:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail='Организации в радиусе не найдены'
                    )
            return [
                OrganizationRead.model_validate(
                    organization
                ) for organization in organizations
            ]

    async def get_organizations_in_rectangle(
        self,
        uow: UnitOfWork,
        lat_min: float,
        lon_min: float,
        lat_max: float,
        lon_max: float
    ) -> list[OrganizationRead]:
        async with uow:
            building_ids = await uow.buildings.get_with_rectangle(
                lat_min,
                lon_min,
                lat_max,
                lon_max
            )
            organizations = await uow.organizations.filter_by_buildings_id(
                building_ids
            )
            if not organizations:
                if not organizations:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail='Организации в прямоугольной области не найдены'
                    )
            return [
                OrganizationRead.model_validate(
                    organization
                ) for organization in organizations
            ]
