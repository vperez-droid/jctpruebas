import streamlit as st
from PIL import Image
import sqlite3
from passlib.context import CryptContext
import datetime
from streamlit_calendar import calendar
import pandas as pd
import altair as alt # Importamos la nueva librería

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

if 'logged_in' not in st.session_state: st.session_state.logged_in = False; st.session_state.username = ""

def login_user():
    username = st.session_state.login_username
    password = st.session_state.login_password
    user_data = get_user(username)
    if user_data and verify_password(password, user_data[1]):
        st.session_state.logged_in = True; st.session_state.username = username; st.rerun()
    else: st.error("Usuario o contraseña incorrectos.")

# --- INTERFAZ DE USUARIO ---

if st.session_state.logged_in:
    
    ADMIN_USERNAME = "admin" 
    
    if st.session_state.username == ADMIN_USERNAME:
        # --- VISTA DE ADMINISTRADOR (Sin cambios) ---
        st.title("Panel de Administrador")
        conn = get_db_connection(); clientes = conn.execute("SELECT username FROM users WHERE username != ?", (ADMIN_USERNAME,)).fetchall()
        if clientes:
            cliente_seleccionado = st.selectbox("Seleccionar Cliente", [c['username'] for c in clientes])
            fecha_rutina = st.date_input("Fecha de la Rutina")
            contenido_rutina = st.text_area("Contenido de la Rutina")
            if st.button("Guardar Rutina"):
                conn.execute("INSERT OR REPLACE INTO rutinas (username, fecha, contenido) VALUES (?, ?, ?)", (cliente_seleccionado, fecha_rutina.strftime("%Y-%m-%d"), contenido_rutina))
                conn.commit(); st.success(f"Rutina guardada para {cliente_seleccionado}.")
        else: st.warning("No hay clientes para asignar rutinas.")
        conn.close(); st.write("---")
        if st.button("Cerrar Sesión de Admin"): st.session_state.logged_in = False; st.session_state.username = ""; st.rerun()

    else:
        # --- VISTA DE CLIENTE NORMAL ---
        col1, col2 = st.columns([4, 1])
        with col1: st.title(f"Bienvenido, {st.session_state.username}!")
        with col2:
            if st.button("Cerrar sesión"): st.session_state.logged_in = False; st.session_state.username = ""; st.rerun()
        st.write("---")

        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Panel de Control", "Entrenamiento de Hoy", "Mi Historial", "Mis Rutinas", "Mi Progreso"])

        with tab1: # Panel de Control
            _, center_col, _ = st.columns([1, 2, 1])
            with center_col:
                st.header("Resumen de tu Actividad")
                dias_entrenados_ultimo_mes = 15
                st.metric(label="Entrenamientos en los últimos 30 días", value=f"{dias_entrenados_ultimo_mes} días")
                mensaje = "### 💪 ¡Gran trabajo! Estás construyendo un hábito sólido."
                st.markdown(f"<div style='text-align: center;'>{mensaje}</div>", unsafe_allow_html=True)

        with tab2: # Entrenamiento de Hoy
            st.header("Tu Rutina para Hoy")
            st.info("Nota: Esta es una rutina de ejemplo.")
            st.markdown("### Rutina de Tren Superior\n- **Press de Banca:** 4x10\n- **Dominadas:** 4x Fallo\n- **Remo con Barra:** 3x12")
            st.write("---")
            if st.button("✅ He completado el entrenamiento"): st.success("¡Genial!"); st.balloons()
        
        with tab3: # Mi Historial
            st.header("Calendario de Entrenamientos")
            historial_eventos_demo = [{"title": "✅", "start": f"2025-11-{d:02d}", "color": "#28a745"} for d in [3, 5, 7, 10, 12]]
            calendar_options = {"headerToolbar": {"left": "today", "center": "title", "right": "prev,next"}, "initialView": "dayGridMonth", "height": "auto"}
            calendar(events=historial_eventos_demo, options=calendar_options)

        with tab4: # Mis Rutinas
            st.header("Biblioteca de Rutinas")
            with st.expander("🏋️‍♂️ Rutina A: Fuerza"): st.markdown("- **Sentadillas:** 5x5")
            with st.expander("🏃‍♂️ Rutina B: Hipertrofia"): st.markdown("- **Press Inclinado:** 4x10")
            
        # --- PESTAÑA 5: MI PROGRESO (TOTALMENTE REDISEÑADA) ---
        with tab5:
            st.header("Tu Evolución")
            st.write("---")
            
            # --- Creación de datos ficticios MÁS REALISTAS ---
            data = {
                'Mes': pd.to_datetime(['2025-06-01', '2025-07-01', '2025-08-01', '2025-09-01', '2025-10-01', '2025-11-01']),
                'Peso (kg)': [115.0, 112.0, 107.0, 108.0, 102.0, 100.5] # Inicio -> -3kg -> -5kg -> +1kg -> -6kg -> -1.5kg
            }
            df_progreso = pd.DataFrame(data)
            
            # --- Gráfica de Evolución de Peso con ALTAIR ---
            st.subheader("Evolución del Peso Corporal (Mes a Mes)")

            chart = alt.Chart(df_progreso).mark_line(
                point=alt.OverlayMarkDef(color="yellow", size=100, filled=True) # Puntos amarillos
            ).encode(
                x=alt.X('Mes:T', title='Fecha'),
                y=alt.Y('Peso (kg):Q', title='Peso Corporal (kg)', scale=alt.Scale(domain=[80, 120])), # EJE Y CONTROLADO
                tooltip=['Mes', 'Peso (kg)']
            ).properties(
                height=400
            ).configure_axis(
                labelColor='yellow',
                titleColor='yellow'
            ).configure_title(
                color='yellow'
            ).configure_view(
                stroke=None
            )
            
            st.altair_chart(chart, use_container_width=True)

            st.write("---")

            # --- Métrica de Consistencia ---
            st.header("Consistencia de Entrenamiento")
            
            entrenamientos_mes_actual = 15; meta_mensual = 20
            
            _, center_metric_col, _ = st.columns([1, 1, 1])
            with center_metric_col:
                st.metric(label="Entrenamientos este mes", value=f"{entrenamientos_mes_actual} / {meta_mensual}")
            
            porcentaje_meta = int((entrenamientos_mes_actual / meta_mensual) * 100)
            st.progress(porcentaje_meta, text=f"Llevas el {porcentaje_meta}% de tu objetivo mensual")

# --- PÁGINA DE LOGIN (Sin cambios) ---
else:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("JAVIER CANCELAS TRAINING - JCT")
        img_col1, img_col2, img_col3 = st.columns([1, 1, 1])
        with img_col2:
            try: image = Image.open('jct.jpeg'); st.image(image, width=200)
            except FileNotFoundError: st.error("No se encontró el logo.")
        st.header("Inicio de sesión")
        with st.form("login_form"):
            st.text_input("Usuario", key="login_username")
            st.text_input("Contraseña", type="password", key="login_password")
            if st.form_submit_button("Iniciar sesión"): login_user()
