import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import io
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Nexus AI Dashboard",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    h1 { color: #1f2937; }
    .stProgress > div > div > div > div { background-color: #4F46E5; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def cargar_datos():
    conn = sqlite3.connect('ventas_final.db')
    query = """
    SELECT p.fecha, p.total, p.producto, p.categoria, c.nombre as cliente, c.sector
    FROM pedidos p JOIN clientes c ON p.cliente_id = c.cliente_id
    ORDER BY p.fecha
    """
    try:
        df = pd.read_sql_query(query, conn)
        conn.close()
        df['fecha'] = pd.to_datetime(df['fecha'])
        return df
    except:
        return None

def predecir_ventas(df):
    df_mensual = df.set_index('fecha').resample('M')['total'].sum().reset_index()
    df_mensual['mes_ordinal'] = df_mensual['fecha'].map(datetime.toordinal)
    
    X = df_mensual['mes_ordinal'].values.reshape(-1, 1)
    y = df_mensual['total'].values
    
    coeficientes = np.polyfit(X.flatten(), y, 1)
    polinomio = np.poly1d(coeficientes)
    
    ultima_fecha = df_mensual['fecha'].iloc[-1]
    fechas_futuras = [ultima_fecha + timedelta(days=30*i) for i in range(1, 4)]
    ordinales_futuros = [d.toordinal() for d in fechas_futuras]
    
    predicciones = polinomio(ordinales_futuros)
    
    return df_mensual, fechas_futuras, predicciones

df = cargar_datos()
if df is None:
    st.error("Error: Ejecuta primero 'generar_data.py'")
    st.stop()

with st.sidebar:
    st.title("🔮 Nexus AI")
    st.markdown("Intelligence Suite v3.0")
    st.markdown("---")
    
    menu = st.radio("Menú Principal", 
        ["🏠 Dashboard General", "🔮 Predicción IA", "🎯 Metas y Objetivos", "📥 Datos y Reportes"],
    )
    
    st.markdown("---")
    cat_filtro = st.multiselect("Categoría", df['categoria'].unique(), default=df['categoria'].unique())

df_filtered = df[df['categoria'].isin(cat_filtro)]

if menu == "🏠 Dashboard General":
    st.title("📊 Resumen Ejecutivo")
    
    total_ventas = df_filtered['total'].sum()
    total_ordenes = len(df_filtered)
    promedio = df_filtered['total'].mean()
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Ingresos Totales", f"${total_ventas:,.0f}", "+8.4%")
    c2.metric("Transacciones", f"{total_ordenes}", "+120")
    c3.metric("Ticket Promedio", f"${promedio:,.0f}", "-2.1%")
    
    col_chart1, col_chart2 = st.columns([2,1])
    
    with col_chart1:
        st.subheader("Evolución de Ventas")
        df_dia = df_filtered.set_index('fecha').resample('M')['total'].sum().reset_index()
        fig = px.area(df_dia, x='fecha', y='total', color_discrete_sequence=['#4F46E5'])
        st.plotly_chart(fig, use_container_width=True)
        
    with col_chart2:
        st.subheader("Mix de Productos")
        fig2 = px.pie(df_filtered, names='categoria', values='total', hole=0.6)
        st.plotly_chart(fig2, use_container_width=True)

elif menu == "🔮 Predicción IA":
    st.title("🔮 Forecasting Inteligente")
    st.markdown("Proyección de ingresos para el próximo trimestre basada en regresión lineal histórica.")
    
    df_hist, fechas_futuras, valores_futuros = predecir_ventas(df_filtered)
    
    fig_pred = go.Figure()
    
    fig_pred.add_trace(go.Scatter(
        x=df_hist['fecha'], y=df_hist['total'],
        mode='lines+markers', name='Histórico Real',
        line=dict(color='#4F46E5', width=3)
    ))
    
    fig_pred.add_trace(go.Scatter(
        x=fechas_futuras, y=valores_futuros,
        mode='lines+markers', name='Proyección IA',
        line=dict(color='#10B981', width=3, dash='dot')
    ))
    
    fig_pred.update_layout(template="plotly_white")
    st.plotly_chart(fig_pred, use_container_width=True)
    
    total_proyectado = sum(valores_futuros)
    st.success(f"Análisis IA: Se proyectan ingresos adicionales de **${total_proyectado:,.0f}** para los próximos 90 días.")

elif menu == "🎯 Metas y Objetivos":
    st.title("🎯 Control de Performance")
    
    col1, col2 = st.columns([1,2])
    with col1:
        meta = st.number_input("Meta de Ventas Anual ($)", value=1000000, step=50000)
    
    with col2:
        actual = df_filtered['total'].sum()
        progreso = min(actual / meta, 1.0)
        
        st.progress(progreso)
        st.caption(f"Progreso: ${actual:,.0f} / ${meta:,.0f} ({progreso*100:.1f}%)")
        
        if progreso == 1.0:
            st.balloons()

elif menu == "📥 Datos y Reportes":
    st.title("📥 Exportación de Data")
    
    st.dataframe(df_filtered.head(50), use_container_width=True)
    
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df_filtered.to_excel(writer, index=False, sheet_name='Data_Cruda')
    writer.close()
    processed_data = output.getvalue()
    
    st.download_button(
        label="📄 Descargar Reporte Excel",
        data=processed_data,
        file_name="Reporte_Nexus_AI.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary")