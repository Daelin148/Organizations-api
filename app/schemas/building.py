from .base import BaseSchema

from pydantic import Field, BaseModel, computed_field

from typing import Annotated


class BuildingBase(BaseModel):
    address: Annotated[str, Field(description='Адрес здания')]
    latitude: Annotated[float, Field(description='Широта')]
    longitude: Annotated[float, Field(description='Долгота')]


class BuildingCreate(BuildingBase):

    @computed_field
    @property
    def geog(self) -> int:
        return f'POINT({self.longitude} {self.latitude})'


class BuildingRead(BaseSchema, BuildingBase):
    pass


class BuildingOrganizations(BaseSchema, BuildingBase):
    organizations: Annotated[
        list['OrganizationRead'], Field(description='Организации в здании')
    ]
