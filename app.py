import streamlit as st

# Título de la página y configuración
st.set_page_config(page_title="Javier Cancelas Training", layout="wide")

# --- CENTRADO DEL CONTENIDO ---
# Se crean 3 columnas: col1 y col3 actúan como espacios vacíos a los lados.
# El contenido se pone en col2, la columna central.
# El ratio [1, 2, 1] significa que la columna central es el doble de ancha que las laterales.
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # --- CONTENIDO DE LA PÁGINA ---
    st.title("JAVIER CANCELAS TRAINING")
    st.header("Inicio de sesión")

    # --- FORMULARIO DE INICIO DE SESIÓN ---
    with st.form("login_form"):
        username = st.text_input("Usuario", key="username")
        password = st.text_input("Contraseña", type="password", key="password")

        # Botón para enviar el formulario
        submitted = st.form_submit_button("Iniciar sesión")

        if submitted:
            # Aquí es donde añadirás la lógica para verificar el usuario y la contraseña.
            st.success("¡Has iniciado sesión correctamente!")
