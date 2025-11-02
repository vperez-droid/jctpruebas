import streamlit as st

# Título de la página y configuración
st.set_page_config(page_title="Javier Cancelas Training", layout="wide")

# --- ESTILOS CSS ---
# Esto inyecta CSS para cambiar los colores de fondo y de los elementos.
# El fondo del cuerpo es negro (#000000) y el color del texto principal es blanco.
# El botón se configura con fondo amarillo (#FFFF00) y texto negro.
page_bg_img = """
<style>
/* Estilo para el cuerpo de la página */
body {
    background-color: #000000; /* Fondo negro */
    color: #FFFFFF; /* Texto blanco por defecto */
}

/* Estilo para los campos de texto */
.stTextInput > div > div > input {
    background-color: #333333; /* Fondo gris oscuro para el campo */
    color: #FFFFFF; /* Texto blanco dentro del campo */
}

/* Estilo para el botón */
.stButton > button {
    color: #000000; /* Texto del botón negro */
    background-color: #FFFF00; /* Fondo del botón amarillo */
    border: none; /* Sin borde */
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# --- CONTENIDO DE LA PÁGINA ---
st.title("JAVIER CANCELAS TRAINING - JCT")
st.header("Inicio de sesión")

# --- FORMULARIO DE INICIO DE SESIÓN ---
# 'with st.form' crea un formulario que agrupa elementos. Los datos solo se envían
# cuando se presiona el botón 'st.form_submit_button'.
with st.form("login_form"):
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    # Botón para enviar el formulario
    submitted = st.form_submit_button("Iniciar sesión")

    # Cuando el botón es presionado, 'submitted' se vuelve True
    if submitted:
        # Aquí es donde añadirás la lógica para verificar el usuario y la contraseña.
        # Por ahora, solo muestra un mensaje de éxito.
        st.success("¡Has iniciado sesión correctamente!")
        # En un futuro, aquí podrías redirigir a otra página o mostrar contenido nuevo.
