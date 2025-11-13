from . import BaseSchema

from typing import Annotated

from pydantic import Field, BaseModel


class ScopeBase(BaseModel):
    name: Annotated[str, Field(description='Название')]
    parent_id: Annotated[int | None, Field(
        description='Идентификатор родительского вида деятельности'
    )]


class ScopeRead(BaseSchema, ScopeBase):
    pass


class ScopeOrganizations(BaseSchema, ScopeBase):
    organizations: Annotated[
        list['OrganizationRead'],
        Field(description='Организации по виду деятельности')
    ]
