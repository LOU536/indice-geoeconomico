import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración básica
st.set_page_config(page_title="Monitor Geoeconómico", layout="wide")

st.title("📊 Índice de Conversión Geoeconómica")
st.markdown("### Análisis de Estrategia Trump vs. Irán y China (2026)")

# Datos base (puedes expandir esto después)
data = {
    'Pais': ['Estados Unidos', 'China', 'Irán', 'Alemania', 'India', 'Rusia', 'México', 'Taiwán'],
    'ISO_Code': ['USA', 'CHN', 'IRN', 'DEU', 'IND', 'RUS', 'MEX', 'TWN'],
    'Apalancamiento': [0.95, 0.85, 0.70, 0.40, 0.55, 0.90, 0.30, 0.98],
    'Dependencia_EEUU': [0.05, 0.18, 0.02, 0.15, 0.12, 0.01, 0.85, 0.25],
    'Aranceles_Actuales': [0, 0.60, 0.95, 0.10, 0.05, 0.85, 0.25, 0.00]
}
df = pd.DataFrame(data)

# Barra lateral para simulación
st.sidebar.header("⚙️ Simulador de Presión")
arancel_global = st.sidebar.slider("Nivel de Aranceles Globales de EE.UU. (%)", 0, 100, 10)

# Cálculo dinámico del Índice (ICG)
df['ICG_Calculado'] = (df['Apalancamiento'] * (1 - (df['Aranceles_Actuales'] * (arancel_global/100)))) * 100

# Mapa
fig = px.choropleth(df, locations="ISO_Code", color="ICG_Calculado",
                    hover_name="Pais", projection="natural earth",
                    color_continuous_scale="YlOrRd")
st.plotly_chart(fig, use_container_width=True)

st.write("Datos actualizados al análisis geopolítico de 2026.")
