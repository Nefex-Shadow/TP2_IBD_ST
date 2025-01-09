import sqlite3
import pandas as pd
import streamlit as st

def fetch_contratos(conn):
    query = '''
        SELECT DISTINCT
            nome
        FROM
            Contrato
        ORDER BY
            nome
    '''
    return pd.read_sql_query(query, conn)

def fetch_data_by_uf(conn, uf, info_type):
    if info_type == 'Operador':
        query = '''
        SELECT DISTINCT
            O.codigo as Codigo, O.nome as Nome
        FROM
            Operador as O JOIN Contrato as C 
        ON O.codigo = C.codigo_operador
        WHERE C.nome = ?
        '''
    elif info_type == 'Carregador':
        query = '''
            SELECT DISTINCT
            Ca.codigo as Codigo, Ca.nome as Nome
        FROM
            Carregador as Ca JOIN Contrato as C 
        ON Ca.codigo = C.codigo_carregador
        WHERE C.nome = ?
        '''
    else:
        return pd.DataFrame()  

    return pd.read_sql_query(query, conn, params=(uf,))

conn = sqlite3.connect('./Movimentacao_Julho_2021.db')
cursor = conn.cursor()

st.title('Funcionários')
st.sidebar.markdown('Funcionários')

st.write('#### Esse trecho representa buscas relacionadas a cada contrato, trazendo informações seus operadores e carregadores.')

left_column, right_column = st.columns(2)

contratos_df = fetch_contratos(conn)
contratos_option = left_column.selectbox('Selecione o contrato', contratos_df['nome'])

infodf = ['Operador', 'Carregador']
info_option = right_column.selectbox('Selecione a informação desejada', infodf)

data_df = fetch_data_by_uf(conn, contratos_option, info_option)

if data_df.empty:
    st.warning(f"Nenhum dado encontrado para '{contratos_option}' e '{info_option}'.")
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
