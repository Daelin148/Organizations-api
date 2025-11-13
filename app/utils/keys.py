from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from core.config import settings


API_KEY_NAME = "X-API-Key"
APP_KEY = settings.api_key

api_key_scheme = APIKeyHeader(name="X-API-Key", auto_error=False)


def verify_api_key(api_key: str = Depends(api_key_scheme)):
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='API ключ не передан'
        )
    if api_key != APP_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='API ключ не валиден'
        )

    return api_key
