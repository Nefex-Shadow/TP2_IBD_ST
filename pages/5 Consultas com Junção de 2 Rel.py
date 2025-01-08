import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Consultas com Junção de 2 Rel", layout="wide")

st.title("Consultas Envolvendo Junção de Duas Relações")
st.sidebar.markdown('Consultas com Junção de 2 Rel')

st.header("Três consultas envolvendo junção de duas relações")

st.subheader('Consulta 1')
st.markdown("### Instalações de Transporte em São Paulo")
st.markdown("""
Para essa consulta, temos que unir **Instalacao_de_Transporte** com 
**Instalacao_de_Gasoduto** (Relação "*Pertence*") e também com **Municipio** 
(Relação "*Localização*").

Essa pesquisa encontra as Instalações de Transporte que operam em São Paulo.
Essa pesquisa é interessante para o governo, que busca compreender as atuações 
dessas empresas de movimentação dentro de seu território.
""")

st.code('''query = """
SELECT DISTINCT
    T.codigo as Codigo, T.nome as Nome
FROM
    Instalacao_de_Transporte as T JOIN (SELECT *
        FROM Instalacao_de_Gasoduto as G JOIN Municipio as M
        ON G.codigo_municipio = M.codigo 
        WHERE M.UF = "SP") as GM
ON
    T.codigo = GM.codigo_transporte
WHERE
    GM.UF = "SP";
"""

pr = pd.read_sql_query(query, conn)
pr
''', language="python")

conn = sqlite3.connect('./Movimentacao_Julho_2021.db')
cursor = conn.cursor()

query = """
SELECT DISTINCT
    T.codigo as Codigo, T.nome as Nome
FROM
    Instalacao_de_Transporte as T JOIN (SELECT *
        FROM Instalacao_de_Gasoduto as G JOIN Municipio as M
        ON G.codigo_municipio = M.codigo 
        WHERE M.UF = "SP") as GM
ON
    T.codigo = GM.codigo_transporte
WHERE
    GM.UF = "SP";
"""
df = pd.read_sql_query(query, conn)
st.write(df)


st.subheader('Consulta 2')
st.markdown("### Contratos da Pilar")
st.markdown("""
Para essa consulta, temos que unir **Instalacao_de_Transporte** com 
**Instalacao_de_Gasoduto** (Relação "*Pertence*") e também com **Contrato** 
(Relação "*Contrato*").

Essa pesquisa encontra todos os contratos nos quais a Pilar (Intalação de 
Tranporte) estava envolvido. Útil para traçar as movimentações e eventos 
relacionados com a Pilar
""")

st.code('''query = """
SELECT DISTINCT
    GC.nome as Nome
FROM
    Instalacao_de_Transporte as T JOIN (SELECT C.nome as nome, G.codigo_transporte
    FROM Instalacao_de_Gasoduto as G JOIN Contrato as C
    ON C.codigo_gasoduto = G.codigo
    WHERE C.nome IS NOT NULL) GC
ON
    T.codigo = GC.codigo_transporte
WHERE
    T.nome = "GASBOL"
ORDER BY
    GC.nome;
"""

pr = pd.read_sql_query(query, conn)
pr
''', language="python")

conn = sqlite3.connect('./Movimentacao_Julho_2021.db')
cursor = conn.cursor()

query = """
SELECT DISTINCT
    GC.nome as Nome
FROM
    Instalacao_de_Transporte as T JOIN (SELECT C.nome as nome, G.codigo_transporte
    FROM Instalacao_de_Gasoduto as G JOIN Contrato as C
    ON C.codigo_gasoduto = G.codigo
    WHERE C.nome IS NOT NULL) GC
ON
    T.codigo = GC.codigo_transporte
WHERE
    T.nome = "GASBOL"
ORDER BY
    GC.nome;
"""
df = pd.read_sql_query(query, conn)
st.write(df)

st.subheader('Consulta 3')
st.markdown("### Municípios onde a Petrobrás não operou")
st.markdown("""
Para essa consulta, temos que unir **Carregador** com **Instalacao_de_Gasoduto**
(Relação "*Contrato*") e também com **Municipio** (Relação "*Localização*").

Essa pesquisa encontra todos os municípios onde a Petrobrás não fez 
carregamento. Essa pesquisa serve, por exemplo, para empresas competidoras da 
Petrobrás que gostariam de se estabelecer em cidades onde a Petrobrás não opera.
""")

st.code('''query = """
SELECT DISTINCT
    M.nome as Nome, M.UF as UF
FROM
    Municipio as M LEFT JOIN (SELECT DISTINCT G.codigo_municipio as codigo_municipio
    FROM Instalacao_de_Gasoduto as G JOIN ( SELECT DISTINCT Co.codigo_gasoduto as codigo_gasoduto
        FROM Contrato as Co JOIN Carregador as Ca
        ON Co.codigo_carregador = Ca.codigo
        WHERE Ca.nome = "Petróleo Brasileiro S.A. - PETROBRAS") as C
    ON C.codigo_gasoduto = G.codigo) as GC
ON
    M.codigo = GC.codigo_municipio
WHERE
    GC.codigo_municipio IS NULL
ORDER BY
    M.nome;
"""

pr = pd.read_sql_query(query, conn)
pr
''', language="python")

conn = sqlite3.connect('./Movimentacao_Julho_2021.db')
cursor = conn.cursor()

query = """
SELECT DISTINCT
    M.nome as Nome, M.UF as UF
FROM
    Municipio as M LEFT JOIN (SELECT DISTINCT G.codigo_municipio as codigo_municipio
    FROM Instalacao_de_Gasoduto as G JOIN ( SELECT DISTINCT Co.codigo_gasoduto as codigo_gasoduto
        FROM Contrato as Co JOIN Carregador as Ca
        ON Co.codigo_carregador = Ca.codigo
        WHERE Ca.nome = "Petróleo Brasileiro S.A. - PETROBRAS") as C
    ON C.codigo_gasoduto = G.codigo) as GC
ON
    M.codigo = GC.codigo_municipio
WHERE
    GC.codigo_municipio IS NULL
ORDER BY
    M.nome;
"""
df = pd.read_sql_query(query, conn)
st.write(df)



