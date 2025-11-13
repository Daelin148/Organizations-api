from fastapi import APIRouter, Depends

from api.v1.routers import building, organizations, phone, scope
from utils.keys import verify_api_key

api_router = APIRouter(dependencies=([Depends(verify_api_key)]))

api_router.include_router(
    organizations.router,
    prefix='/organizations',
    tags=['organizations']
)

api_router.include_router(
    scope.router,
    prefix='/scopes',
    tags=['scopes']
)

api_router.include_router(
    building.router,
    prefix='/buildings',
    tags=['buildings']
)

api_router.include_router(
    phone.router,
    prefix='/phones',
    tags=['phones']
)
