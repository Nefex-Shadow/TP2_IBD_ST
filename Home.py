import io
import sqlite3
import pandas as pd
import streamlit as st
import numpy
import csv

conn = sqlite3.connect('./Movimentacao_Julho_2021.db')
cursor = conn.cursor()

st.title('Trabalho Prático 2')
st.sidebar.markdown("Home")

# # 6. Consultas
# 
# ## 6.1 Duas consultas envolvendo seleção e projeção
# 
# ### 6.1.1 Consulta 1
# **Instalação de Gasodutos do tipo Recebedor**
# 
# Essa pesquisa encontra as instalações capazes de receber os recursos. Útil para encontrar possibilidades de lugares para enviar ditos recursos.

# In[5]:

left_column, right_column = st.columns(2)

query = '''
SELECT
    T.codigo as Codigo, T.nome as Nome
FROM
    Instalacao_de_Transporte as T
'''

df = pd.read_sql_query(query, conn)
option = left_column.selectbox(
    'Selecione o Nome',
     df['Nome'])

query = ('''
SELECT
    T.codigo as Codigo, T.nome as Nome
FROM
    Instalacao_de_Transporte as T
WHERE
    T.nome = "replace"
''').replace('replace', option)
df = pd.read_sql_query(query, conn)
right_column.write(df);

query = '''
SELECT
    G.codigo as Codigo, G.nome as Nome, G.Tipo as Tipo
FROM
    Instalacao_de_Gasoduto as G
'''

df = pd.read_sql_query(query, conn)
option = st.selectbox(
    'Selecione o Nome',
     df['Nome'])

query = ('''
SELECT
    G.codigo as Codigo, G.nome as Nome, G.Tipo as Tipo
FROM
    Instalacao_de_Gasoduto as G
WHERE
    G.nome = "replace"
''').replace('replace', option)
df = pd.read_sql_query(query, conn)
st.write(df);

# ### 6.1.2 Consulta 2
# **Contratos que geraram eventos no dia 30 de Julho**
# 
# Essa pesquisa encontra os contratos por tŕas dos eventos do dia 30. Útil para descobrir os responsáveis das movimentações do dia.

# In[6]:


query = '''
SELECT DISTINCT
    C.nome
FROM
    Contrato as C
WHERE
    C.data = "30/07/2021" AND C.nome IS NOT NULL
ORDER BY
    C.nome;
'''

pr = pd.read_sql_query(query, conn)
pr


# ## 6.2 Três consultas envolvendo junção de duas relações
# 
# ### 6.2.1 Consulta 3
# 
# **Instalações de Transporte em São Paulo**
# - Para essa consulta, temos que unir **Instalacao_de_Transporte** com **Instalacao_de_Gasoduto** (Relação "*Pertence*") e também com **Municipio** (Relação "*Localização*").
# 
# Essa pesquisa encontra as Instalações de Transporte que operam em São Paulo. Essa pesquisa é interessante para o governo, que busca compreender as atuações dessas empresas de movimentação dentro de seu território

# In[7]:


query = '''
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
'''

pr = pd.read_sql_query(query, conn)
pr


# ### 6.2.2 Consulta 4
# 
# **Contratos da Pilar**
# - Para essa consulta, temos que unir **Instalacao_de_Transporte** com **Instalacao_de_Gasoduto** (Relação "*Pertence*") e também com **Contrato** (Relação "*Contrato*").
# 
# Essa pesquisa encontra todos os contratos nos quais a Pilar (Intalação de Tranporte) estava envolvido. Útil para traçar as movimentações e eventos relacionados com a Pilar

# In[8]:


query = '''
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
'''

pr = pd.read_sql_query(query, conn)
pr


# ### 6.2.3 Consulta 5
# 
# **Municípios onde a Petrobrás não operou**
# - Para essa consulta, temos que unir **Carregador** com **Instalacao_de_Gasoduto** (Relação "*Contrato*") e também com **Municipio** (Relação "*Localização*").
# 
# Essa pesquisa encontra todos os municípios onde a Petrobrás não fez carregamento. Essa pesquisa serve, por exemplo, para empresas competidoras da Petrobrás que gostariam de se estabelecer em cidades onde a Petrobrás não opera.

# In[10]:


query = '''
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
'''

pr = pd.read_sql_query(query, conn)
pr


# ## 6.3 Três consultas envolvendo junção de três ou mais relações
# 
# Para os seguintes casos, tivemos que utilizar todas as três relações disponíveis (**Pertence**, **Localização** e **Contrato**).
# 
# ### 6.3.1 Consulta 6
# 
# **Instalações de Transporte que participaram de Solicitações de Volume no Rio de Janeiro no dia 15 de Julho.**
# 
# Essa pesquisa serve para encontrar as Instalações de Transporte cujas Instalações de Gasoduto fizeram solicitações de recurso. Útil para verificação quanto foi pedido para verificação posterior de validação dos contratos

# In[11]:


query = '''
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
'''

pr = pd.read_sql_query(query, conn)
pr


# ### 6.3.2 Consulta 7
# 
# **Instalação de Transporte que operam na Região Sul com maior quantidade de Contratos no dia 7 de Julho.**
# 
# Essa pesquisa encontra as Instalações de Transporte operando na Região Sul cujos contratos levaram a eventos o dia 7 de Julho, junto da quantidade desses contratos por Transporte. Útil para descobrir as Instalações de Transporte que tiveram movimentação nesse dia.

# In[12]:


query = '''
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
'''

pr = pd.read_sql_query(query, conn)
pr


# ### 6.3.3 Consulta 8
# 
# **Carregadores que já trabalharam para GASBEL e GASBEL II fora de Minas Gerais.**
# 
# Essa pesquisa encontra os Carregadores que já fecharam contrato com a GASBEL E GASBEL II em um trabalho fora de Minas Gerais. Como GASBEL e GASBEL II atuam primariamente em Minas Gerias, julga-se interessante para a empresa olhar para fora e analisar novas oportunidades sem repetir lugares já passados.

# In[13]:


query = '''
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
'''

pr = pd.read_sql_query(query, conn)
pr


# ## 6.4 Duas consultas envolvendo agregação sobre junção de duas ou mais relações
# 
# ### 6.4.1 Consulta 9
# 
# **Municípios com maior valor de Volume Realizado**
# - Para essa consulta, temos que unir **Contrato** com **Instalacao_de_Gasoduto** (Relação "*Contrato*") e também com **Municipio** (Relação "*Localização*").
# 
# Essa pesquisa encontra os Municipios com maior volume de recursos utilizados. Ela é interessante para analisar municípios produtíveis quanto às suas operações.

# In[14]:


query = '''
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
'''

pr = pd.read_sql_query(query, conn)
pr


# ### 6.4.2 Consulta 10
# 
# **Quantidade de Município em que cada Instalação de Transporte opera**
# - Para essa consulta, temos que unir **Instalacao_de_Transporte** com **Instalacao_de_Gasoduto** (Relação "*Pertence*") e também com **Municipio** (Relação "*Localização*").
# 
# Essa pesquisa encontra a quantidade de municípios ligados as Instalações de Tansporte. Útil para compará-las quanto ao seu alcance e influência nas regiões.  

# In[15]:


query = '''
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
'''

pr = pd.read_sql_query(query, conn)
pr


# # 7. Autoavaliação dos membros
