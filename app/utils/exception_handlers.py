from fastapi.responses import JSONResponse
from asyncpg.exceptions import UniqueViolationError


async def handle_integrity_error(request, exc):

    if exc.orig.sqlstate == UniqueViolationError.sqlstate:
        return JSONResponse(
            status_code=400,
            content={"detail": "Объект с переданными данными уже существует."}
        )
    return JSONResponse(
            status_code=400,
            content={"detail": "Ошибка целостности данных."}
        )
