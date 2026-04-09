import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página
st.set_page_config(page_title="Índice Geoeconómico 2026", layout="wide")

st.title("🌐 Monitor del Umbral de Conversión Geoeconómica")
st.markdown("### Estrategia de Aranceles y Poder Global (Escenario 2026)")

# 2. Base de Datos Integrada (Para que no necesites archivos extra)
data = {
    'Pais': ['Estados Unidos', 'China', 'Irán', 'Alemania', 'India', 'Rusia', 'México', 'Taiwán'],
    'ISO_Code': ['USA', 'CHN', 'IRN', 'DEU', 'IND', 'RUS', 'MEX', 'TWN'],
    'Apalancamiento_Recursos': [0.98, 0.88, 0.75, 0.45, 0.60, 0.92, 0.35, 0.99],
    'Dependencia_EEUU': [0.05, 0.20, 0.02, 0.18, 0.15, 0.01, 0.88, 0.30],
    'Vulnerabilidad_Arancelaria': [0.0, 0.70, 0.95, 0.15, 0.10, 0.85, 0.40, 0.05]
}
df = pd.DataFrame(data)

# 3. Sidebar: El "Gatillo" de la Estrategia Trump
st.sidebar.header("🕹️ Simulador de Presión Geoeconómica")
st.sidebar.info("Ajusta el nivel de aranceles de EE.UU. para ver cómo colapsa o resiste el poder de conversión de otros países.")

arancel_usa = st.sidebar.slider("Nivel de Aranceles de EE.UU. (%)", 0, 100, 15)

# 4. Lógica del Índice (Fórmula de Conversión)
# El poder de conversión cae cuando el arancel impacta la economía del país objetivo
df['ICG_Final'] = (df['Apalancamiento_Recursos'] * (1 - (df['Vulnerabilidad_Arancelaria'] * (arancel_usa/100)))) * 100

# 5. Visualización del Mapa
fig = px.choropleth(
    df, 
    locations="ISO_Code", 
    color="ICG_Calculado" if 'ICG_Calculado' in df else "ICG_Final",
    hover_name="Pais",
    hover_data=['Apalancamiento_Recursos', 'Dependencia_EEUU'],
    projection="natural earth",
    color_continuous_scale=px.colors.sequential.YlOrRd,
    title="Mapa de Poder de Conversión Geoeconómica"
)

st.plotly_chart(fig, use_container_width=True)

# 6. Análisis Táctico
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Ranking de Poder")
    st.dataframe(df[['Pais', 'ICG_Final']].sort_values(by='ICG_Final', ascending=False))

with col2:
    st.subheader("Análisis de Situación")
    if arancel_usa > 50:
        st.warning("⚠️ ALTA PRESIÓN: El umbral de conversión de países dependientes (como México o China) se está reduciendo drásticamente. EE.UU. está 'armamentizando' su mercado doméstico.")
    else:
        st.success("✅ ESTABILIDAD RELATIVA: El poder de conversión se mantiene basado en recursos naturales y tecnología.")
