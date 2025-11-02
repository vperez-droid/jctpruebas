import streamlit as st

# Título de la página y configuración
st.set_page_config(page_title="Javier Cancelas Training", layout="wide")

# --- ESTILOS CSS ---
# Se inyecta CSS para cambiar los colores.
# El fondo del cuerpo ahora es amarillo (#FFFF00) y el color del texto principal es negro.
# El botón se configura con fondo negro y texto amarillo para que contraste.
page_bg_img = """
<style>
/* Estilo para el cuerpo de la página */
body {
    background-color: #FFFF00; /* Fondo amarillo */
    color: #000000; /* Texto principal negro para legibilidad */
}

/* Cambiar color del título principal para que sea negro */
h1 {
    color: #000000;
}

/* Estilo para los campos de texto */
.stTextInput > div > div > input {
    background-color: #FFFFFF; /* Fondo blanco para el campo */
    color: #000000; /* Texto negro dentro del campo */
}

/* Estilo para el botón */
.stButton > button {
    color: #FFFF00; /* Texto del botón amarillo */
    background-color: #000000; /* Fondo del botón negro */
    border: none; /* Sin borde */
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# --- CONTENIDO DE LA PÁGINA ---
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
