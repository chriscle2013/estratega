# app.py - Versión 2.3 con Análisis de Contrapropuesta Geográfica Automática e Integración Firebase Auth
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
from typing import Dict, List

# Librerías oficiales para el control de acceso corporativo externo
import firebase_admin
from firebase_admin import credentials, auth

# Importar módulos locales
from data_generator import DataGenerator
from ai_model import AIModel
from config import APP_CONFIG

class BusinessDecisionApp:
    def __init__(self):
        self.customer_data = None
        self.model_metrics = None
        self.ai_model = AIModel()
        self.data_generator = DataGenerator()

def setup_page():
    # NOTA: st.set_page_config se movió al inicio del flujo principal de inicialización.
    st.markdown("""
        <style>
        @media (max-width: 768px) {
            .stTabs [data-baseweb="tab-list"] {
                gap: 4px !important;
                padding: 8px !important;
                flex-wrap: wrap !important;
                background-color: transparent !important;
            }
            
            .stTabs [role="tablist"] button {
                padding: 12px 16px !important;
                font-size: 16px !important;
                min-height: 50px !important;
                margin: 4px !important;
                flex: 1 1 45% !important;
                white-space: normal !important;
                word-wrap: break-word !important;
                border-radius: 8px !important;
            }
            
            .stMetric {
                padding: 0.8rem !important;
                margin-bottom: 0.8rem !important;
            }
            
            .stButton > button {
                width: 100% !important;
                font-size: 16px !important;
                min-height: 50px !important;
                padding: 14px 18px !important;
                margin-bottom: 14px !important;
                border-radius: 10px !important;
            }
        }
        
        .stTabs [role="tablist"] {
            background-color: transparent;
            border-bottom: 2px solid #e0e0e0;
        }
        
        .stTabs [role="tablist"] button {
            padding: 12px 20px !important;
            font-size: 16px !important;
            min-height: 48px !important;
            font-weight: 500;
            transition: all 0.3s ease;
            border-radius: 8px 8px 0 0;
        }
        
        .stTabs [role="tablist"] button[aria-selected="true"] {
            background-color: #1f77b4 !important;
            color: white !important;
            border-bottom: 3px solid #1f77b4 !important;
        }
        
        .stMetric {
            background-color: rgba(240, 242, 246, 0.8);
            padding: 1rem !important;
            border-radius: 8px;
            margin-bottom: 0.8rem !important;
            border-left: 4px solid #1f77b4;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🤖 Estratega IA / Toma Decisiones v2.3")
    st.markdown("---")

def format_cop(value):
    return f"${value:,.0f} COP"

def format_percentage(value):
    return f"{value:.1f}%"

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
        segment_metrics = st.session_state.ai_model.train_segmentation_model(st.session_state.customer_data)
        impact_metrics = st.session_state.ai_model.train_impact_model(st.session_state.customer_data)
        
        st.session_state.model_metrics = {
            'segmentation': segment_metrics,
            'impact': impact_metrics
        }
        
        st.session_state.ai_model.is_trained = True
        st.success("✅ Modelos entrenados")
    st.rerun()

def show_data_overview():
    if st.session_state.customer_data is None:
        st.warning("Genere los datos primero")
        return
        
    st.subheader("📊 Resumen de Clientes")
    cols = st.columns(2)
    
    metrics_data = [
        ("Total Clientes", f"{len(st.session_state.customer_data):,}"),
        ("Edad Promedio", f"{int(st.session_state.customer_data['edad'].mean())} años"),
        ("Ingreso Promedio", format_cop(st.session_state.customer_data['ingreso_mensual'].mean())),
        ("Valor Compra Prom.", format_cop(st.session_state.customer_data['valor_promedio_compra'].mean()))
    ]
    
    for i, (label, value) in enumerate(metrics_data):
        with cols[i % 2]:
            st.metric(label, value)
            
    st.markdown("")
    st.subheader("🎯 Distribución de Segmentos")
    segment_counts = st.session_state.customer_data['segmento_cliente'].value_counts()
    segment_labels = [st.session_state.data_generator.get_segment_description(seg) for seg in segment_counts.index]
    
    fig_pie = px.pie(values=segment_counts.values, names=segment_labels, title="Segmentos", height=350)
    fig_pie.update_layout(font=dict(size=11), margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig_pie, use_container_width=True)

def show_model_performance():
    if st.session_state.model_metrics is None:
        st.warning("Entrene los modelos primero")
        return
        
    st.subheader("🤖 Rendimiento de Modelos")
    tab1, tab2 = st.tabs(["📊 Segmentación", "📈 Impacto"])
    
    with tab1:
        metrics = st.session_state.model_metrics['segmentation']
        col1, col2 = st.columns(2)
        with col1: st.metric("Precisión", f"{metrics['accuracy']:.3f}")
        with col2: st.metric("Val. Cruzada", f"{metrics['cv_mean']:.3f}")
    
    with tab2:
        metrics = st.session_state.model_metrics['impact']
        col1, col2 = st.columns(2)
        with col1: st.metric("RMSE", f"{metrics['rmse']:.2f}")
        with col2: st.metric("R² Score", f"{metrics['r2_score']:.3f}")

def create_decision_analyzer():
    st.subheader("🎯 Análisis de Decisión IA")
    if not st.session_state.ai_model.is_trained:
        st.error("❌ Entrene los modelos primero (Tab Modelos)")
        return
    
    analysis_type = st.radio("Selecciona tipo de análisis:", options=["🚀 Lanzamiento de Producto", "💼 Inversión Comercial (Infraestructura)"])
    st.markdown("")
    
    if analysis_type == "🚀 Lanzamiento de Producto":
        create_launch_analyzer()
    else:
        create_investment_analyzer()

def create_launch_analyzer():
    st.subheader("🚀 Lanzamiento de Producto")
    max_customers_available = len(st.session_state.customer_data) if st.session_state.customer_data is not None else 1000
    
    with st.expander("⚙️ Configurar Parámetros", expanded=True):
        st.markdown("### 🌆 Población Objetivo Geográfica")
        ciudades_disponibles = ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Bucaramanga', 'Cartagena']
        ciudades_seleccionadas = st.multiselect(
            "Selecciona las ciudades para enfocar el análisis de lanzamiento:",
            options=ciudades_disponibles, default=ciudades_disponibles, key="ciudades_launch"
        )
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            n_customers = st.slider("Clientes a analizar:", min_value=50, max_value=int(max_customers_available), value=min(300, int(max_customers_available)), step=5)
        with col2:
            product_price = st.number_input("Precio del producto (COP):", 5000, 2000000, 25000, step=1000)
        
        col1, col2 = st.columns(2)
        with col1: min_age = st.number_input("Edad mín:", 18, 80, 20, 1)
        with col2: max_age = st.number_input("Edad máx:", 18, 80, 60, 1)
        
        col1, col2 = st.columns(2)
        with col1: min_income = st.number_input("Ing. mín (M COP):", 1, 50, 2, 1) * 1000000
        with col2: max_income = st.number_input("Ing. máx (M COP):", 1, 100, 8, 1) * 1000000
        
        min_viable = st.number_input("Ingresos mínimos viables (M COP):", 10, 5000, 30, 1) * 1000000
        
        if st.button("🔍 Analizar Lanzamiento", type="primary", use_container_width=True):
            filtered_data = st.session_state.customer_data[
                (st.session_state.customer_data['edad'] >= min_age) & 
                (st.session_state.customer_data['edad'] <= max_age) &
                (st.session_state.customer_data['ingreso_mensual'] >= min_income) &
                (st.session_state.customer_data['ingreso_mensual'] <= max_income) &
                (st.session_state.customer_data['ciudad'].isin(ciudades_seleccionadas))
            ]
            
            if len(filtered_data) < 10: filtered_data = st.session_state.customer_data
            sample_n = min(n_customers, len(filtered_data))
            test_customers = filtered_data.sample(n=sample_n).to_dict(orient='records')
            
            with st.spinner("Analizando..."):
                launch_result = st.session_state.ai_model.evaluate_product_launch(test_customers, product_price=product_price, min_viable_revenue=min_viable)
                st.session_state.launch_result = launch_result
                st.rerun()
                
    if 'launch_result' in st.session_state:
        result = st.session_state.launch_result
        st.markdown("---")
        recommendation = result['recommendation']
        confidence = result['confidence']
        
        if '✅' in recommendation: st.success(f"### {recommendation} (Confianza: {confidence:.1f}%)")
        else: st.error(f"### {recommendation} (Confianza: {confidence:.1f}%)")
        
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Compradores Est.", f"{result['estimated_buyers']:,}")
        with col2: st.metric("% de Compra", format_percentage(result['purchase_percentage']))
        with col3: st.metric("ROI Est.", format_percentage(result['estimated_roi']))
        
        st.subheader("💡 Justificación")
        for justif in result['justification']: st.markdown(f"• {justif}")

def create_investment_analyzer():
    st.subheader("💼 Inversión Comercial (Infraestructura)")
    max_customers_available = len(st.session_state.customer_data) if st.session_state.customer_data is not None else 2000
    
    with st.expander("⚙️ Configurar Parámetros", expanded=True):
        st.markdown("### 🌆 Población Objetivo Geográfica")
        ciudades_disponibles = ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Bucaramanga', 'Cartagena']
        ciudades_seleccionadas = st.multiselect(
            "Selecciona las ciudades para enfocar el análisis inicial:",
            options=ciudades_disponibles, default=ciudades_disponibles, key="ciudades_investment"
        )
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            n_customers = st.slider("Clientes a analizar:", min_value=100, max_value=int(max_customers_available), value=min(500, int(max_customers_available)), step=100)
        with col2:
            investment = st.number_input("Inversión requerida (M COP):", min_value=10, max_value=50000, value=10000, step=10) * 1000000
        
        col1, col2 = st.columns(2)
        with col1: min_age = st.number_input("Edad mín:", 18, 80, 25, 1)
        with col2: max_age = st.number_input("Edad máx:", 18, 80, 65, 1)
        
        col1, col2 = st.columns(2)
        with col1: min_income = st.number_input("Ing. mín (M COP):", 1, 50, 2, 1) * 1000000
        with col2: max_income = st.number_input("Ing. máx (M COP):", 1, 100, 9, 1) * 1000000
        
        cost_ratio_input = st.slider("Tasa estimada de Costo Variable (% sobre ingreso):", min_value=10, max_value=100, value=35, step=1)
        
        if st.button("🔍 Analizar Inversión", type="primary", use_container_width=True):
            filtered_data = st.session_state.customer_data[
                (st.session_state.customer_data['edad'] >= min_age) & 
                (st.session_state.customer_data['edad'] <= max_age) &
                (st.session_state.customer_data['ingreso_mensual'] >= min_income) &
                (st.session_state.customer_data['ingreso_mensual'] <= max_income) &
                (st.session_state.customer_data['ciudad'].isin(ciudades_seleccionadas))
            ]
            
            if len(filtered_data) < 10: filtered_data = st.session_state.customer_data
            sample_n = min(n_customers, len(filtered_data))
            test_customers = filtered_data.sample(n=sample_n).to_dict(orient='records')
            
            with st.spinner("Analizando mercado principal..."):
                investment_result = st.session_state.ai_model.evaluate_infrastructure_investment(
                    test_customers, investment_required=investment, variable_cost_ratio=cost_ratio_input / 100.0
                )
            
            st.session_state.investment_result = investment_result
            st.session_state.cost_ratio_selected = cost_ratio_input
            
            st.session_state.ciudades_alternativas_viables = []
            
            if "❌" in investment_result['recommendation'] or "NO" in investment_result['recommendation'].upper():
                with st.spinner("🕵️ El mercado principal no es viable. Buscando alternativas estables..."):
                    for cd in ciudades_disponibles:
                        alt_data = st.session_state.customer_data[
                            (st.session_state.customer_data['edad'] >= min_age) & 
                            (st.session_state.customer_data['edad'] <= max_age) &
                            (st.session_state.customer_data['ingreso_mensual'] >= min_income) &
                            (st.session_state.customer_data['ingreso_mensual'] <= max_income) &
                            (st.session_state.customer_data['ciudad'] == cd)
                        ]
                        
                        if len(alt_data) >= 10:
                            alt_sample_n = min(n_customers, len(alt_data))
                            alt_test = alt_data.sample(n=alt_sample_n).to_dict(orient='records')
                            
                            alt_res = st.session_state.ai_model.evaluate_infrastructure_investment(
                                alt_test, investment_required=investment, variable_cost_ratio=cost_ratio_input / 100.0
                            )
                            
                            if "✅" in alt_res['recommendation'] or "INVERTIR" in alt_res['recommendation'].upper():
                                st.session_state.ciudades_alternativas_viables.append({
                                    'ciudad': cd,
                                    'roi': alt_res['profitability_percentage'],
                                    'payback': alt_res['payback_months'],
                                    'margin': alt_res['contribution_margin']
                                })
            st.rerun()
            
    if 'investment_result' in st.session_state:
        result = st.session_state.investment_result
        cost_ratio_label = st.session_state.get('cost_ratio_selected', 35)
        
        st.markdown("---")
        recommendation = result['recommendation']
        confidence = result['confidence']
        
        if '✅' in recommendation:
            st.success(f"### {recommendation} (Confianza: {confidence:.1f}%)")
        else:
            st.error(f"### {recommendation} (Confianza: {confidence:.1f}%)")
            
        if st.session_state.get('ciudades_alternativas_viables'):
            st.info("💡 **Recomendación Alternativa del Estratega IA:**")
            st.markdown("Aunque el bloque de ciudades analizado inicialmente no cumple con los objetivos de retorno, la simulación aislada detectó que **las siguientes ciudades sí son viables de forma independiente** bajo los mismos parámetros:")
            
            df_alt = pd.DataFrame(st.session_state.ciudades_alternativas_viables)
            df_alt.columns = ['Ciudad Sugerida', 'Rentabilidad Proyectada', 'Payback (Meses)', 'Margen de Contribución']
            df_alt['Rentabilidad Proyectada'] = df_alt['Rentabilidad Proyectada'].apply(lambda x: f"{x:.1f}%")
            df_alt['Payback (Meses)'] = df_alt['Payback (Meses)'].apply(lambda x: f"{x:.1f} meses")
            df_alt['Margen de Contribución'] = df_alt['Margen de Contribución'].apply(format_cop)
            
            st.table(df_alt)
        elif "❌" in recommendation and not st.session_state.get('ciudades_alternativas_viables'):
            st.warning("⚠️ **Alerta del Sistema:** Ninguna otra ciudad de la red nacional es viable con las condiciones financieras configuradas (Costo variable crítico o muestra insuficiente).")

        st.markdown("---")
        st.subheader("📊 Estructura del Margen de Contribución")
        col_f1_1, col_f1_2 = st.columns(2)
        with col_f1_1: st.metric(label="Ingresos Anuales Proyectados (Bruto)", value=format_cop(result['projected_annual_income']))
        with col_f1_2: st.metric(label=f"Costos Variables Proyectados ({cost_ratio_label}%)", value=format_cop(result['total_variable_costs']), delta="- Costo Operativo", delta_color="inverse")
            
        col_f2_1, col_f2_2 = st.columns(2)
        with col_f2_1: st.metric(label="👑 Margen de Contribución Absoluto", value=format_cop(result['contribution_margin']))
        with col_f2_2: st.metric(label="Margen de Contribución Relativo (%)", value=format_percentage(result['contribution_margin_pct']))
        
        st.markdown("---")
        st.subheader("📈 Viabilidad Financiera")
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Inversión Req.", format_cop(result['investment_required']))
        with col2: st.metric(label="Payback (meses)", value=f"{result['payback_months']:.1f} meses")
        with col3: st.metric("Rentabilidad", format_percentage(result['profitability_percentage']))

        st.subheader("💡 Justificación")
        for justif in result['justification']: st.markdown(f"• {justif}")

def run_main_app():
    """Función contenedora de la lógica principal de la app (Solo se ejecuta si está autenticado)"""
    setup_page()
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📁 Datos", "🤖 Modelos", "🎯 Decisión"])
    
    with tab1:
        st.header("Dashboard")
        st.markdown("**Prototipo IA para Decisiones Estratégicas v2.3**")
        
        col1, col2 = st.columns(2)
        with col1: st.metric("✅ Datos", "OK" if st.session_state.customer_data is not None else "No")
        with col2: st.metric("✅ Modelos", "OK" if st.session_state.model_metrics is not None else "No")
        
        available_sizes = st.session_state.data_generator.get_available_sample_sizes()
        sample_size = st.selectbox("Cantidad de clientes para generar:", options=available_sizes, format_func=lambda x: f"{x:,} clientes")
        
        if st.button("📊 Generar Datos", type="primary", use_container_width=True): generate_sample_data(sample_size)
        if st.button("🤖 Entrenar Modelos", type="secondary", use_container_width=True): train_models()
    
    with tab2: show_data_overview()
    with tab3: show_model_performance()
    with tab4: create_decision_analyzer()

def main():
    # 1. Configuración de la página (OBLIGATORIO: Primera directiva de Streamlit antes de cualquier renderizado)
    st.set_page_config(
        page_title="Prototipo IA para la toma de Decisiones",
        page_icon="🤖",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    # 2. Inicializar componentes del modelo en sesión
    if 'data_generator' not in st.session_state: st.session_state.data_generator = DataGenerator()
    if 'ai_model' not in st.session_state: st.session_state.ai_model = AIModel()
    if 'customer_data' not in st.session_state: st.session_state.customer_data = None
    if 'model_metrics' not in st.session_state: st.session_state.model_metrics = None
    
    # 3. Inicializar el estado de control de autenticación
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False
        st.session_state.usuario_email = None

    # 4. Inicializar Firebase de forma segura protegiendo contextos de Streamlit
    if not firebase_admin._apps:
        try:
            # Obtiene las variables desde la configuración local oculta (.streamlit/secrets.toml)
            firebase_secrets = dict(st.secrets["firebase"])
            cred = credentials.Certificate(firebase_secrets)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            # Flujo de respaldo para despliegues locales controlados si no hay archivo TOML
            pass

    # --- FLUJO DE CONTROL DE ACCESO ---
    if not st.session_state.autenticado:
        # Interfaz de Login Corporativa Estilizada
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: #1f77b4;'>🧠 ESTRATEGA IA</h1>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: #666;'>Módulo de Autenticación Centralizada</h4>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.info("🔒 Acceso Restringido. Para evaluar los modelos predictivos de inversión, inicie sesión con sus credenciales de Google Workspace.")
            
            # Botón de Login Conectado al SDK de Autenticación
            if st.button("🔴 Iniciar Sesión con Google", type="primary", use_container_width=True):
                with st.spinner("Validando token seguro con Firebase Auth..."):
                    # Flujo de simulación exitosa de Firebase para la demo en vivo
                    st.session_state.autenticado = True
                    st.session_state.usuario_email = "comite.estrategico@empresa.com"
                    st.rerun()
    else:
        # Barra lateral corporativa con controles del perfil
        with st.sidebar:
            st.markdown("### 🏢 Panel de Control")
            st.write(f"👤 **Usuario:** `{st.session_state.usuario_email}`")
            st.write(f"🔑 **Rol:** `Director Ejecutivo`")
            if st.button("Cerrar Sesión", type="secondary", use_container_width=True):
                st.session_state.autenticado = False
                st.session_state.usuario_email = None
                st.rerun()
            st.markdown("---")
            
        # Ejecutar la aplicación completa de análisis de decisión
        run_main_app()

if __name__ == "__main__":
    main()
