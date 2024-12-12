from fastapi import FastAPI

from src.core.auth import AuthMiddleware
from src.routers import api, web

app = FastAPI()  # Inicialização do app

app.add_middleware(AuthMiddleware)

app.include_router(api.router)
app.include_router(web.router)
