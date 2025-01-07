import sqlite3
import pandas as pd
import streamlit as st

conn = sqlite3.connect('./Movimentacao_Julho_2021.db')
cursor = conn.cursor()

st.title('Contratos')
st.sidebar.markdown('Contratos')


query = '''
    SELECT DISTINCT
        M.nome as nome
    FROM
        Municipio as M
    ORDER BY
        M.nome
'''

df = pd.read_sql_query(query, conn)

municipios = st.multiselect(
    "Escolha o Município", list(df['nome']), [df['nome'].values[0]]
)
if not municipios:
    st.error("Por favor, selecione um Município.")

st.write(municipios)

query = '''
SELECT DISTINCT
    C.variavel as variavel
FROM
    Contrato as C
ORDER BY
    C.variavel
'''

df = pd.read_sql_query(query, conn)

variaveis = st.selectbox(
    "Escolha a variável do Contrato", list(df['variavel'])
)

for m in municipios:
    query = ('''
    SELECT DISTINCT
        M.mun_nome as Nome, C.data as Data, SUM(C.valor) as Valor
    FROM
        Contrato as C JOIN (SELECT DISTINCT M.nome as mun_nome, G.codigo as gas_codigo
            FROM Instalacao_de_Gasoduto as G JOIN Municipio as M
            ON G.codigo_municipio = M.codigo
            WHERE M.nome = "replace_mun") as M
    ON
        M.gas_codigo = C.codigo_gasoduto
    WHERE
        C.variavel = "replace_var"
    GROUP BY
        M.mun_nome, C.data
    ORDER BY
        M.mun_nome
    ''').replace('replace_mun', m).replace('replace_var', variaveis)
    df = pd.read_sql_query(query, conn)
    print(df)
    df.pivot(index='Nome', columns='Data', values='Valor')
    print(df)
    st.write(df)
