import httpx

url = 'https://services.dipes.intranet.bb.com.br/login/info'


async def validate_token(token: str) -> bool:
    """Valida o token de autenticação."""
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(url, cookies={'BBSSOToken': token})
        if response.status_code != httpx.codes.OK:
            return False
        response_json = response.json()
        if 'AAA4' not in response_json.get('acessos'):
            return False
        return True


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
