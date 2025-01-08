import sqlite3
import pandas as pd
import streamlit as st

def fetch_ufs(conn):
    query = '''
        SELECT DISTINCT
            UF
        FROM
            Municipio
        ORDER BY
            UF
    '''
    return pd.read_sql_query(query, conn)

def fetch_data_by_uf(conn, uf, info_type):
    if info_type == 'Instalações de Transporte':
        query = '''
        SELECT DISTINCT
            T.codigo as Codigo, T.nome as Nome
        FROM
            Instalacao_de_Transporte as T JOIN (SELECT *
                FROM Instalacao_de_Gasoduto as G JOIN Municipio as M
                ON G.codigo_municipio = M.codigo) as GM
        ON
            T.codigo = GM.codigo_transporte
        WHERE GM.UF = ?
        '''
    elif info_type == 'Instalações de Gasoduto':
        query = '''
            SELECT DISTINCT
                G.codigo AS Codigo, 
                G.nome AS Nome
            FROM
                Instalacao_de_Gasoduto AS G
            JOIN Municipio AS M
                ON G.codigo_municipio = M.codigo
            WHERE M.UF = ?
        '''
    else:
        return pd.DataFrame()  

    return pd.read_sql_query(query, conn, params=(uf,))

conn = sqlite3.connect('./Movimentacao_Julho_2021.db')
cursor = conn.cursor()

st.title('Estados')
st.sidebar.markdown('Estados')

st.write('#### Esse trecho representa buscas relacionadas a cada UF, trazendo informações sobre a desejada.')

left_column, right_column = st.columns(2)

ufs_df = fetch_ufs(conn)
UFoption = left_column.selectbox('Selecione a UF', ufs_df['UF'])

infodf = ['Instalações de Transporte', 'Instalações de Gasoduto']
info_option = right_column.selectbox('Selecione a informação desejada', infodf)

data_df = fetch_data_by_uf(conn, UFoption, info_option)

if data_df.empty:
    st.warning(f"Nenhum dado encontrado para UF '{UFoption}' e tipo de informação '{info_option}'.")
else:
    # Renderizar tabela com centralização e ajuste de tamanho
    st.markdown(
        '''
        <style>
            .custom-table-container {
                display: flex;
                justify-content: center; /* Centralizar horizontalmente */
                margin-top: 20px;
            }
            .custom-table-container table {
                width: 80%; /* Ajustar tamanho da tabela */
                text-align: left; /* Alinhar texto à esquerda */
                border-collapse: collapse; /* Unificar bordas */
            }
            .custom-table-container th, .custom-table-container td {
                border: 1px solid #ddd; /* Adicionar borda às células */
                padding: 8px; /* Espaçamento interno das células */
            }
        </style>
        ''',
        unsafe_allow_html=True
    )
    
    # Adicionar tabela dentro de um contêiner centralizado
    st.markdown('<div class="custom-table-container">', unsafe_allow_html=True)
    st.write(data_df.to_html(index=False, escape=False), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
