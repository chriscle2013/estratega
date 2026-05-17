# app.py - Versión optimizada para dispositivos móviles
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
    # Configuración responsiva
    st.set_page_config(
        page_title="Prototipo IA para Toma de Decisiones",
        page_icon="🤖",
        layout="wide",  # Cambiar a wide para mejor adaptación
        initial_sidebar_state="collapsed"  # Colapsar sidebar en móviles
    )
    
    # Título responsivo
    st.title("🤖 Prototipo IA para Toma de Decisiones")
    st.markdown("---")

def format_cop(value):
    """Formatea valores como pesos colombianos"""
    return f"${value:,.0f} COP"

def generate_sample_data():
    """Genera datos de muestra para el prototipo"""
    with st.spinner("Generando datos..."):
        st.session_state.customer_data = st.session_state.data_generator.generate_synthetic_data(1000)
        st.success(f"✅ Datos generados: {len(st.session_state.customer_data)} clientes")
        
def train_models():
    """Entrena los modelos de IA"""
    if st.session_state.customer_data is None:
        st.error("❌ Primero genere los datos")
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
        st.warning("Primero genere los datos")
        return
        
    st.subheader("📊 Resumen de Clientes")
    
    # Métricas en columna única para móviles
    col1 = st.columns(1)[0]
    
    with col1:
        st.metric("Total Clientes", len(st.session_state.customer_data))
        st.metric("Edad Promedio", f"{int(st.session_state.customer_data['edad'].mean())} años")
        st.metric("Ingreso Promedio", format_cop(st.session_state.customer_data['ingreso_mensual'].mean()))
        st.metric("Valor Promedio Compra", format_cop(st.session_state.customer_data['valor_promedio_compra'].mean()))
    
    # Distribución de segmentos
    st.subheader("🎯 Distribución de Segmentos")
    segment_counts = st.session_state.customer_data['segmento_cliente'].value_counts()
    segment_labels = [st.session_state.data_generator.get_segment_description(seg) for seg in segment_counts.index]
    
    # Gráfico más pequeño para móviles
    fig_pie = px.pie(
        values=segment_counts.values,
        names=segment_labels,
        title="Distribución de Segmentos",
        height=300
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
    segment_stats['edad'] = segment_stats['edad'].astype(int).astype(str) + ' años'
    segment_stats['ingreso_mensual'] = segment_stats['ingreso_mensual'].apply(format_cop)
    segment_stats['valor_promedio_compra'] = segment_stats['valor_promedio_compra'].apply(format_cop)
    segment_stats['lealtad_marca'] = segment_stats['lealtad_marca'].round(1).astype(str) + '%'
    
    # Tabla responsive
    st.dataframe(segment_stats, use_container_width=True)

def show_model_performance():
    """Muestra el rendimiento de los modelos optimizado para móviles"""
    if st.session_state.model_metrics is None:
        st.warning("Primero entrene los modelos")
        return
        
    st.subheader("🤖 Rendimiento de Modelos de IA")
    
    # Métricas en una columna
    col1 = st.columns(1)[0]
    
    with col1:
        metrics = st.session_state.model_metrics['segmentation']
        st.metric("Precisión Segmentación", f"{metrics['accuracy']:.3f}")
        st.metric("Validación Cruzada", f"{metrics['cv_mean']:.3f} ± {metrics['cv_std']:.3f}")
        
        # Reporte de clasificación simplificado
        st.write("Reporte de Clasificación:")
        report_df = pd.DataFrame(metrics['classification_report']).transpose()
        st.dataframe(report_df, use_container_width=True)
    
    # Métricas de impacto
    col2 = st.columns(1)[0]
    
    with col2:
        metrics = st.session_state.model_metrics['impact']
        st.metric("RMSE", f"{metrics['rmse']:.2f}")
        st.metric("R² Score", f"{metrics['r2_score']:.3f}")
    
    # Gráfico de dispersión más pequeño
    st.subheader("📈 Predicciones vs Reales")
    y_true = st.session_state.customer_data['valor_promedio_compra'].values
    X, _ = st.session_state.ai_model.prepare_data(st.session_state.customer_data)
    y_pred = st.session_state.ai_model.impact_model.predict(X)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=y_true,
        y=y_pred,
        mode='markers',
        name='Predicciones vs Reales'
    ))
    fig.add_trace(go.Scatter(
        x=[y_true.min(), y_true.max()],
        y=[y_true.min(), y_true.max()],
        mode='lines',
        name='Línea Perfecta',
        line=dict(color='red', dash='dash')
    ))
    
    fig.update_layout(
        title='Predicciones vs Valores Reales',
        xaxis_title='Valor Real (COP)',
        yaxis_title='Predicción (COP)',
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)

def create_scenario_analyzer():
    """Crea el analizador de escenarios optimizado para móviles"""
    st.subheader("🎯 Analizador de Escenarios")
    
    # Selector de escenario más pequeño
    scenario_types = [
        "Lanzamiento de Producto",
        "Segmentación de Clientes", 
        "Expansión de Portafolio",
        "Estrategia Abastecimiento",
        "Inversión Comercial"
    ]
    
    selected_scenario = st.selectbox("Tipo de escenario:", scenario_types)
    
    # Parámetros del escenario
    st.subheader("Parámetros del Escenario")
    
    with st.expander("Configurar Clientes"):
        n_customers = st.slider("Clientes:", 10, 500, 100)
        
        # Inputs en columna única
        col1 = st.columns(1)[0]
        with col1:
            min_age = st.number_input("Edad mínima:", 18, 80, 25, 1)
            max_age = st.number_input("Edad máxima:", 18, 80, 45, 1)
            min_income = st.number_input("Ingreso mínimo COP:", 1000000, 50000000, 3000000, 100000)
            max_income = st.number_input("Ingreso máximo COP:", 1000000, 100000000, 8000000, 100000)
        
        if st.button("Generar y Analizar", type="primary"):
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
            
            # Resultados compactos
            st.subheader("📊 Resultados del Análisis")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total", scenario_results['total_customers'])
            with col2:
                st.metric("Impacto Promedio", format_cop(scenario_results['avg_impact']))
            with col3:
                st.metric("Impacto Total", format_cop(scenario_results['total_impact']))
            
            # Gráfico de segmentos
            st.subheader("🎯 Distribución de Segmentos")
            segment_dist = scenario_results['segment_distribution']
            segment_labels = [st.session_state.data_generator.get_segment_description(seg) for seg in segment_dist.keys()]
            
            fig_segment = px.pie(
                values=list(segment_dist.values()),
                names=segment_labels,
                title="Distribución",
                height=250
            )
            st.plotly_chart(fig_segment, use_container_width=True)
            
            # Recomendaciones más compactas
            st.subheader("💡 Recomendaciones")
            recommendations = generate_recommendations(scenario_results, selected_scenario, test_customers)
            
            # Mostrar recomendaciones con mejor formato para móviles
            for rec in recommendations:
                if rec.startswith("🎯 **") or rec.startswith("💰 **") or rec.startswith("📊 **"):
                    st.markdown(f"### {rec}")
                elif rec.startswith("🚀 **") or rec.startswith("🎯 **") or rec.startswith("💼 **"):
                    st.markdown(f"**{rec}**")
                elif rec.startswith("  •"):
                    st.markdown(f"> {rec}")
                elif rec == "":
                    st.markdown("")
                else:
                    st.write(rec)

def generate_recommendations(scenario_results, scenario_type, test_customers):
    """Genera recomendaciones estratégicas mejoradas para móviles"""
    recommendations = []
    
    segment_dist = scenario_results['segment_distribution']
    avg_impact = scenario_results['avg_impact']
    total_customers = scenario_results['total_customers']
    
    # Segmento dominante
    dominant_segment = max(segment_dist, key=segment_dist.get)
    segment_name = st.session_state.data_generator.get_segment_description(dominant_segment)
    segment_percentage = (segment_dist[dominant_segment] / total_customers) * 100
    
    recommendations.append(f"🎯 **SEGMENTO DOMINANTE**: {segment_name} ({segment_percentage:.1f}%)")
    
    # Impacto
    if avg_impact > 5000000:
        recommendations.append("💰 **IMPACTO ALTO**: Implementación gradual con monitoreo")
    elif avg_impact > 2000000:
        recommendations.append("📊 **IMPACTO MODERADO**: Requiere seguimiento periódico")
    else:
        recommendations.append("⚠️ **IMPACTO BAJO**: Evaluar alternativa más rentable")
    
    # Recomendaciones por tipo de escenario
    if "Lanzamiento" in scenario_type:
        recommendations.extend([
            "🚀 **ESTRATEGIA DE LANZAMIENTO**:",
            "  • Priorizar segmentos con alta capacidad de compra",
            "  • Precios competitivos para penetración de mercado",
            "  • Marketing dirigido al segmento dominante",
            "  • Indicadores de éxito claros y medibles",
            "  • Plan de contingencia para bajo rendimiento"
        ])
    elif "Segmentación" in scenario_type:
        recommendations.extend([
            "🎯 **ESTRATEGIA DE SEGMENTACIÓN**:",
            "  • Personalizar ofertas por grupo demográfico",
            "  • Programas de fidelización específicos",
            "  • Comunicación optimizada por segmento",
            "  • Pricing diferencial por grupo",
            "  • Métricas de satisfacción por segmento"
        ])
    elif "Expansión" in scenario_type:
        recommendations.extend([
            "📈 **ESTRATEGIA DE EXPANSIÓN**:",
            "  • Identificar segmentos con mayor potencial",
            "  • Evaluar barreras de entrada y competencia",
            "  • Posicionamiento diferencial claro",
            "  • Alianzas estratégicas complementarias",
            "  • Escalabilidad del sistema para mayor demanda"
        ])
    elif "Abastecimiento" in scenario_type:
        recommendations.extend([
            "📦 **ESTRATEGIA DE ABASTECIMIENTO**:",
            "  • Optimizar cadenas según comportamiento segmento",
            "  • Diversificar proveedores para reducir riesgos",
            "  • Inventario predictivo basado en demanda",
            "  • Negociar condiciones específicas con proveedores",
            "  • Indicadores logísticos clave (KPIs)"
        ])
    elif "Inversión" in scenario_type:
        recommendations.extend([
            "💼 **ESTRATEGIA DE INVERSIÓN**:",
            "  • Evaluar ROI por segmento y priorizar",
            "  • Horizonte temporal de recuperación",
            "  • Sensibilidad a variables macroeconómicas",
            "  • Diversificar portafolio para mitigar riesgos",
            "  • Controles y evaluación periódica"
        ])
    
    # Análisis detallado por segmento
    recommendations.append("\n📊 **ANÁLISIS POR SEGMENTO**:")
    
    # Simplificar el análisis para móviles
    for segment_id in sorted(segment_dist.keys(), key=lambda x: segment_dist[x], reverse=True):
        segment_name = st.session_state.data_generator.get_segment_description(segment_id)
        count = segment_dist[segment_id]
        percentage = (count / total_customers) * 100
        
        recommendations.append(f"  • **{segment_name}**: {count} clientes ({percentage:.1f}%)")
        
        if segment_id == dominant_segment:
            recommendations.append("    🏆 **SEGMENTO PRIORITARIO**")
        elif segment_id in [1, 2]:  # Profesionales y Familias
            recommendations.append("    💎 **ALTA CAPACIDAD ADQUISITIVA**")
    
    # Recomendaciones finales
    recommendations.append("\n🎯 **RECOMENDACIONES FINALES**:")
    
    if avg_impact > 8000000:
        recommendations.append("  ⚠️ **RIESGO ALTO**: Implementación piloto primero")
    elif avg_impact > 3000000:
        recommendations.append("  📊 **RIESGO MODERADO**: Monitoreo constante")
    else:
        recommendations.append("  ✅ **RIESGO BAJO**: Implementación directa")
    
    if total_customers > 200:
        recommendations.append("  🚀 **ESCALABILIDAD**: Potencial de expansión")
    elif total_customers > 100:
        recommendations.append("  📈 **CRECIMIENTO**: Optimización recomendada")
    else:
        recommendations.append("  🎯 **ENFOQUE**: Calidad sobre cantidad")
    
    return recommendations

# Función principal optimizada para móviles
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
    
    # Navegación optimizada para móviles
    st.sidebar.title("📱 Menú")
    page = st.sidebar.selectbox(
        "Seleccionar sección:",
        ["Dashboard", "Datos", "Modelos", "Análisis"]
    )
    
    if page == "Dashboard":
        st.header("📊 Dashboard")
        st.subheader("🎯 Resumen del Proyecto")
        st.markdown("Prototipo de IA para Soporte en Toma de Decisiones Estratégicas")
        
        # Estado del sistema
        st.subheader("📈 Estado del Sistema")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.session_state.customer_data is not None:
                st.metric("✅ Datos", "Generados")
            else:
                st.metric("❌ Datos", "No generados")
                
        with col2:
            if st.session_state.model_metrics is not None:
                st.metric("✅ Modelos", "Entrenados")
            else:
                st.metric("❌ Modelos",
