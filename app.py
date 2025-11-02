import streamlit as st
from PIL import Image
import sqlite3
from passlib.context import CryptContext
import datetime
from streamlit_calendar import calendar

# --- CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title="Javier Cancelas Training", layout="wide")

# --- LÓGICA DE BASE DE DATOS Y AUTENTICACIÓN (Sin cambios) ---
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user_data = c.fetchone()
    conn.close()
    return user_data

# --- LÓGICA DE LOGIN Y ESTADO DE SESIÓN (Sin cambios) ---
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

# SI EL USUARIO HA INICIADO SESIÓN, MUESTRA LA APP PRINCIPAL CON NAVEGACIÓN
if st.session_state.logged_in:
    
    # --- BARRA LATERAL DE NAVEGACIÓN ---
    with st.sidebar:
        st.title(f"Hola, {st.session_state.username}")
        st.write("---")
        
        # Opciones del menú
        opcion = st.radio(
            "Navegación",
            ("Panel de Control", "Mi Historial", "Entrenamiento de Hoy", "Mis Rutinas")
        )
        
        st.write("---")
        if st.button("Cerrar sesión"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()

    # --- CONTENIDO PRINCIPAL (CAMBIA SEGÚN LA SELECCIÓN) ---

    # -- APARTADO 1: PANEL DE CONTROL (PÁGINA DE INICIO) --
    if opcion == "Panel de Control":
        st.title("Panel de Control")
        st.header(f"¡Bienvenido de nuevo!")
        hoy = datetime.date.today()
        st.write(f"Hoy es: **{hoy.strftime('%d de %B de %Y')}**.")
        st.write("Selecciona una opción de la barra lateral para empezar.")

    # -- APARTADO 2: MI HISTORIAL --
    elif opcion == "Mi Historial":
        st.title("Mi Historial de Entrenamiento")
        st.write("Aquí puedes ver un resumen de tus días de entrenamiento.")

        # DATOS FICTICIOS: En el futuro, esto vendrá de la base de datos.
        # Creamos eventos para el calendario con un tick verde o una cruz roja.
        historial_eventos = [
            {"title": "✅ Entrenado", "start": "2025-11-03", "color": "#28a745"},
            {"title": "✅ Entrenado", "start": "2025-11-05", "color": "#28a745"},
            {"title": "❌ Faltó", "start": "2025-11-07", "color": "#dc3545"},
            {"title": "✅ Entrenado", "start": "2025-11-10", "color": "#28a745"},
        ]
        
        calendar_options = {"headerToolbar": {"left": "today prev,next", "center": "title"}}
        calendar(events=historial_eventos, options=calendar_options)

    # -- APARTADO 3: ENTRENAMIENTO DE HOY --
    elif opcion == "Entrenamiento de Hoy":
        st.title("Entrenamiento de Hoy")
        st.header("Rutina de Pecho y Tríceps")
        
        # DATOS FICTICIOS:
        st.markdown("""
        - **Press de Banca:** 4 series x 8-10 repeticiones
        - **Fondos en paralelas:** 3 series x al fallo
        - **Aperturas con mancuernas:** 3 series x 12 repeticiones
        - **Press francés:** 4 series x 10 repeticiones
        - **Extensiones de tríceps en polea:** 3 series x 15 repeticiones
        """)
        
        st.info("Recuerda calentar bien antes de empezar y estirar al terminar.")

    # -- APARTADO 4: MIS RUTINAS --
    elif opcion == "Mis Rutinas":
        st.title("Mis Rutinas")
        st.write("Aquí tienes todas las rutinas que te ha asignado tu entrenador.")
        
        # Usamos st.expander para mostrar las rutinas de forma ordenada
        with st.expander("Rutina A: Tren Superior"):
            st.write("Press de Banca, Remo con Barra, Press Militar, Dominadas...")
            
        with st.expander("Rutina B: Tren Inferior"):
            st.write("Sentadillas, Peso Muerto, Zancadas, Elevación de talones...")
            
        with st.expander("Rutina C: Full Body"):
            st.write("Sentadillas, Press de Banca, Dominadas, Plancha...")


# SI EL USUARIO NO HA INICIADO SESIÓN, MUESTRA EL LOGIN
else:
    # --- PÁGINA DE LOGIN (Sin cambios) ---
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
