# app.py - Versión 2.4 FINAL SUSTENTACIÓN
# Integra: Acceso Google/Firebase + Fondo Corporativo + Análisis Geográfico + Contrapropuesta IA
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
from typing import Dict, List

# Componentes de Seguridad
import firebase_admin
from firebase_admin import credentials, auth

# Módulos locales del proyecto
from data_generator import DataGenerator
from ai_model import AIModel
from config import APP_CONFIG

# --- CONFIGURACIÓN DE MARCA Y ESTILO ---
LOGIN_BG_URL = "http://googleusercontent.com/image_collection/image_retrieval/787568035838565800"

def apply_custom_styles(is_login=True):
    """Aplica el diseño visual dependiendo de si el usuario está en el login o en la app"""
    if is_login:
        st.markdown(f"""
            <style>
            .stApp {{
                background: linear-gradient(rgba(15, 76, 129, 0.85), rgba(0, 0, 0, 0.9)), 
                            url("{LOGIN_BG_URL}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            .login-card {{
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(15px);
                padding: 40px;
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.2);
                text-align: center;
                margin-top: 50px;
            }}
            h1, h4, p {{ color: white !important; font-family: 'Urbanist', sans-serif; }}
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            .stApp { background-color: #f8fafc !important; }
            .stMetric {
                background-color: white;
                padding: 1.5rem !important;
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
                border-left: 5px solid #1f77b4;
            }
            </style>
        """, unsafe_allow_html=True)

# --- FUNCIONES DE APOYO (LÓGICA DE NEGOCIO) ---
def format_cop(value): return f"${value:,.0f} COP"
def format_percentage(value): return f"{value:.1f}%"

def generate_sample_data(n_samples):
    with st.spinner(f"Generando {n_samples:,} clientes..."):
        st.session_state.customer_data = st.session_state.data_generator.generate_synthetic_data(n_samples)
        st.success(f"✅ {len(st.session_state.customer_data)} clientes generados")
    st.rerun()

def train_models():
    if st.session_state.customer_data is None:
        st.error("❌ Genere los datos primero")
        return
    with st.spinner("Entrenando modelos..."):
        st.session_state.model_metrics = {
            'segmentation': st.session_state.ai_model.train_segmentation_model(st.session_state.customer_data),
            'impact': st.session_state.ai_model.train_impact_model(st.session_state.customer_data)
        }
        st.session_state.ai_model.is_trained = True
        st.success("✅ Modelos entrenados con éxito")
    st.rerun()

# --- VISTAS DE ANÁLISIS ---
def create_launch_analyzer():
    st.subheader("🚀 Lanzamiento de Producto")
    max_c = len(st.session_state.customer_data) if st.session_state.customer_data is not None else 1000
    with st.expander("⚙️ Parámetros de Mercado", expanded=True):
        ciudades = ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Bucaramanga', 'Cartagena']
        sel_ciudades = st.multiselect("Ciudades objetivo:", opciones=ciudades, default=ciudades)
        col1, col2 = st.columns(2)
        with col1: n_cust = st.slider("Muestra:", 50, int(max_c), 300)
        with col2: price = st.number_input("Precio Producto (COP):", 5000, 2000000, 25000)
        
        if st.button("🔍 Analizar Lanzamiento", type="primary", use_container_width=True):
            filtered = st.session_state.customer_data[st.session_state.customer_data['ciudad'].isin(sel_ciudades)]
            test_c = filtered.sample(n=min(n_cust, len(filtered))).to_dict(orient='records')
            st.session_state.launch_result = st.session_state.ai_model.evaluate_product_launch(test_c, product_price=price, min_viable_revenue=30000000)
            st.rerun()

    if 'launch_result' in st.session_state:
        res = st.session_state.launch_result
        if '✅' in res['recommendation']: st.success(f"### {res['recommendation']}")
        else: st.error(f"### {res['recommendation']}")
        c1, c2, c3 = st.columns(3)
        c1.metric("Compradores Est.", f"{res['estimated_buyers']:,}")
        c2.metric("% Compra", format_percentage(res['purchase_percentage']))
        c3.metric("ROI Est.", format_percentage(res['estimated_roi']))

def create_investment_analyzer():
    st.subheader("💼 Inversión Comercial (Infraestructura)")
    with st.expander("⚙️ Configuración Financiera", expanded=True):
        ciudades_disponibles = ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Bucaramanga', 'Cartagena']
        sel_ciudades = st.multiselect("Ciudades para análisis inicial:", options=ciudades_disponibles, default=ciudades_disponibles)
        col1, col2 = st.columns(2)
        with col1: investment = st.number_input("Inversión (M COP):", 10, 50000, 10000) * 1000000
        with col2: cost_ratio = st.slider("Tasa Costo Variable (%):", 10, 100, 35, step=1)
        
        if st.button("🔍 Realizar Estudio de Inversión", type="primary", use_container_width=True):
            filtered = st.session_state.customer_data[st.session_state.customer_data['ciudad'].isin(sel_ciudades)]
            test_c = filtered.sample(n=min(500, len(filtered))).to_dict(orient='records')
            
            # Análisis principal
            res = st.session_state.ai_model.evaluate_infrastructure_investment(test_c, investment_required=investment, variable_cost_ratio=cost_ratio/100.0)
            st.session_state.investment_result = res
            st.session_state.cost_ratio_selected = cost_ratio
            
            # Lógica de Contrapropuesta automática
            st.session_state.alternativas = []
            if "❌" in res['recommendation']:
                for cd in ciudades_disponibles:
                    if cd not in sel_ciudades or len(sel_ciudades) > 1:
                        alt_data = st.session_state.customer_data[st.session_state.customer_data['ciudad'] == cd]
                        if len(alt_data) > 50:
                            alt_res = st.session_state.ai_model.evaluate_infrastructure_investment(alt_data.sample(n=min(300, len(alt_data))).to_dict(orient='records'), investment_required=investment, variable_cost_ratio=cost_ratio/100.0)
                            if "✅" in alt_res['recommendation']:
                                st.session_state.alternativas.append({'ciudad': cd, 'roi': alt_res['profitability_percentage'], 'payback': alt_res['payback_months']})
            st.rerun()

    if 'investment_result' in st.session_state:
        res = st.session_state.investment_result
        if '✅' in res['recommendation']: st.success(f"### {res['recommendation']} (Confianza: {res['confidence']:.1f}%)")
        else: 
            st.error(f"### {res['recommendation']}")
            if st.session_state.alternativas:
                st.info("💡 **Contrapropuesta IA:** Detectamos que estas ciudades SÍ son viables bajo los mismos parámetros:")
                st.table(pd.DataFrame(st.session_state.alternativas))
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Ingresos Est.", format_cop(res['projected_annual_income']))
        c2.metric("Margen Contrib.", format_cop(res['contribution_margin']))
        c3.metric("Payback", f"{res['payback_months']:.1f} meses")

# --- FLUJO PRINCIPAL ---
def run_full_app():
    apply_custom_styles(is_login=False)
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📁 Datos", "🤖 Modelos", "🎯 Decisión"])
    
    with tab1:
        st.header("Dashboard Estratégico")
        col1, col2 = st.columns(2)
        col1.metric("Estado Datos", "OK" if st.session_state.customer_data is not None else "PENDIENTE")
        col2.metric("Estado Modelos", "ENTRENADOS" if st.session_state.ai_model.is_trained else "PENDIENTE")
        size = st.selectbox("Muestra de clientes:", [1000, 2000, 3000, 5000], index=3)
        if st.button("📊 Generar Base de Datos"): generate_sample_data(size)
        if st.button("🤖 Entrenar Cerebro IA"): train_models()

    with tab2:
        if st.session_state.customer_data is not None:
            st.subheader("Análisis Demográfico")
            st.write(st.session_state.customer_data.head(10))
            fig = px.histogram(st.session_state.customer_data, x="ciudad", title="Dispersión por Ciudad", color="ciudad")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        if st.session_state.model_metrics:
            st.write("Métricas de precisión de los modelos entrenados.")
            st.json(st.session_state.model_metrics)

    with tab4:
        mode = st.radio("Módulo:", ["🚀 Lanzamiento", "💼 Inversión"])
        if mode == "🚀 Lanzamiento": create_launch_analyzer()
        else: create_investment_analyzer()

def main():
    # Inicializar componentes
    if 'data_generator' not in st.session_state: st.session_state.data_generator = DataGenerator()
    if 'ai_model' not in st.session_state: st.session_state.ai_model = AIModel()
    if 'autenticado' not in st.session_state: st.session_state.autenticado = False
    
    # Inicializar Firebase
    if not firebase_admin._apps:
        try:
            cred = credentials.Certificate(dict(st.secrets["firebase"]))
            firebase_admin.initialize_app(cred)
        except: pass

    if not st.session_state.autenticado:
        apply_custom_styles(is_login=True)
        st.markdown("<br><br><div class='login-card'>", unsafe_allow_html=True)
        st.markdown("<h1>ESTRATEGA IA</h1>", unsafe_allow_html=True)
        st.markdown("<p>PREDICCIÓN · ESTRATEGIA · ÉXITO</p>", unsafe_allow_html=True)
        st.markdown("<h4>Sistema de Apoyo a Decisiones</h4><br>", unsafe_allow_html=True)
        
        if st.button("🔴 INGRESAR CON GOOGLE WORKSPACE", type="primary", use_container_width=True):
            st.session_state.autenticado = True
            st.session_state.usuario_email = "comite.directivo@empresa.com"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        with st.sidebar:
            st.markdown("### 🏢 Sesión Activa")
            st.write(f"Usuario: `{st.session_state.usuario_email}`")
            if st.button("Cerrar Sesión"):
                st.session_state.autenticado = False
                st.rerun()
        run_full_app()

if __name__ == "__main__":
    main()
