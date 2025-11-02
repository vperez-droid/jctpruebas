import streamlit as st

# Título de la página y configuración
st.set_page_config(page_title="Javier Cancelas Training", layout="wide")

# --- CONTENIDO DE LA PÁGINA ---
# El estilo y los colores ahora se gestionan desde el archivo .streamlit/config.toml
# por lo que ya no necesitamos el bloque de CSS aquí.

st.title("JAVIER CANCELAS TRAINING - JCT")
st.header("Inicio de sesión")

# --- FORMULARIO DE INICIO DE SESIÓN ---
# 'with st.form' crea un formulario que agrupa elementos.
with st.form("login_form"):
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    # Botón para enviar el formulario
    submitted = st.form_submit_button("Iniciar sesión")

    # Cuando el botón es presionado, 'submitted' se vuelve True
    if submitted:
        # Aquí es donde añadirás la lógica para verificar el usuario y la contraseña.
        st.success("¡Has iniciado sesión correctamente!")
