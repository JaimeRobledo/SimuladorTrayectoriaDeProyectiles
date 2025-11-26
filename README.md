#Simulador de Trayectoria de Proyectiles

Este proyecto implementa un simulador interactivo que calcula la trayectoria realista de un proyectil en 2D considerando gravedad, densidad del aire dependiente de la altitud, arrastre aerodinámico, coeficiente balístico, tipo de munición, velocidad inicial y altura inicial.
Incluye una interfaz con sliders dinámicos, cálculo automático de parámetros y visualización mediante Matplotlib y Streamlit.

#Características principales

Trayectoria con física real: integración numérica de las ecuaciones de movimiento (pos. y vel.), arrastre dependiente de velocidad y densidad.

Densidad del aire dinámica: modelo exponencial p = p0 * e^(-y / 8500).

Cálculo automático del ángulo para impactar un objetivo (función iterativa de búsqueda de ángulo).

Interfaz interactiva con sliders o inputs automáticos según munición (Streamlit + ipywidgets opcional para notebooks).

Visualización profesional con Matplotlib integrada en Streamlit.

#Tecnologías utilizadas

Python 3

Matplotlib

NumPy

Streamlit

ipywidgets (opcional para Jupyter)

(Opcional) Módulo personalizado ammo.py

#Estructura del proyecto
Simulador-Balistico/
│
├── main.py                    # App principal Streamlit (o app.py según prefieras)
├── simulation.py              # Lógica de simulación (RK4, drag, densidad, etc.)
├── ammo.py                    # Diccionario de municiones y parámetros
├── styles.css                 # Estilos CSS a la misma altura que main.py
├── README.md
└── assets/
    ├── Logo_Simulador_Proyectiles.png
    └── capturas/
        └── ejemplo_plot.png


Nota: Si guardas styles.css en assets/, adapta la lógica de carga; el README asume que styles.css está en el mismo nivel que main.py.

#Funciones principales (resumen)

densidad_atmosfera(y)

f(u, m, g, cd, area, p) — deriva estado [x, y, vx, vy]

calcular_resistencia_aire(...) — solver RK4 (devuelve arrays de x,y y velocidades)

objetivoPedido(...) — busca ángulo para impactar un X dado

actualizar_sliders(...) — lógica para mostrar sliders o inputs según munición

#Cómo funciona RK4 (breve)

El método Runge–Kutta de orden 4 (RK4) estima la solución de du/dt = f(t, u) con cuatro evaluaciones intermedias por paso (k1..k4) y combina estas para obtener u_next. Para el sistema [x, y, vx, vy] esto permite integrar con alta precisión fuerzas no lineales (drag dependiente de v², densidad variable, etc.).

Ecuación de actualización (paso dt):

k1 = f(t, u)
k2 = f(t + dt/2, u + dt*k1/2)
k3 = f(t + dt/2, u + dt*k2/2)
k4 = f(t + dt,   u + dt*k3)
u_next = u + (dt/6) * (k1 + 2*k2 + 2*k3 + k4)

#Demostración visual — Cómo inicializar Streamlit
1) Instalar dependencias (entorno virtual recomendado)
python -m venv .venv
source .venv/bin/activate       # Linux / macOS
# .venv\Scripts\activate       # Windows PowerShell

pip install -r requirements.txt
# o instalar manualmente:
pip install streamlit numpy matplotlib


Si usas ipywidgets dentro de Jupyter: pip install ipywidgets (opcional).

2) Ejecutar la app Streamlit

Desde la raíz del proyecto (donde está main.py y styles.css):

streamlit run main.py


Al ejecutarlo verás en la consola una línea similar a:

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501


Abre http://localhost:8501 en tu navegador.

3) Qué esperar en la interfaz

Encabezado con logo y título.

Selector de TIPO DE MUNICIÓN. Si eliges una munición, los sliders de masa/Cd/diámetro se reemplazan por inputs fijos (no se muestran los sliders).

Paneles con:

Parámetros de disparo (velocidad, ángulo, altura).

Características balísticas (masa, Cd, diámetro).

Botón/acción automática: la simulación se recalcula al cambiar parámetros.

Gráfico con:

Trayectoria real (con arrastre).

Trayectoria ideal (vacío).

Punto de impacto, altura máxima.


Panel final con métricas: alcance, altura máxima, tiempo de vuelo, energía cinética al impacto, y comparativa entre real y teórico.

Ejemplo rápido (parámetros)
v0 = 900     # m/s
angulo = 20  # grados
masa = 0.009 # kg
cd = 0.295
altura = 0


Estos valores producen la gráfica de la trayectoria y las métricas mostradas en la interfaz.

#Estilos CSS

Si usas styles.css junto a main.py, aplica en la parte superior de main.py:

from pathlib import Path
import streamlit as st

css_path = Path(__file__).parent / "styles.css"
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


Esto hace que todas las clases CSS que uses en st.markdown(..., unsafe_allow_html=True) (p. ej. .metric-box, .section-header) se apliquen correctamente.

#Cómo ejecutar en Jupyter (opcional)

Instala dependencias y abre el notebook:

pip install jupyterlab ipywidgets numpy matplotlib
jupyter notebook  # o jupyter lab


Abre simulador.ipynb y ejecuta las celdas. (Si usas widgets, activa la extensión de widgets si es necesario).

#Contribuciones

Bienvenidas: ampliar físicas (viento, Magnus, Coriolis), exportar resultados, añadir comparador de municiones, mejorar performance (numba), migrar a una versión 3D, etc. Haz fork y pull request.

#Autor

Jaime Robledo
Estudiante de Ingeniería de Software y Matemáticas
Desarrollador del proyecto Simulador Bal