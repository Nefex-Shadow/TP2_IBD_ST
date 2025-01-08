import streamlit as st

st.title('Diagrama ER')
st.sidebar.markdown('Diagrama ER')

image_path = "./Diagrama_ER.png"

# Adicionando a imagem no app
st.image(image_path, caption="Diagrama ER", width=800)