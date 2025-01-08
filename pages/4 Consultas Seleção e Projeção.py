import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Consultas Seleção e Projeção", layout="wide")

st.title("Consultas Envolvendo Seleção e Projeção")
st.sidebar.markdown('Consultas Seleção e Projeção')

st.header("Duas consultas envolvendo seleção e projeção")

st.subheader('Consulta 1')
st.markdown("### Instalação de Gasodutos do tipo Recebedor")
st.markdown("""
Essa pesquisa encontra as instalações capazes de receber os recursos. 
Útil para encontrar possibilidades de lugares para enviar ditos recursos.
""")

st.code('''query = """
SELECT DISTINCT
    G.codigo as Codigo, G.nome as Nome
FROM
    Instalacao_de_Gasoduto as G
WHERE
    G.tipo = "Ponto de Recebimento"
ORDER BY
    G.codigo;
"""

pr = pd.read_sql_query(query, conn)
pr
''', language="python")

conn = sqlite3.connect('./Movimentacao_Julho_2021.db')
cursor = conn.cursor()

query = """
SELECT DISTINCT
    G.codigo as Codigo, G.nome as Nome
FROM
    Instalacao_de_Gasoduto as G
WHERE
    G.tipo = "Ponto de Recebimento"
ORDER BY
    G.codigo;
"""
df = pd.read_sql_query(query, conn)
st.write(df)

st.subheader('Consulta 2')
st.markdown("### Contratos que geraram eventos no dia 30 de Julho")
st.markdown("""
Essa pesquisa encontra os contratos por tŕas dos eventos do dia 30. 
Útil para descobrir os responsáveis das movimentações do dia.
""")

st.code('''query = """
SELECT DISTINCT
    C.nome
FROM
    Contrato as C
WHERE
    C.data = "30/07/2021" AND C.nome IS NOT NULL
ORDER BY
    C.nome;
"""

pr = pd.read_sql_query(query, conn)
pr
''', language="python")

conn = sqlite3.connect('./Movimentacao_Julho_2021.db')
cursor = conn.cursor()

query = """
SELECT DISTINCT
    C.nome
FROM
    Contrato as C
WHERE
    C.data = "30/07/2021" AND C.nome IS NOT NULL
ORDER BY
    C.nome;
"""
df = pd.read_sql_query(query, conn)
st.write(df)


