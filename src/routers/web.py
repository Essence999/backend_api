from fastapi import APIRouter
from fastapi.responses import FileResponse

BUILD_DIR = '/home/wsl/Downloads/front-end-incon/build'

router = APIRouter(prefix='')


@router.get('/{full_path:path}')
async def serve_react_app(full_path: str):
    """Endpoint para lidar com os arquivos do React."""
    if full_path.startswith('static'):
        return FileResponse(f'{BUILD_DIR}/{full_path}')
    else:
        return FileResponse(f'{BUILD_DIR}/index.html')
