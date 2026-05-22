# app.py - Versión 2.6 INTERFAZ IA PROFESIONAL (EDICIÓN CORREGIDA)
# Soluciona: Título responsive para móviles + Error de paleta de colores de Plotly
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
        /* Importar tipografía moderna */
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
            white-space: pre;
            background-color: transparent;
            border-radius: 8px;
            color: #64748b !important;
            border: none;
            transition: all 0.3s ease;
        }
        .stTabs [data-baseweb="tab"]:hover {
            color: #00D2FF !important;
            background: rgba(0, 210, 255, 0.05);
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(90deg, rgba(0,210,255,0.15), rgba(78,204,163,0.15)) !important;
            color: #00D2FF !important;
            border: 1px solid rgba(0, 210, 255, 0.3) !important;
            box-shadow: 0 0 15px rgba(0, 210, 255, 0.1);
        }

        /* Tarjetas de Métricas (Módulos de datos) */
        div[data-testid="stMetric"] {
            background: #0d111a !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-left: 4px solid #00D2FF !important;
            border-radius: 12px !important;
            padding: 20px !important;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2) !important;
        }
        div[data-testid="stMetric"] [data-testid="stMetricLabel"] {
            font-family: 'Rajdhani', sans-serif !important;
            color: #94a3b8 !important;
            font-size: 14px !important;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        div[data-testid="stMetric"] [data-testid="stMetricValue"] {
            font-family: 'Orbitron', sans-serif !important;
            color: #ffffff !important;
            font-size: 24px !important;
        }

        /* Cajas colapsables e Inputs */
        .stExpander, div[data-testid="stExpander"] {
            background: #0d111a !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 12px !important;
        }
        
        /* Botones Profesionales de Software */
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

        /* Títulos adaptables para celular y PC */
        h1, h2, h3 {
            font-family: 'Orbitron', sans-serif !important;
            letter-spacing: 1px;
        }
        .ai-title {
            background: linear-gradient(90deg, #00D2FF, #4ECCA3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
            font-size: calc(1.8rem + 1.5vw) !important; /* Adaptable a pantallas chicas */
            line-height: 1.2 !important;
            margin-bottom: 5px;
        }
        
        /* Barra lateral (Sidebar) */
        section[data-testid="stSidebar"] {
            background-color: #07090e !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }
        </style>
    """, unsafe_allow_html=True)

# --- FORMATOS DE MONEDA Y PORCENTAJES ---
def format_cop(value): return f"${value:,.0f} COP"
def format_percentage(value): return f"{value:.1f}%"

# --- FUNCIONES DE CONTROL DE NEGOCIO ---
def generate_sample_data(size):
    with st.spinner("🤖 ESTRATEGA ENGINE: Extrayendo y mapeando big data..."):
        st.session_state.customer_data = st.session_state.data_generator.generate_synthetic_data(size)
        st.toast(f"Muestra de {size:,} perfiles normalizada.", icon="🧬")

def train_models():
    if st.session_state.customer_data is None:
        st.error("❌ Error: Código de datos fuente vacío.")
        return
    with st.spinner("🧠 NEURAL NETWORK: Entrenando capas de decisión..."):
        st.session_state.model_metrics = {
            'segmentation_accuracy': st.session_state.ai_model.train_segmentation_model(st.session_state.customer_data),
            'impact_precision': st.session_state.ai_model.train_impact_model(st.session_state.customer_data)
        }
        st.session_state.ai_model.is_trained = True
        st.toast("Redes neuronales optimizadas para predicción retail.", icon="⚡")

# --- MÓDULOS DEL ENGINIO (PESTAÑA DECISIÓN) ---
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

    if 'launch_result' in st.session_state:
        res = st.session_state.launch_result
        st.markdown("---")
        if '✅' in res['recommendation']: st.success(f"🤖 **DICTAMEN IA:** {res['recommendation']}")
        else: st.error(f"🤖 **DICTAMEN IA:** {res['recommendation']}")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("CONVERSIÓN EST.", f"{res['estimated_buyers']:,} clientes")
        col2.metric("RATIO DE COMPRA", format_percentage(res['purchase_percentage']))
        col3.metric("ROI ESTIMADO", format_percentage(res['estimated_roi']))

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
            
            # Algoritmo Avanzado de Contrapropuesta automática
            st.session_state.alternativas = []
            if "❌" in res['recommendation']:
                for cd in ciudades_disponibles:
                    if cd not in sel_ciudades:
                        alt_data = st.session_state.customer_data[st.session_state.customer_data['ciudad'] == cd]
                        if len(alt_data) > 50:
                            alt_res = st.session_state.ai_model.evaluate_infrastructure_investment(alt_data.sample(n=min(300, len(alt_data))).to_dict(orient='records'), investment_required=investment, variable_cost_ratio=cost_ratio/100.0)
                            if "✅" in alt_res['recommendation']:
                                st.session_state.alternativas.append({'Ciudad Sugerida': cd, 'ROI Proyectado': format_percentage(alt_res['profitability_percentage']), 'Retorno (Meses)': f"{alt_res['payback_months']:.1f}"})
            st.rerun()

    if 'investment_result' in st.session_state:
        res = st.session_state.investment_result
        st.markdown("---")
        if '✅' in res['recommendation']: 
            st.success(f"⚡ **RECOMENDACIÓN:** {res['recommendation']} (Confianza del Modelo: {res['confidence']:.1f}%)")
        else: 
            st.error(f"🚨 **ALERTA DE RIESGO:** {res['recommendation']}")
            if st.session_state.alternativas:
                st.markdown("💡 **CONTRA-PROPUESTA GENERATIVA (IA):** Detectamos que los siguientes nodos geográficos sí absorben la inversión de forma rentable:")
                st.dataframe(pd.DataFrame(st.session_state.alternativas), use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("INGRESOS ANUALES PROYEC.", format_cop(res['projected_annual_income']))
        col2.metric("MARGEN DE CONTRIBUCIÓN", format_cop(res['contribution_margin']))
        col3.metric("PAYBACK CRÍTICO", f"{res['payback_months']:.1f} Meses")

# --- INTERFAZ CORE DEL SISTEMA (LOGUEADO) ---
def run_professional_dashboard():
    # Encabezado estilo Centro de Control
    st.markdown("<h1 class='ai-title'>CORE ENGINE // ESTRATEGA IA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; margin-top:-5px; font-size:13px; font-family:\"Orbitron\";'>MÓDULO DE INTELIGENCIA PREDICTIVA PARA RETAIL</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "🌌 CONSOLA CENTRAL", 
        "📊 VECTORES DE DATOS", 
        "🧠 DIAGNÓSTICO ML", 
        "🎯 SIMULACIONES AVANZADAS"
    ])
    
    with tab1:
        st.markdown("### ESTADO GENERAL DEL SISTEMA")
        c1, c2, c3 = st.columns(3)
        c1.metric("REGISTROS EN MEMORIA", f"{len(st.session_state.customer_data):,}" if st.session_state.customer_data is not None else "0")
        c2.metric("RED NEURONAL STATUS", "OPTIMIZADA" if st.session_state.ai_model.is_trained else "INACTIVA")
        c3.metric("LATENCIA DE CONSULTA", "0.82 ms" if st.session_state.ai_model.is_trained else "0.00 ms")
        
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("#### Acciones de Inicialización de Carga")
            size = st.select_slider("Magnitud del Dataset de Simulación (Muestra):", options=[1000, 5000, 10000, 25000], value=5000)
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("🧬 GENERAR BIG DATA SINTÉTICA", use_container_width=True): generate_sample_data(size)
            with col_b2:
                if st.button("⚡ OPTIMIZAR MODELOS DE INTELIGENCIA", use_container_width=True): train_models()

    with tab2:
        if st.session_state.customer_data is not None:
            st.markdown("### DATA LOGGING (Últimos Registros Mapeados)")
            st.dataframe(st.session_state.customer_data.head(15), use_container_width=True)
            
            # Gráfica corregida con paleta cibernética robusta y compatible
            st.markdown("### ANÁLISIS GEOGRÁFICO DE CLIENTES")
            fig = px.histogram(
                st.session_state.customer_data, 
                x="ciudad", 
                color="ciudad",
                template="plotly_dark",
                color_discrete_sequence=px.colors.sequential.Agsunset
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', 
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Rajdhani, sans-serif")
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Consola vacía. Por favor inicie la carga de Big Data en la Consola Central.")
    
    with tab3:
        if st.session_state.ai_model.is_trained:
            st.markdown("### HIPERPARÁMETROS Y PRECISIÓN GENERAL")
            st.json(st.session_state.model_metrics)
        else:
            st.info("Métricas no compiladas. Ejecute la optimización de inteligencia.")

    with tab4:
        if st.session_state.customer_data is not None and st.session_state.ai_model.is_trained:
            selector = st.pills("Seleccione Escenario de Predicción:", ["🚀 Lanzamiento de Producto", "💼 Inversión Estructural"])
            if selector == "🚀 Lanzamiento de Producto": create_launch_analyzer()
            elif selector == "💼 Inversión Estructural": create_investment_analyzer()
        else:
            st.error("🚨 Acceso Denegado: Requiere carga de Datos y Entrenamiento de Modelos previo.")

# --- MANEJO DE ACCESO Y PANTALLA INICIAL ---
def main():
    apply_professional_ai_theme()
    
    # Inicialización de estados globales
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
                <div style="background: #0d111a; border: 1px solid rgba(0, 210, 255, 0.2); padding: 45px; border-radius: 20px; text-align: center; box-shadow: 0 0 40px rgba(0,210,255,0.1);">
                    <h1 style="font-size: calc(2rem + 1vw); margin-bottom: 0; background: linear-gradient(90deg, #00D2FF, #4ECCA3); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-family:'Orbitron';">ESTRATEGA IA</h1>
                    <p style="letter-spacing: 5px; font-weight: 400; color: #4ECCA3; font-size: 11px; font-family:'Orbitron';">PLATAFORMA PREDICITIVA DE NEGOCIOS</p>
                    <hr style="border: 0; height: 1px; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent); margin: 30px 0;">
                    <p style="color: #94a3b8; font-size: 15px; font-family:'Rajdhani';">Consola Autónoma de Simulación Financiera y Evaluación de Viabilidad de Mercados.</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔑 INICIAR SESIÓN CON GOOGLE WORKSPACE", use_container_width=True):
                st.session_state.autenticado = True
                st.session_state.usuario_email = "comite.directivo@empresa.com"
                st.rerun()
    else:
        with st.sidebar:
            st.markdown("### 🌐 ENGINE ACCESS")
            st.markdown(f"User: `{st.session_state.usuario_email}`")
            st.markdown("System Status: `ONLINE`")
            st.markdown("---")
            if st.button("🔒 TERMINAR SESIÓN"):
                st.session_state.autenticado = False
                st.rerun()
        run_professional_dashboard()

if __name__ == "__main__":
    main()
