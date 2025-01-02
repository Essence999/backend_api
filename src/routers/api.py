from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from httpx import codes
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.routers.models.ocr import Meta, Regua
from src.services.dao import update_meta_card, update_regua_card
from src.services.ocr import get_ocr_cards_data
from src.services.versions import get_all_versions_data

router = APIRouter(prefix='/api')


def handle_response(
    data, error_message: str = 'Dados não retornados.', status_code: int = codes.INTERNAL_SERVER_ERROR
):
    """Função auxiliar para padronizar o tratamento de erros."""
    if not data:
        raise HTTPException(status_code=status_code, detail=error_message)
    return data


@router.get('/versoes', status_code=codes.OK)
async def get_versions_data(request: Request, session: Session = Depends(get_db)):
    """Endpoint para mostrar dados dos cartões em JSON."""
    token = request.state.token
    data = await get_all_versions_data(session, token=token)
    return handle_response(data)


@router.get('/meta')
async def get_meta_card_data(session: Session = Depends(get_db)):
    data = get_ocr_cards_data(session, 'meta')
    return handle_response(data)


@router.get('/regua')
async def get_regua_card_data(session: Session = Depends(get_db)):
    data = get_ocr_cards_data(session, 'regua')
    return handle_response(data)


@router.put('/meta')
async def update_meta(meta: Meta, session: Session = Depends(get_db)):
    result = update_meta_card(session, meta.new_value, meta.ind, meta.prf)
    if not result:
        raise HTTPException(status_code=codes.BAD_REQUEST,
                            detail='Erro de atualização.')
    return JSONResponse(content={'detail': 'Atualização realizada.'}, status_code=codes.ACCEPTED)


@router.put('/regua')
async def update_regua(regua: Regua, session: Session = Depends(get_db)):
    result = update_regua_card(
        session, regua.vl, regua.qt, regua.ind, regua.prf)
    if not result:
        raise HTTPException(status_code=codes.BAD_REQUEST,
                            detail='Erro de atualização.')
    return JSONResponse(content={'detail': 'Atualização realizada.'}, status_code=codes.ACCEPTED)


@router.delete('/logout')
async def remove_cookie():
    response = JSONResponse(
        content={'detail': 'Logout realizado.'}, status_code=codes.OK)
    response.delete_cookie(key='BBSSOToken', path='/', domain='.bb.com.br')
    return response
