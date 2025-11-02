import streamlit as st
from PIL import Image

# Título de la página y configuración
st.set_page_config(page_title="Javier Cancelas Training", layout="wide")

# --- CENTRADO DEL CONTENIDO ---
# Creamos 3 columnas para centrar el contenido principal
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # --- IMAGEN ---
    # Intentamos cargar y mostrar la imagen.
    # El bloque try/except evita que la app se rompa si no encuentra la imagen.
    try:
        image = Image.open('jct.jpeg')
        st.image(image, use_column_width=True)
    except FileNotFoundError:
        st.error("No se encontró la imagen 'jct.jpeg'. Asegúrate de que está en el repositorio.")

    # --- CONTENIDO DE LA PÁGINA ---
    st.title("JAVIER CANCELAS TRAINING - JCT")
    st.header("Inicio de sesión")

    # --- FORMULARIO DE INICIO DE SESIÓN ---
    with st.form("login_form"):
        username = st.text_input("Usuario", key="username")
        password = st.text_input("Contraseña", type="password", key="password")

        # Botón para enviar el formulario
        submitted = st.form_submit_button("Iniciar sesión")

        if submitted:
            st.success("¡Has iniciado sesión correctamente!")
