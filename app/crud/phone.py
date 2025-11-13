from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Phone

from .base import BaseRepository


class PhoneRepository(BaseRepository[Phone]):

    def __init__(self, session: AsyncSession):
        return super().__init__(session, Phone)

    def _get_stmt(self) -> Select:
        return select(self.model)
