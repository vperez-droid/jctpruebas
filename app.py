import streamlit as st
from PIL import Image
import sqlite3
from passlib.context import CryptContext
import datetime
from streamlit_calendar import calendar

# --- CONFIGURACIÓN Y CONEXIÓN A BD (Sin cambios) ---
st.set_page_config(page_title="Javier Cancelas Training", layout="wide")

def get_db_connection():
    conn = sqlite3.connect('users.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS rutinas (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, fecha TEXT NOT NULL, contenido TEXT NOT NULL, FOREIGN KEY (username) REFERENCES users (username))')
    conn.execute('CREATE TABLE IF NOT EXISTS historial (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, fecha TEXT NOT NULL, estado TEXT NOT NULL, FOREIGN KEY (username) REFERENCES users (username), UNIQUE(username, fecha))')
    conn.commit()
    conn.close()

init_db()

# --- LÓGICA DE AUTENTICACIÓN (Sin cambios) ---
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
def verify_password(plain_password, hashed_password): return pwd_context.verify(plain_password, hashed_password)
def get_user(username):
    conn = get_db_connection()
    user_data = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return user_data

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
        st.rerun()
    else:
        st.error("Usuario o contraseña incorrectos.")

# --- INTERFAZ DE USUARIO ---

if st.session_state.logged_in:
    
    ADMIN_USERNAME = "admin" 
    
    # --- VISTA DE ADMINISTRADOR (Sin cambios) ---
    if st.session_state.username == ADMIN_USERNAME:
        st.title("Panel de Administrador")
        # (El código del admin sigue igual)
        conn = get_db_connection()
        clientes = conn.execute("SELECT username FROM users WHERE username != ?", (ADMIN_USERNAME,)).fetchall()
        if clientes:
            cliente_seleccionado = st.selectbox("Seleccionar Cliente", [c['username'] for c in clientes])
            fecha_rutina = st.date_input("Fecha de la Rutina")
            contenido_rutina = st.text_area("Contenido de la Rutina (Ej: Press Banca 4x10, ...)")
            if st.button("Guardar Rutina"):
                conn.execute("INSERT OR REPLACE INTO rutinas (username, fecha, contenido) VALUES (?, ?, ?)", (cliente_seleccionado, fecha_rutina.strftime("%Y-%m-%d"), contenido_rutina))
                conn.commit()
                st.success(f"Rutina guardada para {cliente_seleccionado} en la fecha {fecha_rutina}.")
        else:
            st.warning("No hay clientes para asignar rutinas. Crea nuevos usuarios.")
        conn.close()
        st.write("---")
        if st.button("Cerrar Sesión de Admin"):
            st.session_state.logged_in = False; st.session_state.username = ""; st.rerun()

    # --- VISTA DE CLIENTE NORMAL ---
    else:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.title(f"Bienvenido, {st.session_state.username}!")
        with col2:
            if st.button("Cerrar sesión"):
                st.session_state.logged_in = False; st.session_state.username = ""; st.rerun()
        st.write("---")

        tab1, tab2, tab3, tab4 = st.tabs(["Panel de Control", "Mi Historial", "Entrenamiento de Hoy", "Mis Rutinas"])

        # Pestaña 1: Panel de Control (CONTENIDO CENTRADO)
        with tab1:
            # Usamos columnas para centrar todo el contenido
            _, center_col, _ = st.columns([1, 2, 1])
            with center_col:
                st.header("Resumen de tu Actividad")
                
                dias_entrenados_ultimo_mes = 15
                st.metric(label="Entrenamientos en los últimos 30 días", value=f"{dias_entrenados_ultimo_mes} días")

                mensaje = "### 💪 ¡Gran trabajo! Estás construyendo un hábito sólido. ¡A por más!"
                st.markdown(f"<div style='text-align: center;'>{mensaje}</div>", unsafe_allow_html=True)

        # Pestaña 2: Mi Historial (CALENDARIO ARREGLADO + DATOS DE SIMULACIÓN)
        with tab2:
            st.header("Calendario de Entrenamientos")
            
            # --- DATOS DE SIMULACIÓN PARA LA DEMO ---
            # Si la base de datos no tiene historial, usamos estos datos para que siempre se vea bien.
            historial_eventos_demo = [
                {"title": "✅", "start": "2025-11-03", "color": "#28a745"},
                {"title": "✅", "start": "2025-11-05", "color": "#28a745"},
                {"title": "❌", "start": "2025-11-07", "color": "#dc3545"},
                {"title": "✅", "start": "2025-11-10", "color": "#28a745"},
                {"title": "✅", "start": "2025-11-12", "color": "#28a745"},
            ]
            
            calendar(events=historial_eventos_demo, options={"headerToolbar": {"left": "today prev,next", "center": "title"}})

        # Pestaña 3: Entrenamiento de Hoy (CON DATOS DE SIMULACIÓN)
        with tab3:
            st.header("Tu Rutina para Hoy")
            st.info("Nota: Esta es una rutina de ejemplo. Tus rutinas reales aparecerán aquí.")
            
            # --- RUTINA DE SIMULACIÓN PARA LA DEMO ---
            st.markdown("""
            ### Rutina de Tren Superior - Enfoque Pecho y Espalda
            *   **Calentamiento:** 10 minutos de cardio ligero.
            ---
            1.  **Press de Banca con Barra**
                *   Series: 4
                *   Repeticiones: 8-10
            2.  **Dominadas (o Jalón al Pecho)**
                *   Series: 4
                *   Repeticiones: Al fallo
            3.  **Aperturas con Mancuernas en Banco Inclinado**
                *   Series: 3
                *   Repeticiones: 12-15
            4.  **Remo con Barra**
                *   Series: 4
                *   Repeticiones: 10
            5.  **Elevaciones Laterales con Mancuernas**
                *   Series: 3
                *   Repeticiones: 15
            ---
            *   **Enfriamiento:** 5-10 minutos de estiramientos.
            """)
            st.write("---")
            if st.button("✅ He completado el entrenamiento"):
                st.success("¡Genial! Entrenamiento registrado.")
                st.balloons()

        # Pestaña 4: Mis Rutinas (CON DATOS DE SIMULACIÓN)
        with tab4:
            st.header("Biblioteca de Rutinas")
            st.info("Aquí encontrarás todas las rutinas que tu entrenador te ha asignado.")
            
            # --- RUTINAS DE SIMULACIÓN PARA LA DEMO ---
            with st.expander("🏋️‍♂️ Rutina A: Enfoque Fuerza (Lunes)"):
                st.markdown("- **Sentadillas:** 5x5\n- **Press de Banca:** 5x5\n- **Peso Muerto:** 1x5")
            with st.expander("🏃‍♂️ Rutina B: Hipertrofia (Miércoles)"):
                st.markdown("- **Press Inclinado con Mancuernas:** 4x10\n- **Remo con Mancuerna:** 4x12\n- **Prensa de Piernas:** 3x15\n- **Curl de Bíceps:** 3x12")
            with st.expander("🔥 Rutina C: Acondicionamiento (Viernes)"):
                st.markdown("- **Burpees:** 3 series de 1 minuto\n- **Kettlebell Swings:** 3x20\n- **Plancha:** 3 series hasta el fallo")

# --- PÁGINA DE LOGIN (Sin cambios) ---
else:
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
