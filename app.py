import streamlit as st
import pandas as pd
from sqlalchemy import text, Table, MetaData, Column, update, Float, Integer, Date
from geraDf import carregar_dados, retorna_engine
from st_aggrid import AgGrid, GridOptionsBuilder
from data import data
from acesso import ConexaoDB2
from scriptssql import updateScript
import time

df = carregar_dados()
engine = retorna_engine()

st.write("DataFrame original:")
st.dataframe(df, use_container_width=True)

# Entradas do usuário
index_para_alterar = st.number_input("Digite o índice da linha que deseja alterar:", min_value=0, max_value=len(df)-1, step=1)
# coluna_para_alterar = st.selectbox("Escolha a coluna que deseja alterar:", [1,2,3])
novo_valor = st.number_input(f"Digite o novo valor para a linha", format='%f')

def atualizar_dados():
    
    sql_update = updateScript(novo_valor, df, index_para_alterar)
    with engine.begin() as connection:
        connection.execute(text(sql_update))

# Botão para enviar a atualização
if st.button("Enviar"):
    if df.loc[index_para_alterar, 'VL_META_CARD'] != novo_valor:
        df.at[index_para_alterar, 'VL_META_CARD'] = novo_valor
        atualizar_dados()
        st.write("DataFrame atualizado:")
        st.dataframe(df, use_container_width=True)
        st.success("O banco de dados foi atualizado com sucesso.")
        time.sleep(10)
        st.rerun()
    else:
        st.error("Insira outro valor")