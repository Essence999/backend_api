from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.core.auth import AuthMiddleware
from src.core.log import setup_logging
from src.routers import api

setup_logging()

BASE_PREFIX = '/intc_cnxo'

app = FastAPI(root_path=BASE_PREFIX)

app.include_router(api.router)

app.mount('/', StaticFiles(directory='static', html=True))

app.add_middleware(AuthMiddleware)
