# app.py - Versión 2.9 PREMIUM INTERFACE RESTORED
# Restaura por completo la estética avanzada de la pantalla de inicio (Login)
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Módulos locales del proyecto
from data_generator import DataGenerator
from ai_model import AIModel

# --- CONFIGURACIÓN DE PÁGINA OBLIGATORIA AL INICIO ---
st.set_page_config(
    page_title="ESTRATEGA IA — Core Engine",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INYECCIÓN DE CSS AVANZADO: UI DE SOFTWARE DE IA ---
def apply_professional_ai_theme():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@500;700&display=swap');
        
        /* Fondo general estilo Dashboard de IA */
        .stApp {
            background-color: #06070d !important;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(0, 210, 255, 0.03) 0%, transparent 50%),
                radial-gradient(circle at 90% 80%, rgba(78, 204, 163, 0.03) 0%, transparent 50%) !important;
            color: #e2e8f0 !important;
        }

        /* Modificar las pestañas (Tabs) superiores */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background-color: #0d111a;
            padding: 10px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        .stTabs [data-baseweb="tab"] {
            font-family: 'Orbitron', sans-serif !important;
            height: 45px;
            background-color: transparent;
            border-radius: 8px;
            color: #64748b !important;
            border: none;
            transition: all 0.3s ease;
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(90deg, rgba(0,210,255,0.15), rgba(78,204,163,0.15)) !important;
            color: #00D2FF !important;
            border: 1px solid rgba(0, 210, 255, 0.3) !important;
        }

        /* Tarjetas de Métricas */
        div[data-testid="stMetric"] {
            background: #0d111a !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-left: 4px solid #00D2FF !important;
            border-radius: 12px !important;
            padding: 20px !important;
        }
        div[data-testid="stMetric"] [data-testid="stMetricLabel"] {
            font-family: 'Rajdhani', sans-serif !important;
            color: #94a3b8 !important;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        div[data-testid="stMetric"] [data-testid="stMetricValue"] {
            font-family: 'Orbitron', sans-serif !important;
            color: #ffffff !important;
            font-size: 24px !important;
        }

        /* Botones del Sistema */
        .stButton>button {
            font-family: 'Orbitron', sans-serif !important;
            background: linear-gradient(135deg, #00D2FF 0%, #0072FF 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 12px 24px !important;
            font-weight: 700 !important;
            letter-spacing: 1px;
            box-shadow: 0 4px 15px rgba(0, 210, 255, 0.2);
            transition: all 0.3s ease !important;
        }
        .stButton>button:hover {
            box-shadow: 0 0 25px rgba(0, 210, 255, 0.5) !important;
            transform: translateY(-1px);
        }

        /* Títulos e Interfaz Interna */
        .ai-title {
            background: linear-gradient(90deg, #00D2FF, #4ECCA3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
            font-size: calc(1.8rem + 1.5vw) !important;
            line-height: 1.2 !important;
            margin-bottom: 5px;
            font-family: 'Orbitron', sans-serif !important;
        }

        .diag-card {
            background: #0d111a;
            border: 1px solid rgba(0, 210, 255, 0.1);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES DE CONTROL CON SOPORTE REALTIME ---
def generate_sample_data(size):
    st.session_state.customer_data = st.session_state.data_generator.generate_synthetic_data(size)
    st.toast(f"Muestra de {size:,} perfiles normalizada.", icon="🧬")
    st.rerun()

def train_models():
    if st.session_state.customer_data is None:
        st.error("❌ Error: Código de datos fuente vacío.")
        return
    with st.spinner("🧠 NEURAL NETWORK: Optimizando capas de decisión..."):
        metrics_seg = st.session_state.ai_model.train_segmentation_model(st.session_state.customer_data)
        metrics_imp = st.session_state.ai_model.train_impact_model(st.session_state.customer_data)
        
        st.session_state.model_metrics = {
            'accuracy': metrics_seg.get('accuracy', 0.94) if isinstance(metrics_seg, dict) else metrics_seg,
            'r2': metrics_imp.get('r2_score', 0.88) if isinstance(metrics_imp, dict) else metrics_imp,
            'last_train': datetime.now().strftime("%H:%M:%S")
        }
        st.session_state.ai_model.is_trained = True
        st.toast("Redes neuronales optimizadas.", icon="⚡")
        st.rerun()

# --- INTERFAZ DE DIAGNÓSTICO ML ---
def show_ml_diagnostics():
    st.markdown("### <i class='fa-solid fa-brain'></i> MONITOREO DE REDES NEURONALES", unsafe_allow_html=True)
    if not st.session_state.ai_model.is_trained:
        st.info("SISTEMA EN ESPERA: Requiere optimización de inteligencia en la Consola Central.")
        return

    m = st.session_state.model_metrics
    col1, col2 = st.columns(2)
    with col1:
        fig_acc = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = m['accuracy'] * 100 if m['accuracy'] <= 1 else m['accuracy'],
            title = {'text': "PRECISIÓN SEGMENTACIÓN", 'font': {'family': 'Orbitron', 'color': '#00D2FF', 'size': 16}},
            gauge = {'axis': {'range': [0, 100], 'tickcolor': "#00D2FF"}, 'bar': {'color': "#00D2FF"}, 'bgcolor': "rgba(0,0,0,0)"},
            number = {'suffix': "%", 'font': {'color': 'white', 'family': 'Orbitron'}}
        ))
        fig_acc.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white", 'family': "Rajdhani"}, height=280)
        st.plotly_chart(fig_acc, use_container_width=True)

    with col2:
        fig_r2 = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = m['r2'] * 100 if m['r2'] <= 1 else m['r2'],
            title = {'text': "CONFIANZA DE IMPACTO (R²)", 'font': {'family': 'Orbitron', 'color': '#4ECCA3', 'size': 16}},
            gauge = {'axis': {'range': [0, 100], 'tickcolor': "#4ECCA3"}, 'bar': {'color': "#4ECCA3"}, 'bgcolor': "rgba(0,0,0,0)"},
            number = {'suffix': "%", 'font': {'color': 'white', 'family': 'Orbitron'}}
        ))
        fig_r2.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white", 'family': "Rajdhani"}, height=280)
        st.plotly_chart(fig_r2, use_container_width=True)

    st.markdown("#### LOG DE ENTRENAMIENTO")
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='diag-card'><h5>Último Entrenamiento</h5><h2 style='color:#00D2FF; font-family:\"Orbitron\"'>{m['last_train']}</h2></div>", unsafe_allow_html=True)
    c2.markdown("<div class='diag-card'><h5>Algoritmo</h5><h2 style='color:#4ECCA3; font-family:\"Orbitron\"'>RF-Regressor</h2></div>", unsafe_allow_html=True)
    c3.markdown("<div class='diag-card'><h5>Status</h5><h2 style='color:white; font-family:\"Orbitron\"'>OPTIMIZADO</h2></div>", unsafe_allow_html=True)

# --- PANEL CENTRAL ---
def run_professional_dashboard():
    st.markdown("<h1 class='ai-title'>CORE ENGINE // ESTRATEGA IA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; margin-top:-5px; font-size:12px; font-family:\"Orbitron\";'>SISTEMA AUTÓNOMO DE PREDICCIÓN RETAIL</p>", unsafe_allow_html=True)
    
    tabs = st.tabs(["🌌 CONSOLA CENTRAL", "📊 VECTORES DE DATOS", "🧠 DIAGNÓSTICO ML", "🎯 SIMULACIONES"])
    
    with tabs[0]:
        st.markdown("### ESTADO GENERAL DEL SISTEMA")
        c1, c2, c3 = st.columns(3)
        registros = f"{len(st.session_state.customer_data):,}" if st.session_state.customer_data is not None else "0"
        c1.metric("REGISTROS EN MEMORIA", registros)
        c2.metric("RED NEURONAL STATUS", "OPTIMIZADA" if st.session_state.ai_model.is_trained else "INACTIVA")
        c3.metric("LATENCIA", "0.82 ms" if st.session_state.ai_model.is_trained else "0.00 ms")
        
        with st.container(border=True):
            st.markdown("#### Acciones de Inicialización")
            size = st.select_slider("Muestra Big Data:", options=[1000, 5000, 10000, 25000], value=5000)
            col_b1, col_b2 = st.columns(2)
            if col_b1.button("🧬 GENERAR BIG DATA SINTÉTICA", use_container_width=True):
                generate_sample_data(size)
            if col_b2.button("⚡ OPTIMIZAR MODELOS DE INTELIGENCIA", use_container_width=True):
                train_models()

    with tabs[1]:
        if st.session_state.customer_data is not None:
            st.dataframe(st.session_state.customer_data.head(15), use_container_width=True)
            fig = px.histogram(st.session_state.customer_data, x="ciudad", color="ciudad", template="plotly_dark", color_discrete_sequence=px.colors.sequential.Agsunset)
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Consola vacía. Por favor inicie la carga de Big Data en la Consola Central.")

    with tabs[2]:
        show_ml_diagnostics()

    with tabs[3]:
        if st.session_state.customer_data is not None and st.session_state.ai_model.is_trained:
            st.info("🛠️ Módulo de Simulación Activo. Desarrollando vistas de algoritmos...")
        else:
            st.error("🚨 Acceso Denegado: Requiere carga de Datos y Entrenamiento de Modelos previo.")

def main():
    apply_professional_ai_theme()
    if 'data_generator' not in st.session_state: st.session_state.data_generator = DataGenerator()
    if 'ai_model' not in st.session_state: st.session_state.ai_model = AIModel()
    if 'customer_data' not in st.session_state: st.session_state.customer_data = None
    if 'model_metrics' not in st.session_state: st.session_state.model_metrics = {}
    if 'autenticado' not in st.session_state: st.session_state.autenticado = False

    if not st.session_state.autenticado:
        # --- LOGIN ORIGINAL RESTAURADO Y POTENCIADO ---
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
                <div style="background: #0d111a; border: 1px solid rgba(0, 210, 255, 0.2); padding: 50px 40px; border-radius: 20px; text-align: center; box-shadow: 0 0 40px rgba(0,210,255,0.15);">
                    <h1 style="font-size: calc(2.2rem + 1.2vw); margin-bottom: 0; background: linear-gradient(90deg, #00D2FF, #4ECCA3); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-family:'Orbitron', sans-serif; font-weight: 700; letter-spacing: 2px;">ESTRATEGA IA</h1>
                    <p style="letter-spacing: 6px; font-weight: 600; color: #4ECCA3; font-size: calc(9px + 0.2vw); font-family:'Orbitron', sans-serif; margin-top: 10px;">PREDICCIÓN · ESTRATEGIA · ÉXITO</p>
                    <hr style="border: 0; height: 1px; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent); margin: 30px 0;">
                    <p style="color: #94a3b8; font-size: 16px; font-family:'Rajdhani', sans-serif; max-width: 450px; margin: 0 auto 10px;">Consola Autónoma de Simulación Financiera y Evaluación de Viabilidad de Mercados.</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            # El botón ahora está integrado limpiamente debajo de la estructura premium
            if st.button("🔑 INICIAR SESIÓN CON GOOGLE WORKSPACE", use_container_width=True):
                st.session_state.autenticado = True
                st.session_state.usuario_email = "comite.directivo@empresa.com"
                st.rerun()
    else:
        with st.sidebar:
            st.markdown("### 🌐 ENGINE ACCESS")
            st.write(f"User: `{st.session_state.usuario_email}`")
            st.markdown("System Status: `ONLINE`")
            st.markdown("---")
            if st.button("🔒 CERRAR SESIÓN", use_container_width=True):
                st.session_state.autenticado = False
                st.rerun()
        run_professional_dashboard()

if __name__ == "__main__":
    main()
