from typing import Annotated

from fastapi import Depends

from utils.keys import verify_api_key
from utils.unitofwork import UnitOfWork


UOWDep = Annotated[UnitOfWork, Depends(UnitOfWork)]
