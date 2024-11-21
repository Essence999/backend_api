from fastapi import FastAPI
import pandas as pd
from acesso import ConexaoDB2
from geraDf import carregar_dados
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Response
#comando para rodar fastapi dev api.py

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:3001/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/items")
async def root():
    df = carregar_dados()
    df['TS_ATU'] = df['TS_ATU'].astype(str)
    json = df.to_json()
    return Response(content=json, media_type="application/json")

# @app.post("/login")
# async def login(user, senha):
#         try:
            
#     return 0