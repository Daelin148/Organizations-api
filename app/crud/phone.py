from sqlalchemy import select
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from .base import BaseRepository
from models import Phone


class PhoneRepository(BaseRepository[Phone]):

    def __init__(self, session: AsyncSession):
        return super().__init__(session, Phone)

    def _get_stmt(self) -> Select:
        return select(self.model)
