import asyncio

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from httpx import codes
from sqlalchemy.orm import Session

from src.core.auth import validate_token, AuthMiddleware
from src.core.database import get_db
from src.services.versions_getter import get_all_versions_data

semaphore = asyncio.Semaphore(10)  # Semáforo para requisições concorrentes

app = FastAPI()  # Inicialização do app

# # Configuração de templates e arquivos estáticos
# templates = Jinja2Templates(directory='frontend/templates')
# app.mount('/static', StaticFiles(directory='frontend/static',
#           html=True), name='static')

ORIGINS = ['https://shura.bb.com.br:3000']

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    expose_headers=['*'],
)

app.add_middleware(AuthMiddleware)


@app.get('/versoes', status_code=codes.OK)
async def get_table_page(
    request: Request,
    session: Session = Depends(get_db),
):
    """Endpoint para mostrar dados dos cartões em JSON."""
    token = request.cookies.get('BBSSOToken')
    async with semaphore:
        data = await get_all_versions_data(session, token=token)

    if not data:
        return JSONResponse(
            content={'detail': 'Dados não retornados.'},
            status_code=codes.INTERNAL_SERVER_ERROR
        )
    return data
