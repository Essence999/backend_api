import pandas as pd
from sqlalchemy import create_engine
from usuario import Usuario

class ConexaoDB2:
    """
        usa a classe IDMBConnection para fazer a conexao
        possui apenas um metodo que retorna o DF com os dados da query aqui inserida
    """
    def __init__(self, tipo: str):
        # self.user = user
        # self.senha = senha
        self.tipo = tipo


    def conexao(self):
                
        userDB2 = Usuario(self.tipo)

        db2_url = f'ibm_db_sa://{userDB2.username}:{userDB2.password}@{userDB2.hostname}:{userDB2.port}/SUPEROP'

        engine_db2 = create_engine(db2_url)
            
        return engine_db2