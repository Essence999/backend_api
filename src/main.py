import asyncio

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from httpx import codes
from sqlalchemy.orm import Session

from src.core.auth import validate_token
from src.core.database import get_db
from src.services.versions_getter import get_all_versions_data

semaphore = asyncio.Semaphore(10)  # Semáforo para requisições concorrentes

app = FastAPI()  # Inicialização do app

ORIGINS = ['https://shura.bb.com.br']


# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    expose_headers=['*'],
)


@app.middleware('http')
async def auth_and_error_middleware(request: Request, call_next):
    """Middleware para verificar token."""
    token = request.cookies.get('BBSSOToken')
    try:
        is_valid = await validate_token(token)
        if not is_valid:
            raise HTTPException(
                status_code=codes.UNAUTHORIZED, detail='Token inválido.'
            )
        request.state.token = token
        return await call_next(request)
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={'detail': e.detail},
            # headers={
            #     'Access-Control-Allow-Origin': ,
            #     'Access-Control-Allow-Credentials': 'true',
            #     'Access-Control-Allow-Methods': '*',
            #     'Access-Control-Allow-Headers': '*',
            # },
        )


@app.get('/versoes', status_code=codes.OK)
async def get_table_page(
    request: Request,
    session: Session = Depends(get_db),
):
    """Endpoint para mostrar dados dos cartões em JSON."""
    async with semaphore:
        data = await get_all_versions_data(session, token=request.state.token)
    data = None
    if not data:
        raise HTTPException(
            status_code=codes.INTERNAL_SERVER_ERROR,
        )
    return data
