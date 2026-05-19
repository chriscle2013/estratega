Aquí tienes el código completo y actualizado de app.py.

He replicado exactamente la misma lógica de segmentación geográfica en la pantalla de 🚀 Lanzamiento de Producto. Ahora, antes de procesar las métricas, podrás segmentar la población objetivo eligiendo entre las principales ciudades de Colombia dispersadas desde tu base de datos (Bogotá, Medellín, Cali, Barranquilla, Bucaramanga y Cartagena).

Cambios aplicados:
Población Objetivo Geográfica en Lanzamiento: Se añadió el componente st.multiselect dentro del expander de configuración de parámetros de lanzamiento.

Filtrado Dinámico por Ciudades: Al hacer clic en "Analizar Lanzamiento", el DataFrame de clientes se filtra cruzando las ciudades seleccionadas junto con los rangos de edad e ingresos.

Python
# app.py - Versión 2.2 con Filtro Geográfico Completo (Lanzamiento e Inversión)
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
from typing import Dict, List

# Importar módulos locales
from data_generator import DataGenerator
from ai_model import AIModel
from config import APP_CONFIG

class BusinessDecisionApp:
    def __init__(self):
        # Inicializar variables de la aplicación
        self.customer_data = None
        self.model_metrics = None
        self.ai_model = AIModel()
        self.data_generator = DataGenerator()

def setup_page():
    """Configuración inicial de la página optimizada para móviles"""
    st.set_page_config(
        page_title="Prototipo IA para la toma de Decisiones",
        page_icon="🤖",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
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
    
    st.title("🤖 Estratega IA / Toma Decisiones v2.2")
    st.markdown("---")

def format_cop(value):
    """Formatea valores como pesos colombianos"""
    return f"${value:,.0f} COP"

def format_percentage(value):
    """Formatea porcentajes"""
    return f"{value:.1f}%"

def generate_sample_data(n_samples):
    """Genera datos de muestra para el prototipo"""
    with st.spinner(f"Generando {n_samples:,} clientes..."):
        st.session_state.customer_data = st.session_state.data_generator.generate_synthetic_data(n_samples)
        st.success(f"✅ {len(st.session_state.customer_data)} clientes generados")
    
    st.rerun()

def train_models():
    """Entrena los modelos de IA"""
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
    """Muestra overview de los datos"""
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
    
    fig_pie = px.pie(
        values=segment_counts.values,
        names=segment_labels,
        title="Segmentos",
        height=350
    )
    fig_pie.update_layout(
        font=dict(size=11),
        margin=dict(l=10, r=10, t=40, b=10)
    )
    st.plotly_chart(fig_pie, use_container_width=True)

def show_model_performance():
    """Muestra el rendimiento de los modelos"""
    if st.session_state.model_metrics is None:
        st.warning("Entrene los modelos primero")
        return
        
    st.subheader("🤖 Rendimiento de Modelos")
    
    tab1, tab2 = st.tabs(["📊 Segmentación", "📈 Impacto"])
    
    with tab1:
        metrics = st.session_state.model_metrics['segmentation']
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Precisión", f"{metrics['accuracy']:.3f}")
        with col2:
            st.metric("Val. Cruzada", f"{metrics['cv_mean']:.3f}")
    
    with tab2:
        metrics = st.session_state.model_metrics['impact']
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("RMSE", f"{metrics['rmse']:.2f}")
        with col2:
            st.metric("R² Score", f"{metrics['r2_score']:.3f}")

def create_decision_analyzer():
    """Analizador de decisiones con 2 opciones: Lanzamiento e Inversión"""
    st.subheader("🎯 Análisis de Decisión IA")
    
    if not st.session_state.ai_model.is_trained:
        st.error("❌ Entrene los modelos primero (Tab Modelos)")
        return
    
    # Selector de tipo de análisis
    analysis_type = st.radio(
        "Selecciona tipo de análisis:",
        options=["🚀 Lanzamiento de Producto", "💼 Inversión Comercial (Infraestructura)"],
        horizontal=False
    )
    
    st.markdown("")
    
    if analysis_type == "🚀 Lanzamiento de Producto":
        create_launch_analyzer()
    else:
        create_investment_analyzer()

def create_launch_analyzer():
    """Analizador para lanzamiento de producto con Filtro Demográfico de Ciudades de Colombia"""
    st.subheader("🚀 Lanzamiento de Producto")
    
    max_customers_available = len(st.session_state.customer_data) if st.session_state.customer_data is not None else 1000
    
    with st.expander("⚙️ Configurar Parámetros", expanded=True):
        
        # NUEVO: Selección de Población Geográfica para Lanzamientos
        st.markdown("### 🌆 Población Objetivo Geográfica")
        ciudades_disponibles = ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Bucaramanga', 'Cartagena']
        ciudades_seleccionadas = st.multiselect(
            "Selecciona las ciudades para enfocar el análisis de lanzamiento:",
            options=ciudades_disponibles,
            default=ciudades_disponibles, # Por defecto analiza toda la población dispersada
            key="ciudades_launch",
            help="Permite aislar o consolidar el mercado según las principales ciudades de Colombia."
        )
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            n_customers = st.slider(
                "Clientes a analizar:", 
                min_value=50, 
                max_value=int(max_customers_available), 
                value=min(300, int(max_customers_available)), 
                step=5
            )
        with col2:
            product_price = st.number_input("Precio del producto (COP):", 5000, 2000000, 25000, step=1000)
        
        st.markdown("")
        col1, col2 = st.columns(2)
        with col1:
            min_age = st.number_input("Edad mín:", 18, 80, 20, 1)
        with col2:
            max_age = st.number_input("Edad máx:", 18, 80, 60, 1)
        
        st.markdown("")
        col1, col2 = st.columns(2)
        with col1:
            min_income = st.number_input("Ing. mín (M COP):", 1, 50, 2, 1) * 1000000
        with col2:
            max_income = st.number_input("Ing. máx (M COP):", 1, 100, 8, 1) * 1000000
        
        st.markdown("")
        min_viable = st.number_input("Ingresos mínimos viables (M COP):", 10, 5000, 30, 1) * 1000000
        
        st.markdown("")
        if st.button("🔍 Analizar Lanzamiento", type="primary", use_container_width=True):
            # APLICADO: Filtro demográfico cruzado con las ciudades seleccionadas
            filtered_data = st.session_state.customer_data[
                (st.session_state.customer_data['edad'] >= min_age) & 
                (st.session_state.customer_data['edad'] <= max_age) &
                (st.session_state.customer_data['ingreso_mensual'] >= min_income) &
                (st.session_state.customer_data['ingreso_mensual'] <= max_income) &
                (st.session_state.customer_data['ciudad'].isin(ciudades_seleccionadas))
            ]
            
            if len(filtered_data) < 10:
                filtered_data = st.session_state.customer_data
                
            sample_n = min(n_customers, len(filtered_data))
            test_customers = filtered_data.sample(n=sample_n).to_dict(orient='records')
            
            with st.spinner("Analizando..."):
                launch_result = st.session_state.ai_model.evaluate_product_launch(
                    test_customers,
                    product_price=product_price,
                    min_viable_revenue=min_viable
                )
            
                st.session_state.launch_result = launch_result
                st.rerun()
    
    # Mostrar resultados
    if 'launch_result' in st.session_state:
        result = st.session_state.launch_result
        
        st.markdown("")
        st.markdown("---")
        
        # Recomendación principal
        recommendation = result['recommendation']
        confidence = result['confidence']
        
        if '✅' in recommendation:
            st.success(f"### {recommendation} (Confianza: {confidence:.1f}%)")
        else:
            st.error(f"### {recommendation} (Confianza: {confidence:.1f}%)")
        
        st.markdown("")
        
        # Métricas principales
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Compradores Est.", f"{result['estimated_buyers']:,}")
        with col2:
            st.metric("% de Compra", format_percentage(result['purchase_percentage']))
        with col3:
            st.metric("ROI Est.", format_percentage(result['estimated_roi']))
        
        st.markdown("")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Ingresos Proy.", format_cop(result['projected_revenue']))
        with col2:
            st.metric("Mínimo Viable", format_cop(result['min_viable_revenue']))
        
        st.markdown("")
        st.metric("Propensión Promedio", format_percentage(result['avg_propensity']))
        
        # Justificación
        st.markdown("")
        st.subheader("💡 Justificación")
        for justif in result['justification']:
            st.markdown(f"• {justif}")

def create_investment_analyzer():
    """Analizador para inversión comercial con Filtro Demográfico de Ciudades de Colombia"""
    st.subheader("💼 Inversión Comercial (Infraestructura)")
    
    max_customers_available = len(st.session_state.customer_data) if st.session_state.customer_data is not None else 2000
    
    with st.expander("⚙️ Configurar Parámetros", expanded=True):
        
        st.markdown("### 🌆 Población Objetivo Geográfica")
        ciudades_disponibles = ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Bucaramanga', 'Cartagena']
        ciudades_seleccionadas = st.multiselect(
            "Selecciona las ciudades para enfocar el análisis:",
            options=ciudades_disponibles,
            default=ciudades_disponibles,
            key="ciudades_investment",
            help="Permite aislar o consolidar el mercado según las principales ciudades de Colombia."
        )
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            n_customers = st.slider(
                "Clientes a analizar:", 
                min_value=100, 
                max_value=int(max_customers_available), 
                value=min(500, int(max_customers_available)), 
                step=100
            )
        with col2:
            investment = st.number_input(
                "Inversión requerida (M COP):", 
                min_value=10, 
                max_value=50000, 
                value=10000, 
                step=10
            ) * 1000000
        
        st.markdown("")
        col1, col2 = st.columns(2)
        with col1:
            min_age = st.number_input("Edad mín:", 18, 80, 25, 1)
        with col2:
            max_age = st.number_input("Edad máx:", 18, 80, 65, 1)
        
        st.markdown("")
        col1, col2 = st.columns(2)
        with col1:
            min_income = st.number_input("Ing. mín (M COP):", 1, 50, 2, 1) * 1000000
        with col2:
            max_income = st.number_input("Ing. máx (M COP):", 1, 100, 9, 1) * 1000000
        
        st.markdown("")
        cost_ratio_input = st.slider(
            "Tasa estimada de Costo Variable (% sobre ingreso):",
            min_value=10,
            max_value=100,
            value=35,
            step=1,
            help="Porcentaje del ingreso que se consume directamente en la operación logística o de servicio por cada cliente atraído."
        )
        
        st.markdown("")
        if st.button("🔍 Analizar Inversión", type="primary", use_container_width=True):
            filtered_data = st.session_state.customer_data[
                (st.session_state.customer_data['edad'] >= min_age) & 
                (st.session_state.customer_data['edad'] <= max_age) &
                (st.session_state.customer_data['ingreso_mensual'] >= min_income) &
                (st.session_state.customer_data['ingreso_mensual'] <= max_income) &
                (st.session_state.customer_data['ciudad'].isin(ciudades_seleccionadas))
            ]
            
            if len(filtered_data) < 10:
                filtered_data = st.session_state.customer_data
                
            sample_n = min(n_customers, len(filtered_data))
            test_customers = filtered_data.sample(n=sample_n).to_dict(orient='records')
            
            with st.spinner("Analizando..."):
                investment_result = st.session_state.ai_model.evaluate_infrastructure_investment(
                    test_customers,
                    investment_required=investment,
                    variable_cost_ratio=cost_ratio_input / 100.0
                )
            
                st.session_state.investment_result = investment_result
                st.session_state.cost_ratio_selected = cost_ratio_input
                st.rerun()
    
    # Mostrar resultados reestructurados
    if 'investment_result' in st.session_state:
        result = st.session_state.investment_result
        cost_ratio_label = st.session_state.get('cost_ratio_selected', 35)
        
        st.markdown("")
        st.markdown("---")
        
        # Recomendación principal
        recommendation = result['recommendation']
        confidence = result['confidence']
        
        if '✅' in recommendation:
            st.success(f"### {recommendation} (Confianza: {confidence:.1f}%)")
        else:
            st.error(f"### {recommendation} (Confianza: {confidence:.1f}%)")
        
        st.markdown("")
        
        # Estructura del Margen de Contribución
        st.subheader("📊 Estructura del Margen de Contribución")
        
        col_f1_1, col_f1_2 = st.columns(2)
        with col_f1_1:
            st.metric(
                label="Ingresos Anuales Proyectados (Bruto)", 
                value=format_cop(result['projected_annual_income']),
                help="Volumen total de ingresos brutos estimados."
            )
        with col_f1_2:
            st.metric(
                label=f"Costos Variables Proyectados ({cost_ratio_label}%)", 
                value=format_cop(result['total_variable_costs']),
                delta="- Costo Operativo",
                delta_color="inverse",
                help="Monto absorbido directamente por el costo de operación."
            )
            
        col_f2_1, col_f2_2 = st.columns(2)
        with col_f2_1:
            st.metric(
                label="👑 Margen de Contribución Absoluto", 
                value=format_cop(result['contribution_margin']),
                help="Dinero real disponible que le queda al proyecto para amortizar la infraestructura."
            )
        with col_f2_2:
            st.metric(
                label="Margen de Contribución Relativo (%)", 
                value=format_percentage(result['contribution_margin_pct']),
                help="Eficiencia del negocio libre de costos variables."
            )
        
        st.markdown("---")
        
        # Métricas de Retorno e Inversión Base
        st.subheader("📈 Viabilidad Financiera")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Inversión Req.", format_cop(result['investment_required']))
        with col2:
            payback = result['payback_months']
            st.metric(
                label="Payback (meses)", 
                value=f"{payback:.1f} meses",
                delta="Excede Límite (18m)" if payback > 18 else "Tiempo Óptimo",
                delta_color="inverse" if payback > 18 else "normal"
            )
        with col3:
            st.metric("Rentabilidad", format_percentage(result['profitability_percentage']))
        
        st.markdown("")
        st.metric("Propensión Promedio de Compra", format_percentage(result['avg_propensity']))
        
        # Criterios de viabilidad
        st.markdown("")
        st.subheader("✓ Criterios de Viabilidad")
        
        criteria = result['criteria_met']
        col1, col2 = st.columns(2)
        
        with col1:
            if criteria['market_size']:
                st.markdown("✅ Tamaño de mercado >= 500 clientes")
            else:
                st.markdown("❌ Tamaño de mercado < 500 clientes")
            
            if criteria['income_ratio']:
                st.markdown("✅ Ingresos >= 50% inversión")
            else:
                st.markdown("❌ Ingresos < 50% inversión")
        
        with col2:
            if criteria['payback']:
                st.markdown("✅ Payback <= 18 meses")
            else:
                st.markdown("❌ Payback > 18 meses")
            
            if criteria['propensity']:
                st.markdown("✅ Propensión >= 45%")
            else:
                st.markdown("❌ Propensión < 45%")
        
        # Justificación
        st.markdown("")
        st.subheader("💡 Justificación")
        for justif in result['justification']:
            st.markdown(f"• {justif}")

def main():
    if 'data_generator' not in st.session_state:
        st.session_state.data_generator = DataGenerator()
    if 'ai_model' not in st.session_state:
        st.session_state.ai_model = AIModel()
    if 'customer_data' not in st.session_state:
        st.session_state.customer_data = None
    if 'model_metrics' not in st.session_state:
        st.session_state.model_metrics = None
    
    setup_page()
    
    # Navegación con tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📁 Datos", "🤖 Modelos", "🎯 Decisión"])
    
    with tab1:
        st.header("Dashboard")
        st.markdown("**Prototipo IA para Decisiones Estratégicas v2.2**")
        
        st.markdown("")
        st.subheader("📈 Estado del Sistema")
        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.customer_data is not None:
                st.metric("✅ Datos", "OK")
            else:
                st.metric("❌ Datos", "No")
                
        with col2:
            if st.session_state.model_metrics is not None:
                st.metric("✅ Modelos", "OK")
            else:
                st.metric("❌ Modelos", "No")
        
        st.markdown("")
        st.subheader("📊 Seleccionar Tamaño de Muestra")
        
        available_sizes = st.session_state.data_generator.get_available_sample_sizes()
        sample_size = st.selectbox(
            "Cantidad de clientes para generar:",
            options=available_sizes,
            format_func=lambda x: f"{x:,} clientes",
            key="sample_size"
        )
        
        st.markdown("")
        
        if st.button("📊 Generar Datos", type="primary", use_container_width=True, key="btn_generate"):
            generate_sample_data(sample_size)
        
        st.markdown("")
        
        if st.button("🤖 Entrenar Modelos", type="secondary", use_container_width=True, key="btn_train"):
            train_models()
        
        st.markdown("---")
        st.markdown("### ℹ️ Instrucciones")
        st.markdown("""
        1. **Seleccionar Muestra**: Elige un tamaño de muestra permitido (ej. 5,000)
        2. **Generar Datos**: Crea el dataset sintético distribuido en Colombia
        3. **Entrenar Modelos**: Entrena los modelos de IA
        4. **Explorar**: Navega por otras secciones
        5. **Analizar**: Usa la sección "Decisión" para análisis geográfico en ambos módulos
        """)
    
    with tab2:
        st.header("Datos")
        show_data_overview()
            
    with tab3:
        st.header("Modelos")
        show_model_performance()
            
    with tab4:
        st.header("Análisis de Decisión")
        create_decision_analyzer()

if __name__ == "__main__":
    main()
