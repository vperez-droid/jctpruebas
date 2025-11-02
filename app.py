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

        # Pestaña 1: Panel de Control (MODIFICADO)
        with tab1:
            st.header("Resumen de tu Actividad")
            
            # Usamos columnas para centrar el contenido
            center_col1, center_col2, center_col3 = st.columns([1, 2, 1])
            with center_col2:
                dias_entrenados_ultimo_mes = 15 # Dato ficticio
                
                st.metric(label="Entrenamientos en los últimos 30 días", value=f"{dias_entrenados_ultimo_mes} días")

                mensaje = ""
                if dias_entrenados_ultimo_mes > 20:
                    mensaje = "### ✅ ¡Imparable! Tu constancia es de otro nivel. ¡Sigue así!"
                elif dias_entrenados_ultimo_mes > 12:
                    mensaje = "### 💪 ¡Gran trabajo! Estás construyendo un hábito sólido. ¡A por más!"
                elif dias_entrenados_ultimo_mes > 5:
                    mensaje = "### 👍 ¡Buen ritmo! Cada sesión suma. ¡No pierdas el impulso!"
                else:
                    mensaje = "### 🚀 ¡Listos para empezar! El camino comienza ahora. ¡Vamos a por ello!"
                
                st.markdown(f"<div style='text-align: center;'>{mensaje}</div>", unsafe_allow_html=True)

        # Pestaña 2: Mi Historial (MODIFICADO Y ARREGLADO)
        with tab2:
            st.header("Calendario de Entrenamientos")
            conn = get_db_connection()
            registros = conn.execute("SELECT fecha, estado FROM historial WHERE username = ?", (st.session_state.username,)).fetchall()
            conn.close()
            
            historial_eventos = []
            for registro in registros:
                if registro['estado'] == 'Entrenado':
                    # Ahora solo ponemos el emoji en el título
                    evento = {"title": "✅", "start": registro['fecha'], "color": "#28a745"}
                else: 
                    evento = {"title": "❌", "start": registro['fecha'], "color": "#dc3545"}
                historial_eventos.append(evento)
            
            # Se había borrado esta línea, la volvemos a añadir para que el calendario se muestre
            calendar(events=historial_eventos, options={"headerToolbar": {"left": "today prev,next", "center": "title"}})

        # Pestaña 3: Entrenamiento de Hoy (Sin cambios)
        with tab3:
            st.header("Tu Rutina para Hoy")
            hoy_str = datetime.date.today().strftime("%Y-%m-%d")
            conn = get_db_connection()
            rutina_hoy = conn.execute("SELECT contenido FROM rutinas WHERE username = ? AND fecha = ?", (st.session_state.username, hoy_str)).fetchone()
            if rutina_hoy:
                st.markdown(rutina_hoy['contenido'])
                st.write("---")
                if st.button("✅ He completado el entrenamiento"):
                    conn.execute("INSERT OR REPLACE INTO historial (username, fecha, estado) VALUES (?, ?, 'Entrenado')", (st.session_state.username, hoy_str))
                    conn.commit()
                    st.success("¡Genial! Entrenamiento registrado.")
            else:
                st.info("No tienes ninguna rutina asignada para hoy.")
            conn.close()

        # Pestaña 4: Mis Rutinas (Sin cambios)
        with tab4:
            st.header("Biblioteca de Rutinas")
            conn = get_db_connection()
            todas_mis_rutinas = conn.execute("SELECT fecha, contenido FROM rutinas WHERE username = ? ORDER BY fecha DESC", (st.session_state.username,)).fetchall()
            conn.close()
            if todas_mis_rutinas:
                for rutina in todas_mis_rutinas:
                    with st.expander(f"Rutina del {rutina['fecha']}"):
                        st.markdown(rutina['contenido'])
            else:
                st.info("Aún no tienes ninguna rutina asignada.")

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
