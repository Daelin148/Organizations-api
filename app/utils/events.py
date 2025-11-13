from contextlib import asynccontextmanager
from fastapi import FastAPI
import subprocess


@asynccontextmanager
async def apply_migrations(app: FastAPI):
    print("Применяем миграции...")
    try:
        result = subprocess.run(
            ['alembic', '-c', '/app/app/alembic.ini', 'upgrade', 'head'],
            capture_output=True,
            text=True,
            check=True,
            cwd='/app'
        )
    except subprocess.CalledProcessError as e:
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        raise
    print("Миграции успешно применены")
    yield
