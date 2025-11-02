import streamlit as st
from PIL import Image
import sqlite3
from passlib.context import CryptContext
import datetime
from streamlit_calendar import calendar
import pandas as pd
import altair as alt # Importamos la nueva librería

# --- CÓDIGO HTML DEL CUESTIONARIO ---
# He guardado tu HTML en una variable para mantener el código principal limpio
cuestionario_html = """
<html lang="es"><head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>JCT — Cuestionario Inicial</title>
  <meta name="color-scheme" content="light only">
  <style>
    :root{--ink:#111;--muted:#666;--line:#e5e7eb;--accent:#ffd200;--bg:#fff}
    *{box-sizing:border-box}
    body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,Segoe UI,Inter,Roboto,Helvetica,Arial,sans-serif}
    .wrap{max-width:880px;margin:24px auto;padding:0 12px}
    header{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:12px;margin:6px 0 12px}
    h1{font-size:20px;margin:0}
    form{display:block}
    fieldset{border:1px solid var(--line);border-radius:14px;padding:12px 12px 8px;margin:12px 0}
    legend{padding:0 6px;font-weight:800;font-size:13px;background:var(--accent);border-radius:6px}
    label{display:block;font-weight:600;font-size:13px;margin:10px 0 6px}
    .row2{display:grid;grid-template-columns:1fr 1fr;gap:10px}
    input[type="text"],input[type="email"],input[type="date"],input[type="number"],textarea,select{
      width:100%;border:1px solid var(--line);border-radius:10px;padding:10px;font:inherit;background:#fff
    }
    textarea{min-height:78px;resize:vertical}
    .muted{color:var(--muted);font-size:12px}
    .toolbar{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0}
    .btn{border:1px solid var(--line);background:#111;color:#fff;padding:.6rem .9rem;border-radius:12px;cursor:pointer;font-weight:700}
    .foot{display:flex;justify-content:space-between;align-items:center;margin:14px 0 18px;color:var(--muted);font-size:12px}
    @media (max-width:640px){ .row2{grid-template-columns:1fr} }
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <h1>JCT — Cuestionario Inicial</h1>
    </header>

    <form id="mainForm" action="https://getform.io/f/ayvexewb" method="POST">
      <input type="hidden" name="_next" value="#gracias">
      <fieldset>
        <legend>Datos personales</legend>
        <div class="row2">
          <div>
            <label for="nombre">Nombre completo *</label>
            <input id="nombre" name="nombre" type="text" required="" autocomplete="name">
          </div>
          <div>
            <label for="edad">Edad *</label>
            <input id="edad" name="edad" type="number" min="1" max="120" required="" placeholder="Ej: 35">
          </div>
        </div>
        <div class="row2">
          <div>
            <label for="email">Email *</label>
            <input id="email" name="email" type="email" placeholder="tu@email.com" required="" autocomplete="email">
          </div>
          <div>
            <label for="telefono">Teléfono *</label>
            <input id="telefono" name="telefono" type="text" required="" placeholder="+34 600 000 000" autocomplete="tel">
          </div>
        </div>

        <label for="objetivo">Objetivo principal <span class="muted">(elige y/o describe)</span></label>
        <select id="objetivo" name="objetivo">
          <option value="">Selecciona…</option>
          <option>Recomposición corporal</option>
          <option>Fuerza</option>
          <option>Pérdida de peso</option>
          <option>Ganancia muscular</option>
          <option>Rendimiento deportivo</option>
          <option>Salud postural / dolor</option>
          <option>Hábitos y salud general</option>
          <option>Otro</option>
        </select>
        <label for="objetivo_detalle" class="muted">Si quieres, concreta tu objetivo</label>
        <textarea id="objetivo_detalle" name="objetivo_detalle" placeholder="Ej.: perder 6–8 kg, mejorar sentadilla, preparar 10K, aliviar dolor lumbar…"></textarea>
      </fieldset>

      <fieldset>
        <legend>Hábitos básicos</legend>
        <label for="sueno_horas">Horas de sueño por noche</label>
        <select id="sueno_horas" name="sueno_horas">
          <option value="">Selecciona…</option>
          <option>≤5 h</option><option>6 h</option><option>7 h</option><option>8 h</option><option>9 h</option><option>≥10 h</option>
        </select>
        <label for="sueno_calidad">Calidad de sueño</label>
        <select id="sueno_calidad" name="sueno_calidad">
          <option value="">Selecciona…</option>
          <option>Mala</option><option>Regular</option><option>Buena</option><option>Excelente</option>
        </select>
        <label for="estres">Estrés (0–10)</label>
        <select id="estres" name="estres">
          <option value="">Selecciona…</option>
          <option>0</option><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option>
          <option>6</option><option>7</option><option>8</option><option>9</option><option>10</option>
        </select>
        
        <label>Consumo (selecciona todos los que apliquen)</label>
        <div role="group" aria-label="Consumos" style="display:grid;grid-template-columns:repeat(2,1fr);gap:6px;margin:6px 0">
          <label><input type="checkbox" name="consumo[]" value="Alcohol: nada"> Alcohol: nada</label>
          <label><input type="checkbox" name="consumo[]" value="Alcohol: ocasional"> Alcohol: ocasional</label>
          <label><input type="checkbox" name="consumo[]" value="Alcohol: frecuente"> Alcohol: frecuente</label>
          <label><input type="checkbox" name="consumo[]" value="Tabaco"> Tabaco</label>
          <label><input type="checkbox" name="consumo[]" value="Cafeína: baja"> Cafeína: baja</label>
          <label><input type="checkbox" name="consumo[]" value="Cafeína: moderada"> Cafeína: moderada</label>
          <label><input type="checkbox" name="consumo[]" value="Cafeína: alta"> Cafeína: alta</label>
          <label><input type="checkbox" name="consumo[]" value="Otro"> Otro</label>
        </div>
      </fieldset>

      <fieldset>
        <legend>Nutrición</legend>
        <label for="comidas">Comidas al día</label>
        <select id="comidas" name="comidas">
          <option value="">Selecciona…</option>
          <option>2</option><option>3</option><option>4</option><option>5</option><option>≥6</option>
        </select>
        <label for="alergias">Alergias / intolerancias</label>
        <select id="alergias" name="alergias">
          <option value="">Selecciona…</option>
          <option>Ninguna</option>
          <option>Gluten</option>
          <option>Lácteos</option>
          <option>Frutos secos</option>
          <option>Huevo</option>
          <option>Pescado / marisco</option>
          <option>Otro</option>
        </select>
        <label for="suplementos">Suplementación actual</label>
        <textarea id="suplementos" name="suplementos" placeholder="Creatina, multivitamínico, etc."></textarea>
      </fieldset>

      <fieldset>
        <legend>Entrenamiento actual</legend>
        <label for="experiencia">Experiencia</label>
        <select id="experiencia" name="experiencia">
          <option value="">Selecciona…</option>
          <option>Principiante</option><option>Intermedio</option><option>Avanzado</option>
        </select>
        <label for="cambios">¿Qué te gustaría cambiar?</label>
        <select id="cambios" name="cambios">
          <option value="">Selecciona…</option>
          <option>Composición corporal</option>
          <option>Rendimiento</option>
          <option>Dolor/postura</option>
          <option>Hábitos</option>
          <option>Otro</option>
        </select>

        <label>Días disponibles para entrenar</label>
        <div role="group" aria-label="Días disponibles" style="display:grid;grid-template-columns:repeat(4,minmax(120px,1fr));gap:6px">
          <label><input type="checkbox" name="dias[]" value="Lunes"> Lunes</label>
          <label><input type="checkbox" name="dias[]" value="Martes"> Martes</label>
          <label><input type="checkbox" name="dias[]" value="Miércoles"> Miércoles</label>
          <label><input type="checkbox" name="dias[]" value="Jueves"> Jueves</label>
          <label><input type="checkbox" name="dias[]" value="Viernes"> Viernes</label>
          <label><input type="checkbox" name="dias[]" value="Sábado"> Sábado</label>
          <label><input type="checkbox" name="dias[]" value="Domingo"> Domingo</label>
        </div>

        <label for="franja">Franja horaria preferida</label>
        <select id="franja" name="franja">
          <option value="">Selecciona…</option>
          <option>Mañana</option><option>Mediodía</option><option>Tarde</option><option>Noche</option><option>Variable</option>
        </select>

        <label for="preferencias_ejercicios">Preferencias generales de ejercicios</label>
        <select id="preferencias_ejercicios" name="preferencias_ejercicios">
          <option value="">Selecciona…</option>
          <option>Sin preferencias</option>
          <option>Evitar impacto</option>
          <option>Evitar overhead</option>
          <option>Prefiero máquinas</option>
          <option>Prefiero peso libre</option>
          <option>Otro</option>
        </select>

        <label for="ejercicios_gustan">Ejercicios que más te gustan</label>
        <textarea id="ejercicios_gustan" name="ejercicios_gustan" placeholder="Ej.: sentadilla, remo con barra, press banca, zancadas, remo con anillas…"></textarea>

        <label for="ejercicios_evitar">Ejercicios que prefieres evitar</label>
        <textarea id="ejercicios_evitar" name="ejercicios_evitar" placeholder="Ej.: correr, saltos, overhead, peso muerto convencional…"></textarea>
      </fieldset>

      <fieldset>
        <legend>Salud y lesiones</legend>
        <label for="diagnosticos">Diagnósticos previos / cirugías</label>
        <select id="diagnosticos" name="diagnosticos">
          <option value="">Selecciona…</option>
          <option>Ninguno</option><option>Columna</option><option>Hombro</option><option>Rodilla</option>
          <option>Tobillo</option><option>Cardiovascular</option><option>Otro</option>
        </select>
        <label for="medicacion">Medicación actual</label>
        <select id="medicacion" name="medicacion">
          <option value="">Selecciona…</option>
          <option>Ninguna</option><option>Antiinflamatorios</option><option>Analgésicos</option>
          <option>Antihipertensivos</option><option>Antidepresivos/ansiolíticos</option><option>Anticonceptivos</option><option>Otro</option>
        </select>
        <label for="molestias">Molestias al entrenar (0–10)</label>
        <select id="molestias" name="molestias">
          <option value="">Selecciona…</option>
          <option>0</option><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option>
          <option>6</option><option>7</option><option>8</option><option>9</option><option>10</option>
        </select>
        <label for="lesiones">Lesiones últimos 12 meses</label>
        <select id="lesiones" name="lesiones">
          <option value="">Selecciona…</option>
          <option>Ninguna</option><option>Columna</option><option>Hombro</option><option>Codo/Muñeca</option>
          <option>Cadera</option><option>Rodilla</option><option>Tobillo/Pie</option><option>Otro</option>
        </select>
      </fieldset>

      <fieldset>
        <legend>Entorno y preferencias</legend>
        <label for="disponibilidad_real">Disponibilidad semanal real</label>
        <select id="disponibilidad_real" name="disponibilidad_real">
          <option value="">Selecciona…</option>
          <option>1–2 sesiones</option><option>3 sesiones</option><option>4 sesiones</option>
          <option>5 sesiones</option><option>6–7 sesiones</option>
        </select>
        <label for="material">Material y espacio disponible</label>
        <select id="material" name="material">
          <option value="">Selecciona…</option>
          <option>Gimnasio completo</option>
          <option>Gimnasio básico</option>
          <option>Casa: mancuernas/bandas</option>
          <option>Solo peso corporal</option>
          <option>Exterior/parque</option>
        </select>
      </fieldset>

      <fieldset>
        <legend>Motivación y contexto</legend>
        <label for="motivo_contacto">¿Qué te trae por aquí? (motivo del contacto)</label>
        <textarea id="motivo_contacto" name="motivo_contacto" placeholder="Cuéntame en 2–3 frases qué te motivó a contactarme ahora, qué esperas conseguir y si hay una fecha u objetivo cercano." style="min-height:110px"></textarea>
      </fieldset>

      <fieldset>
        <legend>Consentimiento</legend>
        <label><input type="checkbox" id="consent" name="consent" value="Sí" required=""> He leído y acepto las recomendaciones de entrenamiento *</label>
        <label for="fecha">Fecha</label>
        <input id="fecha" type="date" name="fecha">
      </fieldset>

      <div class="toolbar">
        <button class="btn" type="submit">Enviar a JCT</button>
      </div>
    </form>

    <div class="foot">
      <span>© Javier Cancelas Training</span>
    </div>

    <!-- Mensaje de confirmación -->
    <div id="gracias" style="display:none;text-align:center;padding:60px 20px">
      <div style="max-width:600px;margin:0 auto">
        <div style="width:80px;height:80px;background:var(--accent);border-radius:50%;margin:0 auto 24px;display:flex;align-items:center;justify-content:center;font-size:48px">
          ✓
        </div>
        <h2 style="font-size:28px;margin:0 0 12px;color:var(--ink)">¡Recibido!</h2>
        <p style="font-size:18px;color:var(--muted);line-height:1.6;margin:0 0 24px">
          Gracias por tus respuestas.<br>
          Te contactaré pronto para comenzar tu entrenamiento.
        </p>
        <p style="font-size:14px;color:var(--muted)">
          Javier Cancelas Training
        </p>
      </div>
    </div>
  </div>

  <script>
    document.addEventListener('DOMContentLoaded', function() {
        const form = document.getElementById('mainForm');
        if (!form) return;

        const mainContent = document.querySelector('header').parentElement;
        const graciasMsg = document.getElementById('gracias');

        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            fetch(form.action, {
                method: 'POST',
                body: new FormData(form),
                headers: { 'Accept': 'application/json' }
            })
            .then(response => {
                if (response.ok) {
                    form.style.display = 'none';
                    if(document.querySelector('header')) document.querySelector('header').style.display = 'none';
                    if(document.querySelector('.foot')) document.querySelector('.foot').style.display = 'none';
                    if(graciasMsg) graciasMsg.style.display = 'block';
                } else {
                    alert('Hubo un problema al enviar. Por favor, inténtalo de nuevo.');
                }
            })
            .catch(error => {
                alert('Error de conexión. Verifica tu internet e inténtalo de nuevo.');
            });
        });
    });
  </script></body></html>
"""

# --- CONFIGURACIÓN Y CONEXIÓN A BD ---
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

# --- LÓGICA DE AUTENTICACIÓN ---
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
        # VISTA DE ADMINISTRADOR
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

        # AÑADIMOS LA NUEVA PESTAÑA "CUESTIONARIO INICIAL"
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Panel de Control", "Entrenamiento de Hoy", "Mi Historial", "Mis Rutinas", "Mi Progreso", "Cuestionario Inicial"])

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
            
        with tab5: # Mi Progreso
            st.header("Tu Evolución")
            st.write("---")
            data = {'Mes': pd.to_datetime(['2025-06-01', '2025-07-01', '2025-08-01', '2025-09-01', '2025-10-01', '2025-11-01']), 'Peso (kg)': [115.0, 112.0, 107.0, 108.0, 102.0, 100.5]}
            df_progreso = pd.DataFrame(data)
            chart = alt.Chart(df_progreso).mark_line(point=alt.OverlayMarkDef(color="yellow", size=100, filled=True)).encode(
                x=alt.X('Mes:T', title='Fecha'),
                y=alt.Y('Peso (kg):Q', title='Peso Corporal (kg)', scale=alt.Scale(domain=[80, 120])),
                tooltip=['Mes', 'Peso (kg)']).properties(height=400).configure_axis(labelColor='yellow', titleColor='yellow').configure_title(color='yellow').configure_view(stroke=None)
            st.altair_chart(chart, use_container_width=True)
            st.write("---")
            st.header("Consistencia de Entrenamiento")
            entrenamientos_mes_actual = 15; meta_mensual = 20
            _, center_metric_col, _ = st.columns([1, 1, 1])
            with center_metric_col: st.metric(label="Entrenamientos este mes", value=f"{entrenamientos_mes_actual} / {meta_mensual}")
            porcentaje_meta = int((entrenamientos_mes_actual / meta_mensual) * 100)
            st.progress(porcentaje_meta, text=f"Llevas el {porcentaje_meta}% de tu objetivo mensual")

        # --- PESTAÑA 6: CUESTIONARIO INICIAL ---
        with tab6:
            st.header("Cuestionario de Inicio")
            st.info("Por favor, completa este formulario para que podamos personalizar tu plan al máximo.")
            st.components.v1.html(cuestionario_html, height=1200, scrolling=True)

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
            if st.form_submit_button("Iniciar sesión"): login_user()```
