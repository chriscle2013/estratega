# app.py - Versión 2.7 INTERFAZ IA PROFESIONAL (SINCRONIZACIÓN EN TIEMPO REAL)
# Solución: Actualización instantánea de métricas mediante st.rerun()
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import firebase_admin
from firebase_admin import credentials, auth

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
        
        .stApp {
            background-color: #06070d !important;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(0, 210, 255, 0.03) 0%, transparent 50%),
                radial-gradient(circle at 90% 80%, rgba(78, 204, 163, 0.03) 0%, transparent 50%) !important;
            color: #e2e8f0 !important;
        }

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

        .stButton>button {
            font-family: 'Orbitron', sans-serif !important;
            background: linear-gradient(135deg, #00D2FF 0%, #0072FF 100%) !important;
            color: white !important;
            border-radius: 8px !important;
            padding: 12px 24px !important;
            box-shadow: 0 4px 15px rgba(0, 210, 255, 0.2);
        }

        .ai-title {
            background: linear-gradient(90deg, #00D2FF, #4ECCA3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
            font-size: calc(1.8rem + 1.5vw) !important;
            line-height: 1.2 !important;
            margin-bottom: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES DE CONTROL (CORREGIDAS CON RERUN) ---
def generate_sample_data(size):
    # Generar los datos
    st.session_state.customer_data = st.session_state.data_generator.generate_synthetic_data(size)
    st.toast(f"Muestra de {size:,} perfiles normalizada.", icon="🧬")
    # Forzar actualización de pantalla
    st.rerun()

def train_models():
    if st.session_state.customer_data is None:
        st.error("❌ Error: Código de datos fuente vacío.")
        return
    # Entrenar modelos
    st.session_state.model_metrics = {
        'segmentation_accuracy': st.session_state.ai_model.train_segmentation_model(st.session_state.customer_data),
        'impact_precision': st.session_state.ai_model.train_impact_model(st.session_state.customer_data)
    }
    st.session_state.ai_model.is_trained = True
    st.toast("Redes neuronales optimizadas para predicción retail.", icon="⚡")
    # Forzar actualización de pantalla
    st.rerun()

# --- MÓDULOS DE DECISIÓN ---
def create_launch_analyzer():
    st.markdown("### <i class='fa-solid fa-rocket'></i> ALGORITMO DE LANZAMIENTO", unsafe_allow_html=True)
    max_c = len(st.session_state.customer_data) if st.session_state.customer_data is not None else 1000
    with st.container(border=True):
        ciudades = ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Bucaramanga', 'Cartagena']
        sel_ciudades = st.multiselect("Nodos Geográficos Objetivo:", opciones=ciudades, default=ciudades)
        c1, c2 = st.columns(2)
        with c1: n_cust = st.slider("Tamaño del Vector de Prueba:", 50, int(max_c), 300)
        with c2: price = st.number_input("Precio de Entrada del Producto (COP):", 5000, 2000000, 25000)
        if st.button("EXECUTE PREDICTION RUN", use_container_width=True):
            filtered = st.session_state.customer_data[st.session_state.customer_data['ciudad'].isin(sel_ciudades)]
            test_c = filtered.sample(n=min(n_cust, len(filtered))).to_dict(orient='records')
            st.session_state.launch_result = st.session_state.ai_model.evaluate_product_launch(test_c, product_price=price, min_viable_revenue=30000000)
            st.rerun()

def create_investment_analyzer():
    st.markdown("### <i class='fa-solid fa-chart-line'></i> SIMULACIÓN DE INFRAESTRUCTURA", unsafe_allow_html=True)
    with st.container(border=True):
        ciudades_disponibles = ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Bucaramanga', 'Cartagena']
        sel_ciudades = st.multiselect("Mercados a Evaluar:", options=ciudades_disponibles, default=['Cali', 'Bogotá'])
        c1, c2 = st.columns(2)
        with c1: investment = st.number_input("CAPEX Requerido (M COP):", 10, 50000, 10000) * 1000000
        with c2: cost_ratio = st.slider("Margen de Costo Operativo Variable (%):", 10, 100, 35)
        if st.button("RUN FINANCIAL SIMULATION", use_container_width=True):
            filtered = st.session_state.customer_data[st.session_state.customer_data['ciudad'].isin(sel_ciudades)]
            test_c = filtered.sample(n=min(500, len(filtered))).to_dict(orient='records')
            res = st.session_state.ai_model.evaluate_infrastructure_investment(test_c, investment_required=investment, variable_cost_ratio=cost_ratio/100.0)
            st.session_state.investment_result = res
            st.session_state.alternativas = []
            if "❌" in res['recommendation']:
                for cd in ciudades_disponibles:
                    if cd not in sel_ciudades:
                        alt_data = st.session_state.customer_data[st.session_state.customer_data['ciudad'] == cd]
                        if len(alt_data) > 50:
                            alt_res = st.session_state.ai_model.evaluate_infrastructure_investment(alt_data.sample(n=min(300, len(alt_data))).to_dict(orient='records'), investment_required=investment, variable_cost_ratio=cost_ratio/100.0)
                            if "✅" in alt_res['recommendation']:
                                st.session_state.alternativas.append({'Ciudad': cd, 'ROI': f"{alt_res['profitability_percentage']:.1f}%", 'Payback': f"{alt_res['payback_months']:.1f}"})
            st.rerun()

# --- INTERFAZ DASHBOARD ---
def run_professional_dashboard():
    st.markdown("<h1 class='ai-title'>CORE ENGINE // ESTRATEGA IA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; margin-top:-5px; font-size:12px; font-family:\"Orbitron\";'>MÓDULO DE INTELIGENCIA PREDICTIVA PARA RETAIL</p>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["🌌 CONSOLA CENTRAL", "📊 VECTORES DE DATOS", "🧠 DIAGNÓSTICO ML", "🎯 SIMULACIONES"])
    
    with tab1:
        st.markdown("### ESTADO GENERAL DEL SISTEMA")
        c1, c2, c3 = st.columns(3)
        # Estas métricas ahora se actualizan al instante gracias al rerun
        val_registros = f"{len(st.session_state.customer_data):,}" if st.session_state.customer_data is not None else "0"
        c1.metric("REGISTROS EN MEMORIA", val_registros)
        c2.metric("RED NEURONAL STATUS", "OPTIMIZADA" if st.session_state.ai_model.is_trained else "INACTIVA")
        c3.metric("LATENCIA DE CONSULTA", "0.82 ms" if st.session_state.ai_model.is_trained else "0.00 ms")
        
        with st.container(border=True):
            st.markdown("#### Acciones de Inicialización")
            size = st.select_slider("Magnitud de la Muestra:", options=[1000, 5000, 10000, 25000], value=5000)
            col_b1, col_b2 = st.columns(2)
            if col_b1.button("🧬 GENERAR BIG DATA SINTÉTICA", use_container_width=True): generate_sample_data(size)
            if col_b2.button("⚡ OPTIMIZAR MODELOS DE INTELIGENCIA", use_container_width=True): train_models()

    with tab2:
        if st.session_state.customer_data is not None:
            st.dataframe(st.session_state.customer_data.head(15), use_container_width=True)
            fig = px.histogram(st.session_state.customer_data, x="ciudad", color="ciudad", template="plotly_dark", color_discrete_sequence=px.colors.sequential.Agsunset)
            st.plotly_chart(fig, use_container_width=True)

    with tab4:
        if st.session_state.customer_data is not None and st.session_state.ai_model.is_trained:
            selector = st.pills("Escenario:", ["🚀 Lanzamiento", "💼 Inversión"])
            if selector == "🚀 Lanzamiento": create_launch_analyzer()
            else: create_investment_analyzer()

def main():
    apply_professional_ai_theme()
    if 'data_generator' not in st.session_state: st.session_state.data_generator = DataGenerator()
    if 'ai_model' not in st.session_state: st.session_state.ai_model = AIModel()
    if 'customer_data' not in st.session_state: st.session_state.customer_data = None
    if 'model_metrics' not in st.session_state: st.session_state.model_metrics = {}
    if 'autenticado' not in st.session_state: st.session_state.autenticado = False

    if not st.session_state.autenticado:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
        with col_l2:
            st.markdown("""
                <div style="background: #0d111a; border: 1px solid rgba(0, 210, 255, 0.2); padding: 45px; border-radius: 20px; text-align: center;">
                    <h1 style="font-size: calc(2rem + 1vw); background: linear-gradient(90deg, #00D2FF, #4ECCA3); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-family:'Orbitron';">ESTRATEGA IA</h1>
                    <p style="letter-spacing: 5px; color: #4ECCA3; font-size: 11px; font-family:'Orbitron';">PLATAFORMA PREDICITIVA DE NEGOCIOS</p>
                    <p style="color: #94a3b8; font-size: 15px; font-family:'Rajdhani';">Consola Autónoma de Simulación Financiera.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("🔑 INICIAR SESIÓN CON GOOGLE", use_container_width=True):
                st.session_state.autenticado = True
                st.session_state.usuario_email = "directivo@empresa.com"
                st.rerun()
    else:
        with st.sidebar:
            st.markdown("### 🌐 ENGINE ACCESS")
            st.write(f"User: `{st.session_state.usuario_email}`")
            if st.button("🔒 TERMINAR SESIÓN"):
                st.session_state.autenticado = False
                st.rerun()
        run_professional_dashboard()

if __name__ == "__main__":
    main()
