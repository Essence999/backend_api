import streamlit as st
import pandas as pd
from sqlalchemy import text
from acesso import ConexaoDB2
from sqlalchemy.orm import Session
from scriptssql import sql_gera_coluna, sql_select_atb

tipoConexao = 'db2'


def lista_coluna(coluna, engine2): 
    #converte os resultados de uma coluna especifica em string
    sql_query_db2 = sql_gera_coluna(coluna)
    with Session(engine2) as session:
        resultado = session.execute(text(sql_query_db2))
        valores_para_mysql = [str(linha[0]) for linha in resultado]
        valores_para_mysql_str = ",".join(f"'{valor}'" for valor in valores_para_mysql)
    return valores_para_mysql_str



#SELECT USANDO A FUNCAO lista_coluna
if tipoConexao == 'db2': 
    engine = ConexaoDB2('db2').conexao()
#     sql_query = f"""
#                     SELECT VL_META_CARD,
# --                 VL_META_IN_MBZ,
#                CD_PRF_CARD,
#                  CD_IND_ATB,
#                  NM_CARD,
#                 REF_AA ,
#                 REF_MM,
#                 TS_ATU
#                     FROM DB2ATB.INFO_CARDS
#                     WHERE CD_PRF_CARD IN ({lista_coluna('CD_PREF_DEP', engine)}) AND 
#                     CD_IND_ATB IN ({lista_coluna('CD_IN_MBZ', engine)}) AND 
#                     REF_AA = YEAR(CURRENT_DATE) AND 
#                     REF_MM = MONTH(CURRENT_DATE)
#                     """

    coluna_pref = lista_coluna('CD_PREF_DEP', engine)
    coluna_in = lista_coluna('CD_IN_MBZ', engine)
    sql_query = sql_select_atb(coluna_pref, coluna_in)


#SELECT USANDO CONEXAO DEV
if tipoConexao == 'dev':
    engine = ConexaoDB2('dev').conexao()
    sql_query = f"""
                    SELECT  DISTINCT *
                    FROM DB2ATB.INFO_CARDS
                    ORDER BY NM_CARD ASC
                    """

def retorna_engine():
    return engine
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

# Função para carregar o DataFrame a partir do banco de dados SQLite
def carregar_dados():
    df = pd.read_sql(sql_query, engine) # cria df do servidor dev
    # df = pd.read-sql(sql_query, engine) # cria df do servidor oficial
    df.columns = df.columns.str.upper()
    return df

