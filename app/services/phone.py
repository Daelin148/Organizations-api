from models import Phone
from schemas.phone import PhoneRead
from utils.unitofwork import UnitOfWork


class PhoneService:

    async def get_phones(self, uow: UnitOfWork) -> list[PhoneRead]:
        async with uow:
            phones = await uow.phones.get_all()
            return [PhoneRead.model_validate(phone) for phone in phones]
