from fastapi import FastAPI

from src.core.auth import AuthMiddleware
from src.routers import api

app = FastAPI()  # Inicialização do app

app.include_router(api.router)

app.add_middleware(AuthMiddleware)

BUILD_DIR = '/home/wsl/Downloads/frontend/build'


# @app.get('/{full_path:path}')
# async def serve_react_app(full_path: str):
#     """Endpoint para lidar com os arquivos do React."""
#     if full_path.startswith('static'):
#         return FileResponse(f'{BUILD_DIR}/{full_path}')
#     else:
#         return FileResponse(f'{BUILD_DIR}/index.html')
