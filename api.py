from fastapi import FastAPI, Response, Request
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from scriptssql import updateScript
from sqlalchemy import text
from geraDf import CriaDF
import httpx
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

#comando para rodar fastapi dev api.py



async def validate_token(token: str) -> bool:
    print('passou aqui')
    """Valida o token de autenticação."""
    url = 'https://services.dipes.intranet.bb.com.br/login/info'
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(url, cookies={'BBSSOToken': token})
        response_json = response.json()
        if "AAA4" not in response_json.get('acessos'):
            return False
        return True



app = FastAPI()
meta = CriaDF('db2')
con_dev = CriaDF('dev')
regua = CriaDF('rga')


@app.middleware('http')
async def check_token_cache(request: Request, call_next):
    """Middleware para verificar token."""
    token = request.cookies.get('BBSSOToken')

    print('o token eh', token)
    # Verifica se o token é None antes de tentar validá-lo
    if token is None:
        return Response(status_code=401, content="Token not found")
    
    # is_valid = await validate_token(token)
    # if not is_valid:
    #     return Response(status_code=403, content="Você não tem acesso a esse conteúdo.")
    
    request.state.token = token
    return await call_next(request)



app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "https://souza.bb.com.br",
    "https://souza.bb.com.br:3000/tabela",
    "https://souza.bb.com.br:3000"
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# app.add_middleware(CookieMiddleware)



@app.get("/meta")
async def root():
    df = meta.carregar_dados()
    df['TS_ATU'] = df['TS_ATU'].astype(str)
    json = df.to_dict(orient='records')
    return json



@app.get("/dev")
async def dev():
    df = con_dev.carregar_dados()
    df['TS_ATU'] = df['TS_ATU'].astype(str)
    json = df.to_dict(orient='records')
    return json

class Valores(BaseModel):
    novo_valor: float
    cd_prf: int
    cd_in: int
    
@app.put('/attdev')
async def devolve_valores(valores: Valores):
    sql_update = updateScript(valores.novo_valor, valores.cd_prf, valores.cd_in)
    print(sql_update)
    alterar_dados(sql_update, con_dev)
    return {"message": "Dados atualizados com sucesso!"}, 200

@app.get("/regua")
async def rga():
    df = regua.carregar_dados()
    df['TS_ATU'] = df['TS_ATU'].astype(str)
    json = df.to_dict(orient='records')
    return json

# @app.post("attregua")
# async def att_rga(novo_valor, cd_prf, cd_in):
#     sql_update = updateScript(novo_valor, cd_prf, cd_in)
#     print(sql_update)
#     alterar_dados(sql_update, con_dev)
#     return {"message": "Dados atualizados com sucesso!"}, 200

# @app.post('attmeta')
# async def att_meta(novo_valor, cd_prf, cd_in):
#     sql_update = updateScript(novo_valor, cd_prf, cd_in)
#     print(sql_update)
#     alterar_dados(sql_update, con_dev)
#     return {"message": "Dados atualizados com sucesso!"}, 200
    

def alterar_dados(sql_update, con):
    engine = con.retorna_engine()
    try:
        with engine.begin() as connection:
            connection.execute(text(sql_update))
    except Exception as e:
        # raise HTTPException(status_code=400, detail=str(e))
        print(str(e))
        
build_dir = r'/home/wsl/Downloads/front-end-meta/meu-app/build'
@app.get('/{full_path:path}')
async def serve_react_app(full_path: str):
    """Endpoint para lidar com os arquivos do React."""
    if full_path.startswith('static'):
        return FileResponse(f'{build_dir}/{full_path}')
    else:
        return FileResponse(f'{build_dir}/index.html')