import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from acesso import ConexaoDF

# Função para carregar o DataFrame a partir do banco de dados SQLite
def carregar_dados():
    teste = ConexaoDF()
    df = teste.conexao()
    return df

df = carregar_dados()


# Função para atualizar o banco de dados SQLite com o novo valor
def atualizar_banco_dados(df):
    engine = create_engine('sqlite:///sqlite.db') #usar o arq acesso.py, aqui talvez
    df.to_sql('minha_tabela', engine, if_exists='append', index=False)


# Exibir o DataFrame original
st.write("DataFrame original:")
st.dataframe(df, use_container_width=True)



# Entradas do usuário
index_para_alterar = st.number_input("Digite o índice da linha que deseja alterar:", min_value=0, max_value=len(df)-1, step=1)
coluna_para_alterar = st.selectbox("Escolha a coluna que deseja alterar:", df.columns)
novo_valor = st.text_input(f"Digite o novo valor para a coluna {coluna_para_alterar}:")

# Botão para enviar a atualização
if st.button("Enviar"):
    df.at[index_para_alterar, coluna_para_alterar] = novo_valor
    atualizar_banco_dados(df)
    st.write("DataFrame atualizado:")
    st.rerun()
    st.success("O banco de dados foi atualizado com sucesso.")
