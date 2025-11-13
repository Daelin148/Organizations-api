from . import BaseSchema

from pydantic import Field, BaseModel

from typing import Annotated


class PhoneBase(BaseModel):
    phone_number: Annotated[str, Field(..., description='Номер телефона')]


class PhoneRead(BaseSchema, PhoneBase):
    pass
