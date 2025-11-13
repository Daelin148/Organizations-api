from typing import Annotated

from pydantic import BaseModel, Field

from . import BaseSchema


class PhoneBase(BaseModel):
    phone_number: Annotated[str, Field(..., description='Номер телефона')]


class PhoneRead(BaseSchema, PhoneBase):
    pass
