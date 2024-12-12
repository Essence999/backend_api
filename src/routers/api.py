from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from httpx import codes
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.services.dao import update_meta_card, update_regua_card
from src.services.ocr import get_ocr_cards_data
from src.services.versions import get_all_versions_data

router = APIRouter(prefix='/api')


@router.get('/versoes', status_code=codes.OK)
async def get_versions_data(
    request: Request,
    session: Session = Depends(get_db),
):
    """Endpoint para mostrar dados dos cartões em JSON."""
    token = request.state.token
    data = await get_all_versions_data(session, token=token)

    if not data:
        return JSONResponse(
            content={'detail': 'Dados não retornados.'},
            status_code=codes.INTERNAL_SERVER_ERROR,
        )
    return data


@router.get('/ocr/{type}')
async def get_ocr_data(type: str, session: Session = Depends(get_db)):
    data = get_ocr_cards_data(session, type)
    if data is None:
        return JSONResponse(
            content={'detail': 'Requisição inválida.'}, status_code=codes.BAD_REQUEST
        )
    return data


@router.put('/ocr/meta')
async def update_meta(
    new_value: float, ind: int, prf: int, session: Session = Depends(get_db)
):
    result: bool = update_meta_card(session, new_value, ind, prf)
    if not result:
        return JSONResponse(
            content={'detail': 'Erro de atualização.'}, status_code=codes.BAD_REQUEST
        )
    return JSONResponse(
        content={'detail': 'Atualização realizada.'}, status_code=codes.ACCEPTED
    )


@router.put('/ocr/regua')
async def update_regua(
    new_value: str, ind: int, prf: int, session: Session = Depends(get_db)
):
    result: bool = update_regua_card(session, new_value, ind, prf)
    if not result:
        return JSONResponse(
            content={'detail': 'Erro de atualização.'}, status_code=codes.BAD_REQUEST
        )
    return JSONResponse(
        content={'detail': 'Atualização realizada.'}, status_code=codes.ACCEPTED
    )
