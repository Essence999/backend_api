from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles

from src.core.auth import AuthMiddleware
from src.routers import api

BASE_PREFIX = '/intc_cnxo'

app = FastAPI()  # Inicialização do app

main_router = APIRouter(prefix=BASE_PREFIX)
main_router.include_router(api.router)
app.include_router(main_router)

app.mount(f'{BASE_PREFIX}', StaticFiles(directory='static', html=True))

app.add_middleware(AuthMiddleware)
