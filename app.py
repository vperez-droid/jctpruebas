import streamlit as st
from PIL import Image

# Título de la página y configuración
st.set_page_config(page_title="Javier Cancelas Training", layout="wide")

# --- CENTRADO DEL CONTENIDO ---
# Creamos 3 columnas para centrar el bloque principal
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # --- TÍTULO PRINCIPAL ---
    st.title("JAVIER CANCELAS TRAINING")

    # --- IMAGEN / LOGO ---
    # Creamos sub-columnas DENTRO de la columna principal para centrar la imagen
    img_col1, img_col2, img_col3 = st.columns([1, 1, 1])
    with img_col2:
        try:
            image = Image.open('jct.jpeg')
            st.image(image, width=200)
        except FileNotFoundError:
            st.error("No se encontró la imagen 'jct.jpeg'.")

    # --- SUBTÍTULO ---
    st.header("Inicio de sesión")

    # --- FORMULARIO DE INICIO DE SESIÓN ---
    with st.form("login_form"):
        username = st.text_input("Usuario", key="username")
        password = st.text_input("Contraseña", type="password", key="password")

        # Botón para enviar el formulario
        submitted = st.form_submit_button("Iniciar sesión")

        if submitted:
            st.success("¡Has iniciado sesión correctamente!")
