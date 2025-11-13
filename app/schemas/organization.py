from typing import Annotated

from pydantic import BaseModel, Field

from .base import BaseSchema
from .phone import PhoneRead
from .scope import ScopeRead


class OrganizationCreate(BaseModel):
    name: Annotated[str, Field(description='Наименование организации')]
    building_id: Annotated[int, Field(description='Идентификатор здания')]
    phones: Annotated[list[str], Field(description='Номера телефонов')]
    scopes: Annotated[list[int], Field(
        description='Идентификаторы видов деятельности'
    )]


class OrganizationRead(BaseSchema):
    name: Annotated[str, Field(description='Наименование организации')]
    building: Annotated[
        'BuildingRead', Field(description='Здание организации')
    ]
    phones: Annotated[list[PhoneRead], Field(
        description='Номера телефонов организации'
    )]
    scopes: Annotated[list[ScopeRead], Field(
        description='Виды деятельности организации'
    )]
