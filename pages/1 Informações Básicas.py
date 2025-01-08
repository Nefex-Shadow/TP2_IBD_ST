import streamlit as st

st.set_page_config(page_title="Informações Básicas", layout="wide")

st.title("Informações Básicas")
st.sidebar.markdown('Informações Básicas')

st.subheader("1. Membros")
st.markdown("""
- **Luís Eduardo Limas Brito**: 2023102329
- **Felipe Araujo Melo**: 2023027947
- **Natanael dos Santos Júnior**: 2023087842
""")

st.subheader("2. Descrição dos dados")
st.markdown("""
- **URL**: [Dados Consolidados de Movimentação de Gás Natural](https://dados.gov.br/dados/conjuntos-dados/dados-consolidados-de-movimentacao-de-gas-natural-em-gasodutos-de-transporte)
- **Período utilizado**: Julho de 2021
""")

st.markdown("""
Os dados escolhidos armazenam as informações de movimentações de recursos entre diversas entidades. 
Analisando superficialmente os dados e seus identificadores, identificamos a existência das seguintes entidades:
- Instalação de Transporte
- Instalação de Gasoduto
- Município
- Operador de Instalação
- Carregador de Instalação

As movimentações entre as entidades citadas ocorrem por meio de um contrato, o qual retrata os eventos dessa movimentação separado por tipos de análises e separado por dia.
""")

st.markdown("""
Os dados foram processados por linha. Pegamos os valores das colunas de interesse e adicionamos às tabelas correspondentes. 
Quanto aos dados, com exceção dos códigos de identificação e o valor do contrato, todos foram considerados do tipo **TEXTO**, enquanto o valor do contrato é do tipo **FLOAT** e os códigos são do tipo **INTEIRO**. 
Houve um problema na hora de implementação quanto ao código de identificação da entidade Carregador, pois um dos códigos era grande demais, e seu valor era traduzido para "2,75E+13", o qual não era possível traduzir para **INTEIRO**. Por isso, decidimos que o código do Carregador será do tipo **TEXTO**.
""")

st.markdown("""
A leitura dos dados ocorrerá em uma das células mais abaixo, porém antes precisamos criar as tabelas. Assim teremos que explicar a criação do Modelo Relacional e Modelo ER antes.
""")

st.subheader("3. Modelo Relacional")
st.markdown("""
Para montar as tabelas, precisamos normalizar os dados. Isso quer dizer quebrar a linha dos dados em tabelas condizentes com as colunas apresentadas.

Os dados estão no formato:

- **Transportadora** (<u>Código da Instalação de Transporte</u>, Nome da Instalação de Transporte, <u>Código da Instalação de Gasoduto</u>, Nome da Instalação de Gasoduto, Tipo de Instalação de Gasoduto, <u>Nome do Município da Instalação de Gasoduto</u>, <u>Nome da UF da Instalação de Gasoduto</u>, <u>Código do Operador da Instalação de Gasoduto</u>, Nome do Operador da Instalação de Gasoduto, <u>Código do Carregador que usa a Instalação de Gasoduto</u>, Nome do Carregador que usa a Instalação de Gasoduto, <u>Nome do Contrato da Instalação de Gasoduto</u>, <u>Nome da Variável</u>, (<u>Data</u>, Valor));
""", unsafe_allow_html=True)

st.markdown("""
### Primeira Forma Normal (1FN)

- **Transportadora** (<u>Código da Instalação de Transporte</u>, Nome da Instalação de Transporte, <u>Código da Instalação de Gasoduto</u>, Nome da Instalação de Gasoduto, Tipo de Instalação de Gasoduto, <u>Nome do Município da Instalação de Gasoduto</u>, <u>Nome da UF da Instalação de Gasoduto</u>, <u>Código do Operador da Instalação de Gasoduto</u>, Nome do Operador da Instalação de Gasoduto, <u>Código do Carregador que usa a Instalação de Gasoduto</u>, Nome do Carregador que usa a Instalação de Gasoduto, <u>Nome do Contrato da Instalação de Gasoduto</u>, <u>Nome da Variável</u>);
- **Transportadora_Contrato** (<u>Código da Instalação de Transporte</u>, <u>Código da Instalação de Gasoduto</u>, <u>Nome do Município da Instalação de Gasoduto</u>, <u>Código do Operador da Instalação de Gasoduto</u>, <u>Código do Carregador que usa a Instalação de Gasoduto</u>, <u>Nome do Contrato da Instalação de Gasoduto</u>, <u>Nome da Variável</u>, <u>Data</u>, Valor);
""", unsafe_allow_html=True)

st.markdown("""
### Segunda Forma Normal (2FN)

Dependências identificadas:
- **Código da Instalação de Transporte** → Nome da Instalação de Transporte, Código da Instalação de Gasoduto;
- **Código da Instalação de Gasoduto** → Nome da Instalação de Gasoduto, Tipo de Instalação de Gasoduto;
- **Nome do Município da Instalação de Gasoduto, Nome da UF da Instalação de Gasoduto** → Código da Instalação de Gasoduto;
- **Código do Operador da Instalação de Gasoduto** → Nome do Operador da Instalação de Gasoduto;
- **Código do Carregador que usa a Instalação de Gasoduto** → Nome do Carregador que usa a Instalação de Gasoduto;
- **Código da Instalação de Gasoduto, Código do Operador da Instalação de Gasoduto, Código do Carregador que usa a Instalação de Gasoduto** → Nome do Contrato da Instalação de Gasoduto;
- **Nome do Contrato da Instalação de Gasoduto, Nome da Variável, Código da Instalação de Gasoduto, Data** → Valor.
""", unsafe_allow_html=True)

st.markdown("""
### Terceira Forma Normal (3FN)

- **Instalação de Transporte** (<u>Código</u>, Nome);
- **Instalação de Gasoduto** (<u>Código</u>, Nome, Tipo);
- **Transporte_Gasoduto** (<u>Código do Gasoduto</u>, Código do Transporte);
- **Município** (<u>Nome</u>, UF);
- **Município_Gasoduto** (<u>Código do Gasoduto</u>, Nome do Município, UF do Município);
- **Operador** (<u>Código</u>, Nome);
- **Carregador** (<u>Código</u>, Nome);
- **Instalação_Contrato** (<u>Código do Gasoduto</u>, <u>Código do Operador</u>, <u>Código do Carregador</u>, Nome do Contrato);
- **Contrato** (<u>Nome</u>, Variável, Código do Gasoduto, Data, Valor).
""", unsafe_allow_html=True)

image_path = "./Diagrama_ER.png"

st.write(' ')
st.write(' ')
st.write(' ')

st.image(image_path, caption="Diagrama ER", width=800)