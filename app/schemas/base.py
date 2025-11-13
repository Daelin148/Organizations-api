from pydantic import BaseModel
from typing import Annotated
from pydantic import Field


class BaseSchema(BaseModel):
    id: Annotated[int, Field(description='Уникальный идентификатор')]

    class Config:
        from_attributes = True
