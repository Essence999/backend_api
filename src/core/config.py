from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB2_HOST: str
    DB2_DB: str
    DB2_PORT: str
    DB2_USER: str
    DB2_PASS: str

    # Por padrão, é vazio, ou seja: Não será verificado o acesso.
    API_ACESS_CODE: str = None
