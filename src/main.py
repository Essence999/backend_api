from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.core.auth import AuthMiddleware
from src.routers import api

app = FastAPI()  # Inicialização do app

app.add_middleware(AuthMiddleware)

app.include_router(api.router)

app.mount('/', StaticFiles(directory='static', html=True))
