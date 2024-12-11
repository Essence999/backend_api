from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session

from src.core.config import Settings

sett = Settings()
uri = f'{sett.DB2_USER}:{sett.DB2_PASS}@{sett.DB2_HOST}:{sett.DB2_PORT}/{sett.DB2_DB}'

engine = create_engine(
    f'ibm_db_sa://{uri}',
    pool_size=10,
    max_overflow=0,
    pool_recycle=1800,
)


def get_db() -> Generator[Session, None, None]:
    """Criação de sessão de banco de dados."""
    with Session(engine) as session:
        yield session
