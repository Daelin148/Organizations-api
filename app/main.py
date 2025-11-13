from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from api.v1.router import api_router
from utils.events import apply_migrations
from utils.exception_handlers import handle_integrity_error
from sqlalchemy.exc import IntegrityError



app = FastAPI(
    title=settings.app_name,
    lifespan=apply_migrations
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*']
)

app.include_router(api_router, prefix='/api/v1')

app.add_exception_handler(IntegrityError, handle_integrity_error)
