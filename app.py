# app.py - Versión optimizada y adaptativa para dispositivos móviles
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
        page_title="Prototipo IA para Toma de Decisiones",
        page_icon="🤖",
        layout="centered",  # Cambiar a centered para mejor adaptación en móviles
        initial_sidebar_state="collapsed"  # Colapsar sidebar por defecto en móviles
    )
    
    # CSS personalizado para mejor adaptación móvil
    st.markdown("""
        <style>
        /* Optimización para móviles */
        @media (max-width: 768px) {
            .stMetric {
                padding: 0.5rem 0 !important;
            }
            .stTabs [data-baseweb="tab-list"] {
                gap: 0px !important;
            }
            .stButton > button {
                width: 100% !important;
                font-size: 14px !important;
            }
            .stNumberInput, .stSlider, .stSelectbox, .stTextInput {
                font-size: 14px !important;
            }
        }
        
        /* Estilos generales responsive */
        .main {
            max-width: 100% !important;
            padding: 1rem !important;
        }
        
        .stMetric {
            background-color: rgba(240, 242, 246, 0.5);
            padding: 0.8rem;
            border-radius: 0.5rem;
            margin-bottom: 0.5rem;
        }
        
        h1, h2, h3 {
            word-wrap: break-word;
        }
        
        /* Tabs responsivas */
        .stTabs [data-baseweb="tab-list"] {
            flex-wrap: wrap;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🤖 IA para Decisiones")
    st.markdown("---")

def is_mobile():
    """Detecta si es dispositivo móvil basado en el tamaño de la pantalla"""
    # Streamlit no proporciona detección nativa de móvil, usamos heurísticas
    return True  # Asumir móvil para mejor adaptación

def get_responsive_cols(num_cols=4):
    """Retorna número de columnas adaptativo según dispositivo"""
    # En móviles: max 2 cols, en desktop: cols solicitadas
    return min(num_cols, 2)

def format_cop(value):
    """Formatea valores como pesos colombianos"""
    return f"${value:,.0f} COP"

def generate_sample_data():
    """Genera datos de muestra para el prototipo"""
    with st.spinner("Generando datos..."):
        st.session_state.customer_data = st.session_state.data_generator.generate_synthetic_data(1000)
        st.success(f"✅ {len(st.session_state.customer_data)} clientes generados")
        
def train_models():
    """Entrena los modelos de IA"""
    if st.session_state.customer_data is None:
        st.error("❌ Genere los datos primero")
        return
        
    with st.spinner("Entrenando modelos..."):
        # Entrenar modelo de segmentación
        segment_metrics = st.session_state.ai_model.train_segmentation_model(st.session_state.customer_data)
        
        # Entrenar modelo de impacto
        impact_metrics = st.session_state.ai_model.train_impact_model(st.session_state.customer_data)
        
        st.session_state.model_metrics = {
            'segmentation': segment_metrics,
            'impact': impact_metrics
        }
        
        st.session_state.ai_model.is_trained = True
        st.success("✅ Modelos entrenados")

def show_data_overview():
    """Muestra overview de los datos optimizado para móviles"""
    if st.session_state.customer_data is None:
        st.warning("Genere los datos primero")
        return
        
    st.subheader("📊 Resumen de Clientes")
    
    # Métricas en formato responsivo - vertical en móviles
    col_count = get_responsive_cols(4)
    cols = st.columns(col_count)
    
    metrics_data = [
        ("Total Clientes", len(st.session_state.customer_data)),
        ("Edad Promedio", f"{int(st.session_state.customer_data['edad'].mean())} años"),
        ("Ingreso Promedio", format_cop(st.session_state.customer_data['ingreso_mensual'].mean())),
        ("Valor Compra Prom.", format_cop(st.session_state.customer_data['valor_promedio_compra'].mean()))
    ]
    
    for i, (label, value) in enumerate(metrics_data):
        with cols[i % col_count]:
            st.metric(label, value)
    
    # Distribución de segmentos
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
        font=dict(size=10),
        margin=dict(l=10, r=10, t=40, b=10)
    )
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # Estadísticas por segmento - tabla simplificada
    st.subheader("📈 Estadísticas por Segmento")
    segment_stats = st.session_state.customer_data.groupby('segmento_cliente').agg({
        'edad': 'mean',
        'ingreso_mensual': 'mean',
        'valor_promedio_compra': 'mean',
        'lealtad_marca': 'mean'
    }).round(2)
    
    segment_stats.index = [st.session_state.data_generator.get_segment_description(seg) for seg in segment_stats.index]
    segment_stats.columns = ['Edad', 'Ingreso', 'Compra', 'Lealtad %']
    
    # Formatear para tabla responsive
    segment_stats['Edad'] = segment_stats['Edad'].astype(int).astype(str)
    segment_stats['Ingreso'] = segment_stats['Ingreso'].apply(lambda x: f"${x/1e6:.1f}M")
    segment_stats['Compra'] = segment_stats['Compra'].apply(lambda x: f"${x/1e3:.0f}K")
    segment_stats['Lealtad %'] = segment_stats['Lealtad %'].round(0).astype(int).astype(str)
    
    st.dataframe(segment_stats, use_container_width=True)

def show_model_performance():
    """Muestra el rendimiento de los modelos optimizado para móviles"""
    if st.session_state.model_metrics is None:
        st.warning("Entrene los modelos primero")
        return
        
    st.subheader("🤖 Rendimiento de Modelos")
    
    # Usar tabs para mejor organización en móviles
    tab1, tab2 = st.tabs(["Segmentación", "Impacto"])
    
    with tab1:
        metrics = st.session_state.model_metrics['segmentation']
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Precisión", f"{metrics['accuracy']:.3f}")
        with col2:
            st.metric("Val. Cruzada", f"{metrics['cv_mean']:.3f}")
        
        st.write("**Reporte de Clasificación:**")
        report_df = pd.DataFrame(metrics['classification_report']).transpose()
        # Simplificar columnas para móvil
        report_df = report_df[['precision', 'recall', 'f1-score']].round(3)
        st.dataframe(report_df, use_container_width=True)
    
    with tab2:
        metrics = st.session_state.model_metrics['impact']
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("RMSE", f"{metrics['rmse']:.2f}")
        with col2:
            st.metric("R² Score", f"{metrics['r2_score']:.3f}")
        
        # Gráfico de dispersión optimizado
        y_true = st.session_state.customer_data['valor_promedio_compra'].values
        X, _ = st.session_state.ai_model.prepare_data(st.session_state.customer_data)
        y_pred = st.session_state.ai_model.impact_model.predict(X)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=y_true,
            y=y_pred,
            mode='markers',
            marker=dict(size=4),
            name='Predicciones'
        ))
        fig.add_trace(go.Scatter(
            x=[y_true.min(), y_true.max()],
            y=[y_true.min(), y_true.max()],
            mode='lines',
            name='Perfecto',
            line=dict(color='red', dash='dash', width=1)
        ))
        
        fig.update_layout(
            title='Predicciones vs Reales',
            xaxis_title='Valor Real',
            yaxis_title='Predicción',
            height=350,
            font=dict(size=10),
            margin=dict(l=40, r=20, t=40, b=40),
            hovermode='closest'
        )
        st.plotly_chart(fig, use_container_width=True)

def create_scenario_analyzer():
    """Crea el analizador de escenarios optimizado para móviles"""
    st.subheader("🎯 Analizador de Escenarios")
    
    # Opciones de escenario
    scenario_types = [
        "Lanzamiento de Producto",
        "Segmentación de Clientes", 
        "Expansión de Portafolio",
        "Estrategia Abastecimiento",
        "Inversión Comercial"
    ]
    
    selected_scenario = st.selectbox("Tipo de escenario:", scenario_types, key="scenario_type")
    
    # Parámetros del escenario en expander para ahorrar espacio
    with st.expander("⚙️ Configurar Parámetros"):
        n_customers = st.slider("Clientes:", 10, 500, 100, step=10)
        
        col1, col2 = st.columns(2)
        with col1:
            min_age = st.number_input("Edad min:", 18, 80, 25, 1)
        with col2:
            max_age = st.number_input("Edad máx:", 18, 80, 45, 1)
            
        col1, col2 = st.columns(2)
        with col1:
            min_income = st.number_input("Ing. mín (M COP):", 1, 50, 3, 1)
            min_income *= 1000000
        with col2:
            max_income = st.number_input("Ing. máx (M COP):", 1, 100, 8, 1)
            max_income *= 1000000
        
        if st.button("Analizar", type="primary", use_container_width=True):
            test_customers = []
            for i in range(n_customers):
                customer = {
                    'edad': int(np.random.uniform(min_age, max_age)),
                    'ingreso_mensual': np.random.uniform(min_income, max_income),
                    'educacion': np.random.choice(['Primaria', 'Secundaria', 'Universidad', 'Posgrado']),
                    'frecuencia_compra': np.random.poisson(3),
                    'valor_promedio_compra': np.random.exponential(50000) + 10000,
                    'lealtad_marca': np.random.beta(2, 2) * 100,
                    'crecimiento_mercado': np.random.uniform(0.05, 0.15),
                    'nivel_competencia': np.random.uniform(1, 10)
                }
                test_customers.append(customer)
            
            # Analizar escenario
            with st.spinner("Analizando..."):
                scenario_results = st.session_state.ai_model.analyze_scenario(test_customers)
            
            st.session_state.scenario_results = scenario_results
            st.session_state.test_customers = test_customers
            st.rerun()
    
    # Mostrar resultados si existen
    if 'scenario_results' in st.session_state:
        scenario_results = st.session_state.scenario_results
        test_customers = st.session_state.test_customers
        
        st.subheader("📈 Resultados")
        
        # Métricas principales en columnas responsivas
        col_count = get_responsive_cols(3)
        cols = st.columns(col_count)
        
        metrics_data = [
            ("Clientes", f"{scenario_results['total_customers']}"),
            ("Impacto Prom.", format_cop(scenario_results['avg_impact'])),
            ("Impacto Total", format_cop(scenario_results['total_impact']))
        ]
        
        for i, (label, value) in enumerate(metrics_data):
            with cols[i % col_count]:
                st.metric(label, value)
        
        # Distribución de segmentos
        st.subheader("🎯 Segmentos")
        segment_dist = scenario_results['segment_distribution']
        segment_labels = [st.session_state.data_generator.get_segment_description(seg) for seg in segment_dist.keys()]
        
        fig_segment = px.pie(
            values=list(segment_dist.values()),
            names=segment_labels,
            title="Distribución",
            height=350
        )
        fig_segment.update_layout(
            font=dict(size=10),
            margin=dict(l=10, r=10, t=40, b=10)
        )
        st.plotly_chart(fig_segment, use_container_width=True)
        
        # Recomendaciones en tabs para móviles
        st.subheader("💡 Recomendaciones")
        recommendations = generate_recommendations(scenario_results, selected_scenario, test_customers)
        
        # Mostrar en expanders para mejor navegación en móvil
        with st.expander("📌 Análisis General", expanded=True):
            for rec in recommendations[:5]:
                if rec and not rec.startswith(" "):
                    st.markdown(f"**{rec}**" if "**" in rec else rec)
        
        with st.expander("📊 Análisis por Segmento"):
            in_segment_section = False
            for rec in recommendations:
                if "ANÁLISIS POR SEGMENTO" in rec:
                    in_segment_section = True
                elif "RECOMENDACIONES FINALES" in rec:
                    in_segment_section = False
                elif in_segment_section and rec.strip():
                    st.markdown(rec)
        
        with st.expander("🎯 Estrategias"):
            in_strategy_section = False
            for rec in recommendations:
                if any(x in rec for x in ["LANZAMIENTO", "SEGMENTACIÓN", "EXPANSIÓN", "ABASTECIMIENTO", "INVERSIÓN"]):
                    in_strategy_section = True
                if in_strategy_section and rec.strip():
                    st.markdown(rec)

def generate_recommendations(scenario_results, scenario_type, test_customers):
    """Genera recomendaciones estratégicas optimizadas para móviles"""
    recommendations = []
    
    segment_dist = scenario_results['segment_distribution']
    avg_impact = scenario_results['avg_impact']
    total_customers = scenario_results['total_customers']
    
    # Análisis de segmentos
    dominant_segment = max(segment_dist, key=segment_dist.get)
    segment_name = st.session_state.data_generator.get_segment_description(dominant_segment)
    segment_percentage = (segment_dist[dominant_segment] / total_customers) * 100
    
    segment_analysis = {}
    for customer in test_customers:
        segment = st.session_state.ai_model.predict_segment(customer)
        if segment not in segment_analysis:
            segment_analysis[segment] = {
                'count': 0, 'total_income': 0, 'total_purchase': 0,
                'avg_age': 0, 'avg_loyalty': 0
            }
        segment_analysis[segment]['count'] += 1
        segment_analysis[segment]['total_income'] += customer['ingreso_mensual']
        segment_analysis[segment]['total_purchase'] += customer['valor_promedio_compra']
        segment_analysis[segment]['avg_age'] += customer['edad']
        segment_analysis[segment]['avg_loyalty'] += customer['lealtad_marca']
    
    for segment in segment_analysis:
        count = segment_analysis[segment]['count']
        segment_analysis[segment]['avg_income'] = segment_analysis[segment]['total_income'] / count
        segment_analysis[segment]['avg_purchase'] = segment_analysis[segment]['total_purchase'] / count
        segment_analysis[segment]['avg_age'] = segment_analysis[segment]['avg_age'] / count
        segment_analysis[segment]['avg_loyalty'] = segment_analysis[segment]['avg_loyalty'] / count
    
    # Recomendaciones generales
    recommendations.append(f"🎯 **Segmento Dominante**: {segment_name} ({segment_percentage:.0f}%)")
    
    if avg_impact > 5000000:
        recommendations.append("💰 **Impacto Alto**: Implementar gradualmente con monitoreo")
    elif avg_impact > 2000000:
        recommendations.append("📊 **Impacto Moderado**: Requiere seguimiento periódico")
    else:
        recommendations.append("⚠️ **Impacto Bajo**: Evaluar alternativas más rentables")
    
    # Estrategias por tipo de escenario
    if "Lanzamiento" in scenario_type:
        recommendations.extend([
            "\n🚀 **LANZAMIENTO DE PRODUCTO**",
            "• Priorizar segmentos de alta capacidad",
            "• Precios competitivos para penetración",
            "• Marketing dirigido al segmento dominante",
            "• KPIs claros para medir éxito"
        ])
    elif "Segmentación" in scenario_type:
        recommendations.extend([
            "\n🎯 **SEGMENTACIÓN DE CLIENTES**",
            "• Personalizar ofertas por grupo",
            "• Programas de fidelización específicos",
            "• Canales optimizados por segmento",
            "• Pricing diferencial por grupo"
        ])
    elif "Expansión" in scenario_type:
        recommendations.extend([
            "\n📈 **EXPANSIÓN DE PORTAFOLIO**",
            "• Identificar segmentos de mayor potencial",
            "• Evaluar barreras competitivas",
            "• Alianzas estratégicas",
            "• Planear escalabilidad del sistema"
        ])
    elif "Abastecimiento" in scenario_type:
        recommendations.extend([
            "\n📦 **ABASTECIMIENTO**",
            "• Optimizar cadena de suministro",
            "• Diversificar proveedores",
            "• Inventario predictivo",
            "• KPIs logísticos clave"
        ])
    elif "Inversión" in scenario_type:
        recommendations.extend([
            "\n💼 **INVERSIÓN COMERCIAL**",
            "• Evaluar ROI por segmento",
            "• Horizonte de recuperación claro",
            "• Análisis de sensibilidad",
            "• Diversificar riesgos"
        ])
    
    # Análisis por segmento
    recommendations.append("\n📊 **ANÁLISIS POR SEGMENTO**")
    sorted_segments = sorted(segment_analysis.items(), 
                           key=lambda x: x[1]['avg_income'], reverse=True)
    
    for segment_id, analysis in sorted_segments:
        segment_name = st.session_state.data_generator.get_segment_description(segment_id)
        count = analysis['count']
        recommendations.append(f"\n**{segment_name}** ({count} clientes)")
        recommendations.append(f"• Edad: {int(analysis['avg_age'])} años")
        recommendations.append(f"• Ingreso: ${analysis['avg_income']/1e6:.1f}M COP")
        recommendations.append(f"• Compra: ${analysis['avg_purchase']/1e3:.0f}K COP")
        recommendations.append(f"• Lealtad: {analysis['avg_loyalty']:.0f}%")
        
        if segment_id == dominant_segment:
            recommendations.append("🏆 PRIORITARIO")
        elif analysis['avg_income'] > 4000000:
            recommendations.append("💎 ALTA CAPACIDAD")
        elif analysis['avg_loyalty'] > 60:
            recommendations.append("🤝 ALTA LEALTAD")
    
    # Recomendaciones finales
    recommendations.append("\n🎯 **RECOMENDACIONES FINALES**")
    
    if avg_impact > 8000000:
        recommendations.append("⚠️ RIESGO ALTO: Piloto primero")
    elif avg_impact > 3000000:
        recommendations.append("📊 RIESGO MODERADO: Monitoreo constante")
    else:
        recommendations.append("✅ RIESGO BAJO: Implementación directa")
    
    if total_customers > 200:
        recommendations.append("🚀 ESCALABILIDAD: Alto potencial de expansión")
    elif total_customers > 100:
        recommendations.append("📈 CRECIMIENTO: Potencial con optimización")
    else:
        recommendations.append("🎯 ENFOQUE: Priorizar calidad")
    
    return recommendations

# Función principal
def main():
    # Inicializar session state
    if 'data_generator' not in st.session_state:
        st.session_state.data_generator = DataGenerator()
    if 'ai_model' not in st.session_state:
        st.session_state.ai_model = AIModel()
    if 'customer_data' not in st.session_state:
        st.session_state.customer_data = None
    if 'model_metrics' not in st.session_state:
        st.session_state.model_metrics = None
    
    setup_page()
    
    # Navegación con tabs para mejor adaptación móvil
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📁 Datos", "🤖 Modelos", "🎯 Análisis"])
    
    with tab1:
        st.header("Dashboard")
        st.markdown("**Prototipo IA para Decisiones Estratégicas**")
        
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
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 Generar Datos", type="primary", use_container_width=True):
                generate_sample_data()
                
        with col2:
            if st.button("🤖 Entrenar", type="secondary", use_container_width=True):
                train_models()
    
    with tab2:
        st.header("Datos")
        show_data_overview()
            
    with tab3:
        st.header("Modelos")
        show_model_performance()
            
    with tab4:
        st.header("Análisis")
        create_scenario_analyzer()

if __name__ == "__main__":
    main()
