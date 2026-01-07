# 🔮 Nexus AI: Dashboard de Predicción de Ventas

## 📋 Descripción
Plataforma de **Business Intelligence (BI)** que transforma datos crudos en decisiones estratégicas. A diferencia de un dashboard tradicional, este sistema integra un módulo de **Inteligencia Artificial** para proyectar ingresos futuros.

## 🚀 Características Clave
* **🤖 Forecasting Predictivo:** Algoritmo de Regresión Lineal (NumPy) que analiza 2 años de historial para predecir las ventas del próximo trimestre.
* **🎯 Simulador de Metas:** Seguimiento de KPIs en tiempo real con barras de progreso dinámicas.
* **📥 Reportes Automatizados:** Exportación de data filtrada a Excel con un solo clic.

## 📸 Demo del Módulo IA
El sistema proyecta (línea punteada) el comportamiento futuro del mercado:

<img width="1190" height="795" alt="Dashboard_inteligencia1" src="https://github.com/user-attachments/assets/9b4d2d7a-c29e-4517-806e-638870d80511" />

## 🛠 Stack Tecnológico
* **Lenguaje:** Python 3.10
* **Visualización:** Plotly Interactive & Streamlit
* **Data Science:** NumPy & Pandas
* **Base de Datos:** SQLite

## 💻 Cómo ejecutarlo localmente
1.  Clonar el repositorio.
2.  Instalar dependencias: `pip install streamlit pandas plotly xlsxwriter`
3.  Generar data simulada: `python generar_data.py`
4.  Lanzar dashboard: `streamlit run app_final.py`

---
**Desarrollado por Marcos (MarcsEA)**
*Ingeniero en Informática | Especialista en Datos*
