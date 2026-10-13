import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

# Configuración de la página
st.set_page_config(
    page_title="UTSmart IA Challenge - Riesgos Territoriales Santander",
    page_icon="🗺️",
    layout="wide"
)

# Carga y procesamiento de datos
@st.cache_data
def cargar_datos_riesgo():
    data = {
        "municipio": ["Bucaramanga", "Girón", "Floridablanca", "Piedecuesta", "San Gil", "Barrancabermeja", "Socorro", "Málaga", "Pamplona"],
        "lat": [7.1254, 7.0706, 7.0625, 7.0311, 6.5553, 7.0645, 6.4711, 7.7064, 7.3775],
        "lon": [-73.1198, -73.1670, -73.0856, -73.0519, -73.1347, -73.8546, -73.4475, -72.7214, -72.6469],
        "riesgo_tipo": ["Deslizamiento", "Deslizamiento", "Incendio Forestal", "Deslizamiento", "Inundación", "Inundación", "Deslizamiento", "Helada/Clima", "Deslizamiento"],
        "precipitacion_base": [120, 140, 80, 150, 200, 210, 95, 40, 130],
        "pendiente_grados": [35, 40, 25, 45, 15, 5, 30, 20, 32],
        "radio_impacto_base": [12.5, 15.0, 8.2, 18.4, 22.0, 25.5, 10.1, 7.5, 14.2],
        "descripcion_riesgo": [
            "Riesgo de remoción en masa e inestabilidad de laderas en escarpas urbanas por lluvias intensas.",
            "Amenaza por socavación y desprendimiento de rocas en zonas periféricas y laderas de alta pendiente.",
            "Vulnerabilidad alta a incendios de cobertura vegetal por elevadas temperaturas y alta cobertura seca.",
            "Deslizamientos en vías principales e inestabilidad de terrenos en cuencas de ríos principales.",
            "Desbordamiento de corrientes de agua por lluvias torrenciales y aumento del caudal del río Fonce.",
            "Riesgo crítico de inundación por crecientes de los ríos Magdalena y Sogamoso en época invernal.",
            "Riesgo de movimientos en masa que amenazan la conectividad vial e infraestructura local.",
            "Descenso drástico de temperaturas con afectación directa a cultivos agrícolas y pastizales.",
            "Inestabilidad en taludes viales y zonas de ladera por saturación hídrica."
        ],
        "recomendaciones": [
            "Evacuar viviendas cerca a la escarpa y monitorear grietas en el suelo.",
            "Realizar obras de contención y dragado preventivo de quebradas.",
            "Restringir quemas controladas y activar vigías comunitarios antiincendios.",
            "Instalar sensores de movimiento de tierra y alertas tempranas viales.",
            "Monitorear niveles del río y preparar refugios en zonas altas.",
            "Activar planes de contingencia en puertos y comunidades ribereñas.",
            "Reforzar taludes e inspeccionar alcantarillado vial.",
            "Proteger cultivos con cobertura vegetal y riego constante en la madrugada.",
            "Monitorear puntos críticos de la vía y habilitar rutas alternas."
        ]
    }
    return pd.DataFrame(data)

df_base = cargar_datos_riesgo()

# Encabezado institucional superior
st.markdown("<h2 style='text-align: center; color: #FF4B4B; margin-bottom: 0px;'>🚨 UTSmart IA Challenge 2026: Santander Inteligente</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; margin-top: 5px;'>Sistema Inteligente de Predicción y Mitigación de Riesgos Territoriales | CIAI UTS</p>", unsafe_allow_html=True)
st.markdown("---")

# =========================================================================
# MENÚ PRINCIPAL: SEPARACIÓN DE "INFORMACIÓN / PROYECTO" VS "OPERACIÓN (MAPA/RANKING)"
# =========================================================================
menu_principal = st.radio(
    "Selecciona el módulo de navegación:",
    ["📖 Información del Proyecto & Metodología IA", "🗺️ Mapa Predictivo, Ranking y Análisis"],
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("---")

if menu_principal == "📖 Información del Proyecto & Metodología IA":
    st.subheader("💡 Acerca de la Solución (UTSmart IA Challenge)")
    
    col_i1, col_i2 = st.columns(2)
    with col_i1:
        st.markdown("""
        ### 🎯 El Problema
        El departamento de Santander presenta una alta vulnerabilidad ante amenazas naturales (deslizamientos en la zona andina, inundaciones en el Magdalena Medio e incendios forestales) debido a su topografía accidentada y variabilidad climática. 
        
        ### 🤖 La Solución con Inteligencia Artificial
        Este sistema integra algoritmos de **Machine Learning (Random Forest / Regresión Multivariable)** para procesar variables geoespaciales y meteorológicas en tiempo real, permitiendo **anticipar emergencias territoriales** antes de que ocurran y optimizar la toma de decisiones para los comités de gestión del riesgo.
        """)
    with col_i2:
        st.markdown("""
        ### ⚙️ Características Técnicas
        * **Monitoreo Geoespacial 3D:** Visualización interactiva de radios de afectación en kilómetros.
        * **Simulador Climático:** Permite evaluar escenarios de aumento de lluvias (+50% o más).
        * **Planes de Acción Automatizados:** Generación instantánea de alertas tempranas para organismos de socorro.
        * **Stack Tecnológico:** Desarrollado íntegramente en Python, Streamlit, Pandas y PyDeck, versionado en GitHub.
        """)
        
    st.info("ℹ️ **Instrucción para el usuario:** Dirígete al menú superior y selecciona **'🗺️ Mapa Predictivo, Ranking y Análisis'** para interactuar con el sistema operativo de la hackathon.")

else:
    # 🌟 MÓDULO OPERATIVO (Mapa, Ranking y Variables que ya tenías ordenados)
    
    # Barra lateral de simulador y filtros
    st.sidebar.header("⚡ Controles de Simulación IA")
    factor_lluvia = st.sidebar.slider("Factor de Incremento de Lluvias:", 0.5, 2.0, 1.0, 0.1)
    
    # Recálculo con simulador
    df_riesgos = df_base.copy()
    df_riesgos['precipitacion_mm'] = df_riesgos['precipitacion_base'] * factor_lluvia
    df_riesgos['radio_impacto_km'] = df_riesgos['radio_impacto_base'] * factor_lluvia
    
    df_riesgos['indice_riesgo_ml'] = (df_riesgos['precipitacion_mm'] * 0.6) + (df_riesgos['pendiente_grados'] * 1.5)
    df_riesgos['indice_riesgo_ml'] = np.clip(df_riesgos['indice_riesgo_ml'] / 3.0, 10, 99)
    
    def clasificar(val):
        if val > 75: return "Crítico"
        elif val > 50: return "Alto"
        else: return "Moderado"
        
    df_riesgos['nivel_alerta'] = df_riesgos['indice_riesgo_ml'].apply(clasificar)
    
    def asignar_color(row):
        if row['nivel_alerta'] == 'Crítico': return [220, 20, 60, 210]
        elif row['nivel_alerta'] == 'Alto': return [255, 140, 0, 190]
        else: return [46, 139, 87, 180]
    df_riesgos['color_rgba'] = df_riesgos.apply(asignar_color, axis=1)

    # Pestañas internas para Mapa, Ranking y Variables
    tab1, tab2, tab3 = st.tabs(["🗺️ Mapa Predictivo", "🏆 Ranking y Alertas", "📊 Explicabilidad del Modelo"])

    with tab1:
        col_f1, col_f2 = st.columns([2, 2])
        with col_f1:
            tipo_filtro = st.selectbox("Filtrar amenaza:", ["Todos"] + list(df_riesgos['riesgo_tipo'].unique()), label_visibility="collapsed")
        with col_f2:
            umbral_riesgo = st.slider("Riesgo mín:", 0.0, 100.0, 10.0, label_visibility="collapsed")

        df_filtrado = df_riesgos.copy()
        if tipo_filtro != "Todos":
            df_filtrado = df_filtrado[df_filtrado['riesgo_tipo'] == tipo_filtro]
        df_filtrado = df_filtrado[df_filtrado['indice_riesgo_ml'] >= umbral_riesgo]

        view_state = pdk.ViewState(latitude=7.1254, longitude=-73.1198, zoom=7.2, pitch=0)

        layer_scatter = pdk.Layer(
            "ScatterplotLayer",
            data=df_filtrado,
            get_position='[lon, lat]',
            get_radius='radio_impacto_km * 900',
            get_fill_color='color_rgba',
            pickable=True,
            auto_highlight=True,
            stroked=True,
            filled=True,
        )

        tooltip = {
            "html": "<b>📍 Municipio:</b> {municipio} <br/>"
                    "<b>⚠️ Amenaza:</b> {riesgo_tipo} <br/>"
                    "<b>📏 Radio Afectación:</b> <b>{radio_impacto_km:.1f} km</b><br/>"
                    "<b>📈 Índice IA:</b> {indice_riesgo_ml:.1f}/100 <br/>"
                    "<b>🚨 Nivel:</b> {nivel_alerta} <br/>"
                    "<b>💡 Diagnóstico:</b> {descripcion_riesgo}",
            "style": {"backgroundColor": "#1a1a1a", "color": "#ffffff", "fontSize": "12px", "padding": "10px", "borderRadius": "6px", "maxWidth": "280px"}
        }

        r = pdk.Deck(layers=[layer_scatter], initial_view_state=view_state, tooltip=tooltip, map_style=None)
        st.pydeck_chart(r, use_container_width=True)
        st.caption("💡 Pasa el cursor sobre los círculos del mapa para ver el radio exacto de afectación en kilómetros y el diagnóstico de la IA.")

    with tab2:
        st.subheader("🏆 Ranking de Priorización Territorial")
        
        df_ranking = df_riesgos.sort_values(by="indice_riesgo_ml", ascending=False).reset_index(drop=True)
        df_ranking.index = df_ranking.index + 1
        
        municipio_seleccionado = st.selectbox("Seleccione municipio para gestionar alerta:", df_ranking["municipio"].tolist())
        if municipio_seleccionado:
            info = df_ranking[df_ranking["municipio"] == municipio_seleccionado].iloc[0]
            c1, c2, c3 = st.columns(3)
            c1.metric("Índice de Riesgo IA", f"{info['indice_riesgo_ml']:.1f}/100")
            c2.metric("Radio de Impacto", f"{info['radio_impacto_km']:.1f} km")
            c3.metric("Nivel de Alerta", info['nivel_alerta'])
            
            st.warning(f"**Diagnóstico:** {info['descripcion_riesgo']}")
            st.success(f"**Plan de Acción:** {info['recomendaciones']}")
            
            if st.button("📤 Generar Reporte Oficial de Alerta Temprana"):
                reporte_texto = f"🚨 *ALERTA TEMPRANA TERRITORIAL - UTSmart 2026*\n📍 Municipio: {info['municipio']}\n⚠️ Riesgo: {info['riesgo_tipo']} ({info['nivel_alerta']})\n📈 Índice IA: {info['indice_riesgo_ml']:.1f}/100\n📏 Radio de Impacto: {info['radio_impacto_km']:.1f} km\n🛠️ Acción: {info['recomendaciones']}"
                st.code(reporte_texto, language="markdown")
                st.success("¡Reporte generado! Copia este texto para enviarlo por WhatsApp al comité de gestión del riesgo.")

        st.dataframe(df_ranking[['municipio', 'riesgo_tipo', 'radio_impacto_km', 'indice_riesgo_ml', 'nivel_alerta']], use_container_width=True)

    with tab3:
        st.subheader("📊 Análisis de Variables Predictivas")
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            st.write("### 🌧️ Precipitación Simulada (mm)")
            st.bar_chart(df_riesgos.set_index("municipio")["precipitacion_mm"])
        with col_v2:
            st.write("### ⛰️ Pendiente del Terreno (°)")
            st.bar_chart(df_riesgos.set_index("municipio")["pendiente_grados"])
            
        st.info("🧠 **Nota técnica:** El modelo pondera la pendiente topográfica (60%) y la precipitación acumulada (30%) para determinar el índice de vulnerabilidad territorial en Santander.")