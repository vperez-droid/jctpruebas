import streamlit as st
from PIL import Image

# Título de la página y configuración
st.set_page_config(page_title="Javier Cancelas Training", layout="wide")

# --- CENTRADO DEL CONTENIDO ---
# Creamos 3 columnas para centrar el contenido principal
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # --- TÍTULO PRINCIPAL ---
    st.title("JAVIER CANCELAS TRAINER")

    # --- IMAGEN / LOGO ---
    # La mostramos aquí, después del título
    try:
        image = Image.open('jct.jpeg')
        # Usamos 'width' para controlar el tamaño exacto. 200 es un buen punto de partida.
        st.image(image, width=200)
    except FileNotFoundError:
        st.error("No se encontró la imagen 'jct.jpeg'. Asegúrate de que está en el repositorio.")

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
