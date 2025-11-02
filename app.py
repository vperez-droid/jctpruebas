import streamlit as st
from PIL import Image
import sqlite3
from passlib.context import CryptContext
import datetime
from streamlit_calendar import calendar

# --- CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title="Javier Cancelas Training", layout="wide")

# --- CONTEXTO DE HASHING (CON ARGON2) Y FUNCIONES DE BASE DE DATOS ---
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Función para verificar la contraseña
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Función para obtener la información de un usuario desde la BD
def get_user(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user_data = c.fetchone()
    conn.close()
    return user_data

# --- LÓGICA DE LOGIN Y ESTADO DE SESIÓN ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

def login_user():
    username = st.session_state.login_username
    password = st.session_state.login_password
    
    user_data = get_user(username)
    if user_data and verify_password(password, user_data[1]):
        st.session_state.logged_in = True
        st.session_state.username = username
    else:
        st.error("Usuario o contraseña incorrectos.")

# --- INTERFAZ DE USUARIO ---
if st.session_state.logged_in:
    # --- PÁGINA PRINCIPAL (CONTENIDO DESPUÉS DEL LOGIN) ---
    st.title(f"Bienvenido, {st.session_state.username}!")

    # Mostrar la fecha de hoy
    hoy = datetime.date.today()
    st.header(f"Hoy es: {hoy.strftime('%d de %B de %Y')}")

    # Opciones de configuración para el calendario
    calendar_options = {
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,timeGridDay",
        },
        "initialView": "dayGridMonth",
    }

    st.write("---") # Línea separadora
    
    # Mostrar el calendario
    st.subheader("Calendario del Mes")
    calendar_component = calendar(events=[], options=calendar_options)


    if st.button("Cerrar sesión"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

# Si el usuario no ha iniciado sesión, muestra la página de login
else:
    # --- PÁGINA DE LOGIN ---
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.title("JAVIER CANCELAS TRAINING - JCT")
        
        img_col1, img_col2, img_col3 = st.columns([1, 1, 1])
        with img_col2:
            try:
                image = Image.open('jct.jpeg')
                st.image(image, width=200)
            except FileNotFoundError:
                st.error("No se encontró el logo.")

        st.header("Inicio de sesión")

        with st.form("login_form"):
            st.text_input("Usuario", key="login_username")
            st.text_input("Contraseña", type="password", key="login_password")

            if st.form_submit_button("Iniciar sesión"):
                login_user()
