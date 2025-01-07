import sqlite3
import pandas as pd
import streamlit as st
import altair as alt

conn = sqlite3.connect('./Movimentacao_Julho_2021.db')
cursor = conn.cursor()

st.title('Contratos')
st.sidebar.markdown('Contratos')
st.write('#### Esse trecho representa os valores que os contratos agregaram para cada município.')

left_column, right_column = st.columns(2)

left_column.write('##### Escolha os municípios de interesse e qual tipo de contrato gorstaria de analisar.')
left_column.write('Note contratos diferentes tiveram seus valores somados, logo os valores apresentados na tabela são os valores totais do dia')

query = '''
    SELECT DISTINCT
        M.nome as nome
    FROM
        Municipio as M
    ORDER BY
        M.nome
'''

df = pd.read_sql_query(query, conn)

municipios = right_column.multiselect(
    "###### Escolha o Município", list(df['nome']), [df['nome'].values[0]]
)
if not municipios:
    st.error("Por favor, selecione um Município.")

query = '''
SELECT DISTINCT
    C.variavel as variavel
FROM
    Contrato as C
ORDER BY
    C.variavel
'''

df = pd.read_sql_query(query, conn)

variaveis = right_column.selectbox(
    "###### Escolha a variável do Contrato", list(df['variavel'])
)

query = '''
    SELECT DISTINCT data
    FROM Contrato
'''
col =  pd.read_sql_query(query, conn)

data = pd.DataFrame(columns=col['data'])

for m in municipios:
    query = ('''
    SELECT DISTINCT
        M.mun_nome as Nome, C.data as Data, SUM(C.valor) as Valor
    FROM
        Contrato as C RIGHT JOIN (SELECT DISTINCT M.nome as mun_nome, G.codigo as gas_codigo
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
    if (df.empty):
        data.loc[m] = 0;
    else:
        data = data._append(df.pivot(index='Nome', columns='Data', values='Valor'))

st.write('')
st.write('### Valores')
st.write(data)
st.write('')

if data.empty:
    st.write("###### Nada a ser desenhado");

else: 
    data = data.T.reset_index()
    if {'index'}.issubset(data.columns):
        data = pd.melt(data, id_vars=["index"]).rename(columns={"variable":"Município", "index": "Dia", "value": "Valor"})
    else:
        data = pd.melt(data, id_vars=["data"]).rename(columns={"variable":"Município", "data": "Dia", "value": "Valor"})
    st.write()
    for i in range(0, 31 * len(municipios)):
        data['Dia'].values[i] = data['Dia'].values[i].replace('07', data['Dia'].values[i][0] + data['Dia'].values[i][1])
        data['Dia'].values[i] = data['Dia'].values[i].replace(data['Dia'].values[i][0] + data['Dia'].values[i][1], '07', 1)

    chart = (
        alt.Chart(data)
        .mark_area(opacity=0.3)
        .encode(
            x="Dia:T",
            y=alt.Y("Valor:Q", stack=None),
            color="Município:N",
        )
    )
    st.write('')
    st.write('### Gráfico')

    st.altair_chart(chart, use_container_width=True)
