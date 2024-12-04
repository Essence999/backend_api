import httpx
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

url = 'https://services.dipes.intranet.bb.com.br/login/info'


async def validate_token(token: str) -> bool:
    """Valida o token de autenticação."""
    if not token:
        return False
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(url, cookies={'BBSSOToken': token})
        if response.status_code == httpx.codes.UNAUTHORIZED:
            return False
        # response_json = response.json()
        # if 'AAA4' not in response_json.get('acessos'):
        #     return False
    return True


origins = [
    'https://shura.bb.com.br:3000',
]


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.cookies.get('BBSSOToken')

        is_valid = await validate_token(token)
        if not is_valid:
            response = JSONResponse(
                status_code=httpx.codes.UNAUTHORIZED,
                content={'detail': 'Token inválido.'}
            )
            origin_url = request.headers.get('origin')
            if origin_url in origins:
                origin_header = {
                    'Access-Control-Allow-Origin': origin_url,
                    'Access-Control-Allow-Credentials': 'true'
                }
                response.headers.update(origin_header)
            return response

        request.state.token = token
        response = await call_next(request)
        return response


# async def validate_token():
#     """Obtém token de autenticação."""
#     async with httpx.AsyncClient(
# verify=False,
# auth=('t1092419',
# '24816326')
# ) as client:
#         response = await client.get(url)
#     json_response = response.json()
#     token = json_response['token']
#     return token
