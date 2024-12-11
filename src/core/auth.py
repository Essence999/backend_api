import asyncio

import httpx
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.config import Settings

ACESS_CODE = Settings().API_ACESS_CODE
API_LOGIN_URL = 'https://services.dipes.intranet.bb.com.br/login/info'
WEB_LOGIN_URL = 'https://login.intranet.bb.com.br/sso/XUI/#login&goto='


async def validate_token(token: str) -> bool:
    """Valida o token de autenticação."""
    if not token:
        return False
    async with httpx.AsyncClient(verify=False, timeout=10) as client:
        try:
            response = await client.get(API_LOGIN_URL, cookies={'BBSSOToken': token})
            if response.status_code == httpx.codes.UNAUTHORIZED:
                return False
            response_json = response.json()
            if ACESS_CODE not in response_json.get('acessos'):
                return False
        except Exception:
            return False
    return True


semaphore = asyncio.Semaphore(30)  # Semáforo para requisições concorrentes


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):  # noqa
        async with semaphore:
            token = request.cookies.get('BBSSOToken')

            is_valid = await validate_token(token)
            if not is_valid:
                target_url = request.url
                url = f'{WEB_LOGIN_URL}{target_url}'
                return RedirectResponse(url)

            request.state.token = token
            response = await call_next(request)
            return response
