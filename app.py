import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la interfaz
st.set_page_config(page_title="ICG Master Monitor 2026", layout="wide")
st.title("🌎 Índice del Umbral de Conversión Geoeconómica (ICG)")
st.markdown("### Monitor de Vulnerabilidad y Poder de Choque Estratégico")

# 2. Base de Datos Maestra Final
data = {
    'Pais': [
        'EE.UU.', 'China', 'Irán', 'Venezuela', 'Rusia', 
        'Arabia Saudita', 'México', 'Vietnam', 'Guyana', 'Brasil', 'India'
    ],
    'ISO_Code': [
        'USA', 'CHN', 'IRN', 'VEN', 'RUS', 
        'SAU', 'MEX', 'VNM', 'GUY', 'BRA', 'IND'
    ],
    # Poder basado en recursos/tecnología (0 a 1)
    'Apalancamiento': [0.99, 0.90, 0.75, 0.82, 0.92, 0.90, 0.40, 0.65, 0.70, 0.75, 0.70],
    # Cuánto daño le hace un arancel de EE.UU. (0 a 1)
    'Sensibilidad_Arancelaria': [0.0, 0.75, 0.98, 0.99, 0.90, 0.30, 0.95, 0.50, 0.20, 0.35, 0.25],
    # Qué tan alineado está con el bloque dólar (0 a 1)
    'Alineacion_Oeste': [1.0, 0.1, 0.05, 0.05, 0.05, 0.60, 0.85, 0.70, 0.90, 0.50, 0.65]
}
df = pd.DataFrame(data)

# 3. Sidebar: El Factor Trump 2026
st.sidebar.header("🕹️ Panel de Control Geopolítico")
presion_global = st.sidebar.slider("Nivel de Aranceles/Sanciones (%)", 0, 100, 25)
st.sidebar.markdown("---")
st.sidebar.write("**Definición del ICG:** Mide la capacidad de un país para resistir presión externa y convertir sus recursos en poder político.")

# 4. Cálculo del Índice
# La fórmula: ICG = Apalancamiento - (Sensibilidad * Presión)
df['ICG_Final'] = (df['Apalancamiento'] - (df['Sensibilidad_Arancelaria'] * (presion_global / 100))) * 100

# 5. Mapa Mundial
fig = px.choropleth(
    df, 
    locations="ISO_Code", 
    color="ICG_Final",
    hover_name="Pais",
    hover_data=['Apalancamiento', 'Alineacion_Oeste'],
    projection="natural earth",
    color_continuous_scale="RdYlGn", # Rojo (Peligro) a Verde (Poder)
    range_color=[0, 100]
)
st.plotly_chart(fig, use_container_width=True)

# 6. Gráfico de Comparación Directa
st.subheader("📊 Comparativa de Resiliencia: Bloque Crítico")
fig_bar = px.bar(df.sort_values('ICG_Final'), x='Pais', y='ICG_Final', color='ICG_Final',
                 color_continuous_scale="RdYlGn", text_auto='.1f')
st.plotly_chart(fig_bar, use_container_width=True)

# 7. Conclusión Dinámica
st.markdown("---")
if presion_global > 70:
    st.error(f"⚠️ **ESTADO DE GUERRA ECONÓMICA:** Con un {presion_global}% de presión, Irán y Venezuela pierden casi toda su capacidad de maniobra. China entra en zona de recesión estratégica.")
elif presion_global < 30:
    st.success(f"✅ **COMPETENCIA DE MERCADO:** Con un {presion_global}% de presión, la mayoría de los países mantienen su umbral de conversión estable.")
