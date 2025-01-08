import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Consultas Agregação sobre Junção", layout="wide")

st.title("Consultas Envolvendo Agregação sobre Junção de Duas ou Mais Relações")
st.sidebar.markdown('Consultas Agregação sobre Junção')

st.header("Duas consultas envolvendo agregação sobre junção de duas ou mais relações")

st.subheader('Consulta 1')
st.markdown("""### Municípios com maior valor de Volume Realizado""")
st.markdown("""
Para essa consulta, temos que unir **Contrato** com 
**Instalacao_de_Gasoduto** (Relação "*Contrato*") e também com 
**Municipio** (Relação "*Localização*").

Essa pesquisa encontra os Municipios com maior volume de recursos utilizados. 
Ela é interessante para analisar municípios produtíveis quanto às suas 
operações.
""")

st.code('''query = """
SELECT DISTINCT
    M.nome as Nome, M.UF as UF, SUM(GC.valor) as Valor_Acumulado
FROM
    Municipio as M JOIN (SELECT DISTINCT G.codigo_municipio as codigo_municipio, C.data as data, C.valor as Valor
    FROM Instalacao_de_Gasoduto as G JOIN Contrato as C
    ON C.codigo_gasoduto = G.codigo
    WHERE C.variavel = "Volume Realizado") as GC
ON
    M.codigo = GC.codigo_municipio
GROUP BY
    M.codigo
ORDER BY
    SUM(GC.valor) DESC;
"""

pr = pd.read_sql_query(query, conn)
pr
''', language="python")

conn = sqlite3.connect('./Movimentacao_Julho_2021.db')
cursor = conn.cursor()

query = """
SELECT DISTINCT
    M.nome as Nome, M.UF as UF, SUM(GC.valor) as Valor_Acumulado
FROM
    Municipio as M JOIN (SELECT DISTINCT G.codigo_municipio as codigo_municipio, C.data as data, C.valor as Valor
    FROM Instalacao_de_Gasoduto as G JOIN Contrato as C
    ON C.codigo_gasoduto = G.codigo
    WHERE C.variavel = "Volume Realizado") as GC
ON
    M.codigo = GC.codigo_municipio
GROUP BY
    M.codigo
ORDER BY
    SUM(GC.valor) DESC;
"""
df = pd.read_sql_query(query, conn)
st.write(df)


st.subheader('Consulta 2')
st.markdown("""### Quantidade de Município em que cada Instalação de Transporte opera""")
st.markdown("""
Para essa consulta, temos que unir **Instalacao_de_Transporte** com 
**Instalacao_de_Gasoduto** (Relação "*Pertence*") e também com **Municipio** 
(Relação "*Localização*").
            
Essa pesquisa encontra a quantidade de municípios ligados as Instalações de 
Tansporte. Útil para compará-las quanto ao seu alcance e influência nas 
regiões.  
""")

st.code('''query = """
SELECT DISTINCT
    T.codigo as Codigo, T.nome as Nome, COUNT(GM.codigo) as Num_Municipio
FROM
    Instalacao_de_Transporte as T JOIN (SELECT DISTINCT M.codigo as codigo, G.codigo_transporte as codigo_transporte
        FROM Instalacao_de_Gasoduto as G JOIN Municipio as M
        ON G.codigo_municipio = M.codigo) as GM
ON
    T.codigo = GM.codigo_transporte
GROUP BY
    T.codigo
ORDER BY
    COUNT (GM.codigo) DESC;
"""

pr = pd.read_sql_query(query, conn)
pr
''', language="python")

conn = sqlite3.connect('./Movimentacao_Julho_2021.db')
cursor = conn.cursor()

query = """
SELECT DISTINCT
    T.codigo as Codigo, T.nome as Nome, COUNT(GM.codigo) as Num_Municipio
FROM
    Instalacao_de_Transporte as T JOIN (SELECT DISTINCT M.codigo as codigo, G.codigo_transporte as codigo_transporte
        FROM Instalacao_de_Gasoduto as G JOIN Municipio as M
        ON G.codigo_municipio = M.codigo) as GM
ON
    T.codigo = GM.codigo_transporte
GROUP BY
    T.codigo
ORDER BY
    COUNT (GM.codigo) DESC;
"""
df = pd.read_sql_query(query, conn)
st.write(df)





