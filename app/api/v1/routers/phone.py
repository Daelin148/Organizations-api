from fastapi import APIRouter

from api.v1.dependencies import UOWDep
from schemas import PhoneRead
from services import PhoneService

router = APIRouter()


@router.get('/', response_model=list[PhoneRead])
async def get_phones(
    uow: UOWDep
) -> list[PhoneRead]:
    """Вывод информации о телефонах."""
    async with uow:
        phones = await PhoneService().get_phones(uow)
        return phones
