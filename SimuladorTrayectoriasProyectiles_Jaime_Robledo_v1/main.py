
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from modules import simulation, ammo
#css personalizado
css_path = "styles.css"

with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# Configuración de página
st.set_page_config(
    page_title="Simulador Balístico Profesional",
    page_icon="assets/Logo_Simulador_Proyectiles.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Header con logo
st.image("assets/Logo_Simulador_Proyectiles.png", width=200)
    

st.markdown("<h1 style='color: #000000'>SIMULADOR BALÍSTICO DE PROYECTILES</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #000000; font-size: 1.1rem; margin-bottom: 30px;'></p>", unsafe_allow_html=True)

# Diccionario de municiones
municion_dict = ammo.municion_dict

# Selección de munición principal
municion = st.selectbox(
    "TIPO DE MUNICIÓN",
    list(municion_dict.keys()),
    help="Selecciona el tipo de munición que quiere usar para la simulación, o 'Default' para parámetros personalizados."
)

# Parámetros de simulación
st.markdown("<p style='text-align: center; color: #000000; font-size: 1.1rem; margin-bottom: 30px;'></p>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    
    st.markdown("<div class='section-header' style='text-align: center; color: #000000;'>PARÁMETROS DE DISPARO</div>", unsafe_allow_html=True)
    
    if municion == "Default":
        v0 = st.slider("Velocidad Inicial (m/s)", 0, 5000, 400, 5)
        angulo = st.slider("Ángulo de Elevación (°)", 0, 90, 45, 1)
        y0 = st.slider("Altura Inicial (m)", 0, 1000, 0, 1)
    else:
        v0 = st.number_input("Velocidad Inicial (m/s)", value=municion_dict[municion]["v0"])
        angulo = st.slider("Ángulo de Elevación (°)", 0, 90, 45, 1)
        y0 = st.slider("Altura Inicial (m)", 0, 1000, 0, 1)
    
    st.markdown("<p style='text-align: center; color: #000000; font-size: 1.1rem; margin-bottom: 30px;'></p>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='section-header' style='text-align: center; color: #000000;'>CARACTERÍSTICAS BALÍSTICAS</div>", unsafe_allow_html=True)
    
    if municion == "Default":
        m = st.slider("Masa del Proyectil (kg)", 0.01, 125.0, 0.2, 0.01)
        cd = st.slider("Coeficiente de Arrastre (Cd)", 0.01, 2.0, 0.47, 0.01)
        d = st.slider("Diámetro (m)", 0.01, 1.0, 0.05, 0.01)
    else:
        m = st.number_input("Masa del Proyectil (kg)", value=municion_dict[municion]["m"], disabled=True)
        cd = st.number_input("Coeficiente de Arrastre (Cd)", value=municion_dict[municion]["Cd"], disabled=True)
        d = st.number_input("Diámetro (m)", value=municion_dict[municion]["d"], disabled=True)
    
    st.markdown("<p style='text-align: center; color: #000000; font-size: 1.1rem; margin-bottom: 30px;'></p>", unsafe_allow_html=True)

# Simulación
x_vals, y_vals, vx, vy, t, x_vals_perfecto, y_vals_perfecto, t_perfecto, energia_inicial, energia_final_real, energia_final_perfecta = simulation.graficar(
    v0=v0, angulo=angulo, m=m, cd=cd, d=d, y0=y0, 
    municion="Default", municion_dict=municion_dict, plot=False
)

# Gráfico profesional
fig, ax = plt.subplots(figsize=(14, 8), facecolor="#000000")
ax.set_facecolor("#ffffff")

# Zonas de fondo
ax.fill_betweenx(
    y=[-0.00001, 0], 
    x1=0, 
    x2=max(max(x_vals), max(x_vals_perfecto))/1000, 
    color="#4fe431", 
    alpha=1,
    label='Tierra'
)
ax.fill_betweenx(
    y=[0, max(max(y_vals), max(y_vals_perfecto))/1000], 
    x1=0, 
    x2=max(max(x_vals), max(x_vals_perfecto))/1000, 
    color="#21DEF0", 
    alpha=0.35,
    label='Cielo'
)

# Trayectorias
ax.plot(np.array(x_vals)/1000, np.array(y_vals)/1000, 
        color="#ff0000", linewidth=2.5, label='Con Resistencia Aerodinámica', alpha=1)
ax.plot(np.array(x_vals_perfecto)/1000, np.array(y_vals_perfecto)/1000, 
        color="#001eff", linewidth=2, linestyle='--', label='Vacío Ideal', alpha=1)

# Puntos críticos
idx = np.argmax(y_vals)
idx_perfecto = np.argmax(y_vals_perfecto)

ax.plot(x_vals[idx]/1000, y_vals[idx]/1000, 'o', color="#ffff00", 
        markersize=10, label='Altura Máxima (Real)', markeredgecolor='Black', markeredgewidth=1.5)
ax.plot(x_vals[-1]/1000, 0, 's', color="#FF7700", 
        markersize=10, label='Punto de Impacto', markeredgecolor='Black', markeredgewidth=1.5)
ax.plot(x_vals_perfecto[idx_perfecto]/1000, y_vals_perfecto[idx_perfecto]/1000, 
        'o', color="#ffff00", markersize=8, alpha=1, markeredgecolor='Black', markeredgewidth=1)
ax.plot(x_vals_perfecto[-1]/1000, 0, 's', color="#FF7700", 
        markersize=8, alpha=1, markeredgecolor='Black', markeredgewidth=1)

# Estilo del gráfico
ax.set_xlabel("Distancia Horizontal (km)", fontsize=12, color="#ffffff", fontweight='600')
ax.set_ylabel("Altitud (km)", fontsize=12, color='#ffffff', fontweight='600')
ax.set_title("Comparativa de Trayectorias Balísticas", fontsize=14, color='#ffffff', 
             fontweight='700', pad=20)
ax.grid(True, linestyle='--', alpha=0.2, color='#4a5568')
ax.tick_params(colors='#ffffff', labelsize=10)
ax.spines['bottom'].set_color('#2d3748')
ax.spines['top'].set_color('#2d3748')
ax.spines['left'].set_color('#2d3748')
ax.spines['right'].set_color('#2d3748')

legend = ax.legend(loc='upper right', fontsize=10, framealpha=0.9, 
                   facecolor="#ffffff", edgecolor="#000000", labelcolor="#000000")

st.pyplot(fig)

# Resultados en formato profesional
st.markdown("<p style='text-align: center; color: #000000; font-size: 1.1rem; margin-bottom: 30px;'></p>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #000000;'>RESULTADOS DE LA SIMULACIÓN</h3>", unsafe_allow_html=True)


col1, col2 = st.columns(2)

with col1:
    st.markdown("<p style='text-align: center; color: #000000; font-size: 1.1rem; margin-bottom: 30px;'></p>", unsafe_allow_html=True)
    st.markdown("<div class='section-header' style='color: #000000;'>CONDICIONES REALES (con resistencia aerodinámica)</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='metric-box'>
        <div class='metric-title' style='color: #ffffff;'>Alcance Máximo</div>
        <div class='metric-value-1'>{max(x_vals)/1000:.3f} km</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='metric-box'>
        <div class='metric-title' style='color: #ffffff;'>Altura Máxima</div>
        <div class='metric-value-1'>{max(y_vals)/1000:.3f} km</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='metric-box'>
        <div class='metric-title' style='color: #ffffff;'>Tiempo de Vuelo</div>
        <div class='metric-value-1'>{t:.2f} s</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='metric-box'>
        <div class='metric-title' style='color: #ffffff;'>Energía Cinética al Impacto</div>
        <div class='metric-value-1'>{energia_final_real:.2f} J</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("<p style='text-align: center; color: #000000; font-size: 1.1rem; margin-bottom: 30px;'></p>", unsafe_allow_html=True)
    st.markdown("<div class='section-header' style='color: #000000;'>CONDICIONES IDEALES (vacío teórico)</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='metric-box'>
        <div class='metric-title' style='color: #ffffff;'>Alcance Máximo</div>
        <div class='metric-value-2'>{max(x_vals_perfecto)/1000:.3f} km</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='metric-box'>
        <div class='metric-title' style='color: #ffffff;'>Altura Máxima</div>
        <div class='metric-value-2'>{max(y_vals_perfecto)/1000:.3f} km</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='metric-box'>
        <div class='metric-title' style='color: #ffffff;'>Tiempo de Vuelo</div>
        <div class='metric-value-2'>{t_perfecto:.2f} s</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='metric-box'>
        <div class='metric-title' style='color: #ffffff;'>Energía Cinética al Impacto</div>
        <div class='metric-value-2'>{energia_final_perfecta:.2f} J</div>
    </div>
    """, unsafe_allow_html=True)

# Análisis de diferencias
st.markdown("<p style='text-align: center; color: #000000; font-size: 1.1rem; margin-bottom: 30px;'></p>", unsafe_allow_html=True)
st.markdown("<div class='section-header' style='color: #000000;'>ANÁLISIS COMPARATIVO</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

dif_alcance = ((max(x_vals_perfecto) - max(x_vals)) / max(x_vals_perfecto)) * 100
dif_altura = ((max(y_vals_perfecto) - max(y_vals)) / max(y_vals_perfecto)) * 100
dif_tiempo = ((t_perfecto - t) / t_perfecto) * 100

with col1:
    st.markdown(f"""
    <div class='metric-box'>
        <div class='metric-title' style='color: #ffffff;'>Reducción de Alcance</div>
        <div class='metric-value-1'>{dif_alcance:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='metric-box'>
        <div class='metric-title' style='color: #ffffff;'>Reducción de Altura</div>
        <div class='metric-value-1'>{dif_altura:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='metric-box'>
        <div class='metric-title' style='color: #ffffff;'>Reducción de Tiempo</div>
        <div class='metric-value-1'>{dif_tiempo:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<p style='text-align: center; color: #000000; font-size: 1.1rem; margin-bottom: 30px;'></p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #4a5568; font-size: 0.9rem;'>Jaime Robledo | Ingenieria de Software y Matematicas</p>", unsafe_allow_html=True)