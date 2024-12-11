import streamlit as st
import pandas as pd
from sqlalchemy import text
from acesso import ConexaoDB2
from sqlalchemy.orm import Session
from scriptssql import sql_select_atb, select_regua

# tipoConexao = ''

# #SELECT USANDO A FUNCAO lista_coluna
# if tipoConexao == 'db2' or tipoConexao == 'rga': 
#     engine = ConexaoDB2('db2').conexao()
#     # sql_query = sql_select_atb()


# #SELECT USANDO CONEXAO DEV
# if tipoConexao == 'dev':
#     engine = ConexaoDB2('dev').conexao()
#     sql_query = f"""
#                     SELECT  DISTINCT *
#                     FROM DB2ATB.INFO_CARDS
#                     ORDER BY NM_CARD ASC
#                     """
                    
# if tipoConexao == 'rga':
#     engine = ConexaoDB2('db2').conexao()
#     sql_query = select_regua()

#                     SELECT DENTRO DE SELECT
# sql_query = """SELECT *
#                 FROM DB2ATB.INFO_CARDS
#                 WHERE CD_PRF_CARD IN (SELECT
#                 CD_PREF_DEP
#             FROM
#                 DB2ATB.VS_DVGA_ATB_CARD
#             WHERE
#                 OCR_META = 1) AND 
#                 CD_IND_ATB IN (SELECT
#                 CD_IN_MBZ
#             FROM
#                 DB2ATB.VS_DVGA_ATB_CARD
#             WHERE
#                 OCR_META = 1) AND 
#                 REF_AA = YEAR(CURRENT_DATE) AND 
#                 REF_MM = MONTH(CURRENT_DATE)"""



# COLUNAS PARA MOSTRAR NO FRONT               
# sql_query = """SELECT
#                 CD_PREF_DEP,
#                 CD_IN_MBZ,
#                 CD_IND_ATB,
#                 NM_IN_MBZ,
#                 AA_APRC,
#                 MM_APRC,
#                 VL_META_CARD,
#                 VL_META_IN_MBZ
#             FROM
#                 DB2ATB.VS_DVGA_ATB_CARD
#             WHERE
#                 OCR_META = 1"""


class CriaDF():
    
    def __init__(self, tipo):
        if tipo == 'dev':
            self.engine =  ConexaoDB2('dev').conexao()
        elif tipo == 'db2' or tipo == 'rga':
            self.engine = ConexaoDB2('db2').conexao()
        self.tipo = tipo

    def retorna_engine(self):
        return self.engine
    
    def select_dev(self):
        sql_query = f"""
                        SELECT  DISTINCT *
                        FROM DB2ATB.INFO_CARDS
                        ORDER BY NM_CARD ASC
                        """
        return sql_query

    # Função para carregar o DataFrame a partir do banco de dados SQLite
    def carregar_dados(self):
        if self.tipo == 'db2':
            sql_query = sql_select_atb()
        elif self.tipo == 'rga':
            sql_query = select_regua()
        elif self.tipo == 'dev':
            sql_query = self.select_dev()
        df = pd.read_sql(sql_query, self.engine)
        df.columns = df.columns.str.upper()
        return df

