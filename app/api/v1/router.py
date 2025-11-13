from fastapi import APIRouter

from api.v1.routers import building, organizations, phone, scope

api_router = APIRouter()

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
