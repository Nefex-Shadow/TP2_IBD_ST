import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Consultas com Junção de 3+ Rel", layout="wide")

st.title("Consultas Envolvendo Junção de Três ou mais Relações")
st.sidebar.markdown('Consultas com Junção de 3+ Rel')

st.header("Três consultas envolvendo junção de três ou mias realações")

st.subheader('Consulta 1')
st.markdown("""### Instalações de Transporte que participaram de Solicitações de Volume no Rio de Janeiro no dia 15 de Julho.""")
st.markdown("""
Essa pesquisa serve para encontrar as Instalações de Transporte cujas 
Instalações de Gasoduto fizeram solicitações de recurso. Útil para verificação quanto foi pedido para 
verificação posterior de validação dos contratos
""")

st.code('''query = """
SELECT DISTINCT
    T.codigo as Codigo, T.nome as Nome, SUM(MCG.valor) as Total_Valor
FROM
    Instalacao_de_Transporte as T JOIN 
    (SELECT DISTINCT *
    FROM Municipio as M JOIN
        (SELECT DISTINCT *
        FROM Contrato as C JOIN Instalacao_de_Gasoduto as G
        ON C.codigo_gasoduto = G.codigo
        WHERE C.variavel = "Volume Solicitado" AND C.data = "15/07/2021") as CG
    ON CG.codigo_municipio = M.codigo
    WHERE M.UF = "RJ") as MCG
ON
    T.codigo = MCG.codigo_transporte
GROUP BY
    T.codigo
ORDER BY
    SUM(MCG.valor) DESC;
"""

pr = pd.read_sql_query(query, conn)
pr
''', language="python")

conn = sqlite3.connect('./Movimentacao_Julho_2021.db')
cursor = conn.cursor()

query = """
SELECT DISTINCT
    T.codigo as Codigo, T.nome as Nome, SUM(MCG.valor) as Total_Valor
FROM
    Instalacao_de_Transporte as T JOIN 
    (SELECT DISTINCT *
    FROM Municipio as M JOIN
        (SELECT DISTINCT *
        FROM Contrato as C JOIN Instalacao_de_Gasoduto as G
        ON C.codigo_gasoduto = G.codigo
        WHERE C.variavel = "Volume Solicitado" AND C.data = "15/07/2021") as CG
    ON CG.codigo_municipio = M.codigo
    WHERE M.UF = "RJ") as MCG
ON
    T.codigo = MCG.codigo_transporte
GROUP BY
    T.codigo
ORDER BY
    SUM(MCG.valor) DESC;
"""
df = pd.read_sql_query(query, conn)
st.write(df)


st.subheader('Consulta 2')
st.markdown("""### Instalação de Transporte que operam na Região Sul com maior quantidade de Contratos no dia 7 de Julho.""")
st.markdown("""
Essa pesquisa encontra as Instalações de Transporte operando na 
Região Sul cujos contratos levaram a eventos o dia 7 de Julho, 
junto da quantidade desses contratos por Transporte. Útil para 
descobrir as Instalações de Transporte que tiveram movimentação 
nesse dia.
""")

st.code('''query = """
SELECT DISTINCT
    T.codigo as Codigo, T.nome as Nome, COUNT(MCG.nome) as Num_Contratos
FROM
    Instalacao_de_Transporte as T JOIN
    (SELECT DISTINCT CG.nome as nome, CG.codigo_transporte as codigo_transporte
    FROM Municipio as M JOIN
        (SELECT DISTINCT C.nome as nome, G.codigo_municipio as codigo_municipio, G.codigo_transporte as codigo_transporte
        FROM Contrato as C JOIN Instalacao_de_Gasoduto as G
        ON C.codigo_gasoduto = G.codigo
        WHERE C.data = "07/07/2021") as CG
    ON CG.codigo_municipio = M.codigo
    WHERE M.UF = "RS" OR M.UF = "SC" OR M.UF = "PR") as MCG
ON
    T.codigo = MCG.codigo_transporte
GROUP BY
    T.codigo
ORDER BY
    COUNT(MCG.nome) DESC;
"""

pr = pd.read_sql_query(query, conn)
pr
''', language="python")

conn = sqlite3.connect('./Movimentacao_Julho_2021.db')
cursor = conn.cursor()

query = """
SELECT DISTINCT
    T.codigo as Codigo, T.nome as Nome, COUNT(MCG.nome) as Num_Contratos
FROM
    Instalacao_de_Transporte as T JOIN
    (SELECT DISTINCT CG.nome as nome, CG.codigo_transporte as codigo_transporte
    FROM Municipio as M JOIN
        (SELECT DISTINCT C.nome as nome, G.codigo_municipio as codigo_municipio, G.codigo_transporte as codigo_transporte
        FROM Contrato as C JOIN Instalacao_de_Gasoduto as G
        ON C.codigo_gasoduto = G.codigo
        WHERE C.data = "07/07/2021") as CG
    ON CG.codigo_municipio = M.codigo
    WHERE M.UF = "RS" OR M.UF = "SC" OR M.UF = "PR") as MCG
ON
    T.codigo = MCG.codigo_transporte
GROUP BY
    T.codigo
ORDER BY
    COUNT(MCG.nome) DESC;
"""
df = pd.read_sql_query(query, conn)
st.write(df)

st.subheader('Consulta 3')
st.markdown("""### Carregadores que já trabalharam para GASBEL e GASBEL II fora de Minas Gerais.""")
st.markdown("""
Essa pesquisa encontra os Carregadores que já fecharam contrato com 
a GASBEL E GASBEL II em um trabalho fora de Minas Gerais. Como 
GASBEL e GASBEL II atuam primariamente em Minas Gerias, julga-se 
interessante para a empresa olhar para fora e analisar novas 
oportunidades sem repetir lugares já passados.
""")

st.code('''query = """
SELECT DISTINCT
    MCG.ca_codigo as Codigo, MCG.ca_nome as Nome, MCG.mun_nome as Municipio, MCG.mun_UF as UF
FROM
    Instalacao_de_Transporte as T JOIN
    (SELECT DISTINCT CG.ca_codigo as ca_codigo, CG.ca_nome as ca_nome, CG.codigo_transporte as codigo_transporte, M.nome as mun_nome, M.UF as mun_UF
    FROM Municipio as M JOIN
        (SELECT DISTINCT C.ca_codigo as ca_codigo, C.ca_nome as ca_nome, G.codigo_transporte as codigo_transporte, G.codigo_municipio as codigo_municipio
        FROM Instalacao_de_Gasoduto as G JOIN (SELECT DISTINCT Ca.codigo as ca_codigo, Ca.nome as ca_nome, Co.codigo_gasoduto as codigo_gasoduto
            FROM Carregador as Ca JOIN Contrato as Co
            ON Ca.codigo = Co.codigo_carregador) C
        ON C.codigo_gasoduto = G.codigo) as CG
    ON CG.codigo_municipio = M.codigo
    WHERE M.UF != "MG") as MCG
ON
    T.codigo = MCG.codigo_transporte
WHERE
    T.nome = "GASBEL" OR T.nome = "GASBEL II"
ORDER BY
    MCG.ca_codigo DESC;
"""

pr = pd.read_sql_query(query, conn)
pr
''', language="python")

conn = sqlite3.connect('./Movimentacao_Julho_2021.db')
cursor = conn.cursor()

query = """
SELECT DISTINCT
    MCG.ca_codigo as Codigo, MCG.ca_nome as Nome, MCG.mun_nome as Municipio, MCG.mun_UF as UF
FROM
    Instalacao_de_Transporte as T JOIN
    (SELECT DISTINCT CG.ca_codigo as ca_codigo, CG.ca_nome as ca_nome, CG.codigo_transporte as codigo_transporte, M.nome as mun_nome, M.UF as mun_UF
    FROM Municipio as M JOIN
        (SELECT DISTINCT C.ca_codigo as ca_codigo, C.ca_nome as ca_nome, G.codigo_transporte as codigo_transporte, G.codigo_municipio as codigo_municipio
        FROM Instalacao_de_Gasoduto as G JOIN (SELECT DISTINCT Ca.codigo as ca_codigo, Ca.nome as ca_nome, Co.codigo_gasoduto as codigo_gasoduto
            FROM Carregador as Ca JOIN Contrato as Co
            ON Ca.codigo = Co.codigo_carregador) C
        ON C.codigo_gasoduto = G.codigo) as CG
    ON CG.codigo_municipio = M.codigo
    WHERE M.UF != "MG") as MCG
ON
    T.codigo = MCG.codigo_transporte
WHERE
    T.nome = "GASBEL" OR T.nome = "GASBEL II"
ORDER BY
    MCG.ca_codigo DESC;
"""
df = pd.read_sql_query(query, conn)
st.write(df)



