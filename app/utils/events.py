import subprocess
from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def apply_migrations(app: FastAPI):
    print("Применяем миграции...")
    try:
        subprocess.run(
            ['alembic', '-c', '/app/app/alembic.ini', 'upgrade', 'head'],
            capture_output=True,
            text=True,
            check=True,
            cwd='/app'
        )
    except subprocess.CalledProcessError:
        raise
    print("Миграции успешно применены")
    yield
