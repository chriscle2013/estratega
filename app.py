# app.py - Versión corregida para mostrar enteros en edad y pesos colombianos
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
    """Configuración inicial de la página"""
    st.set_page_config(
        page_title="Prototipo IA para Toma de Decisiones",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Prototipo IA para Soporte en Toma de Decisiones Estratégicas")
    st.markdown("---")

def generate_sample_data():
    """Genera datos de muestra para el prototipo"""
    with st.spinner("Generando datos de clientes..."):
        st.session_state.customer_data = st.session_state.data_generator.generate_synthetic_data(1000)
        st.success(f"✅ Datos generados: {len(st.session_state.customer_data)} clientes")
        
def train_models():
    """Entrena los modelos de IA"""
    if st.session_state.customer_data is None:
        st.error("❌ Primero genere los datos de clientes")
        return
        
    with st.spinner("Entrenando modelos de IA..."):
        # Entrenar modelo de segmentación
        segment_metrics = st.session_state.ai_model.train_segmentation_model(st.session_state.customer_data)
        
        # Entrenar modelo de impacto
        impact_metrics = st.session_state.ai_model.train_impact_model(st.session_state.customer_data)
        
        st.session_state.model_metrics = {
            'segmentation': segment_metrics,
            'impact': impact_metrics
        }
        
        st.session_state.ai_model.is_trained = True
        st.success("✅ Modelos de IA entrenados exitosamente")
        
def format_cop(value):
    """Formatea valores como pesos colombianos"""
    return f"${value:,.0f} COP"

def show_data_overview():
    """Muestra overview de los datos"""
    if st.session_state.customer_data is None:
        st.warning("Primero genere los datos de clientes desde el Dashboard Principal")
        return
        
    st.subheader("📊 Vista General de Datos de Clientes")
    
    # Métricas básicas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Clientes", len(st.session_state.customer_data))
        
    with col2:
        # Edad como número entero
        st.metric("Edad Promedio", f"{int(st.session_state.customer_data['edad'].mean())} años")
        
    with col3:
        # Ingreso en pesos colombianos
        st.metric("Ingreso Promedio", format_cop(st.session_state.customer_data['ingreso_mensual'].mean()))
        
    with col4:
        # Valor de compra en pesos colombianos
        st.metric("Valor Promedio Compra", format_cop(st.session_state.customer_data['valor_promedio_compra'].mean()))
    
    # Distribución de segmentos
    st.subheader("🎯 Distribución de Segmentos de Clientes")
    segment_counts = st.session_state.customer_data['segmento_cliente'].value_counts()
    segment_labels = [st.session_state.data_generator.get_segment_description(seg) for seg in segment_counts.index]
    
    fig_pie = px.pie(
        values=segment_counts.values,
        names=segment_labels,
        title="Distribución de Segmentos"
    )
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # Estadísticas por segmento
    st.subheader("📈 Estadísticas por Segmento")
    segment_stats = st.session_state.customer_data.groupby('segmento_cliente').agg({
        'edad': 'mean',
        'ingreso_mensual': 'mean',
        'valor_promedio_compra': 'mean',
        'lealtad_marca': 'mean'
    }).round(2)
    
    segment_stats.index = [st.session_state.data_generator.get_segment_description(seg) for seg in segment_stats.index]
    
    # Formatear los valores para mostrar enteros en edad y pesos colombianos
    segment_stats['edad'] = segment_stats['edad'].astype(int).astype(str) + ' años'
    segment_stats['ingreso_mensual'] = segment_stats['ingreso_mensual'].apply(format_cop)
    segment_stats['valor_promedio_compra'] = segment_stats['valor_promedio_compra'].apply(format_cop)
    segment_stats['lealtad_marca'] = segment_stats['lealtad_marca'].round(1).astype(str) + '%'
    
    st.dataframe(segment_stats)
    
def show_model_performance():
    """Muestra el rendimiento de los modelos"""
    if st.session_state.model_metrics is None:
        st.warning("Primero entrene los modelos de IA desde el Dashboard Principal")
        return
        
    st.subheader("📊 Rendimiento de Modelos de IA")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Modelo de Segmentación")
        metrics = st.session_state.model_metrics['segmentation']
        
        st.metric("Precisión", f"{metrics['accuracy']:.3f}")
        st.metric("Validación Cruzada", f"{metrics['cv_mean']:.3f} ± {metrics['cv_std']:.3f}")
        
        # Reporte de clasificación
        st.write("Reporte de Clasificación:")
        report_df = pd.DataFrame(metrics['classification_report']).transpose()
        st.dataframe(report_df)
        
    with col2:
        st.subheader("Modelo de Impacto")
        metrics = st.session_state.model_metrics['impact']
        
        st.metric("RMSE", f"{metrics['rmse']:.2f}")
        st.metric("R² Score", f"{metrics['r2_score']:.3f}")
        
        # Gráfico de dispersión
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
            yaxis_title='Predicción (COP)'
        )
        st.plotly_chart(fig, use_container_width=True)

def create_scenario_analyzer():
    """Crea el analizador de escenarios"""
    st.subheader("🎯 Analizador de Escenarios de Negocio")
    
    # Opciones de escenario
    scenario_types = [
        "Lanzamiento de Nuevo Producto",
        "Segmentación de Clientes", 
        "Expansión de Portafolio",
        "Estrategia de Abastecimiento",
        "Inversión Comercial"
    ]
    
    selected_scenario = st.selectbox("Seleccionar tipo de escenario:", scenario_types)
    
    # Parámetros del escenario
    st.subheader("Parámetros del Escenario")
    
    with st.expander("Crear Clientes de Prueba"):
        n_customers = st.slider("Número de clientes:", 10, 500, 100)
        
        col1, col2 = st.columns(2)
        with col1:
            min_age = st.number_input("Edad mínima:", min_value=18, max_value=80, value=25, step=1)
            max_age = st.number_input("Edad máxima:", min_value=18, max_value=80, value=45, step=1)
            
        with col2:
            min_income = st.number_input("Ingreso mínimo (COP):", min_value=1000000, max_value=50000000, value=3000000, step=100000)
            max_income = st.number_input("Ingreso máximo (COP):", min_value=1000000, max_value=100000000, value=8000000, step=100000)
        
        if st.button("Generar clientes de prueba"):
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
            with st.spinner("Analizando escenario..."):
                scenario_results = st.session_state.ai_model.analyze_scenario(test_customers)
            
            # Mostrar resultados
            st.subheader("📈 Resultados del Análisis")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Clientes", scenario_results['total_customers'])
            with col2:
                st.metric("Impacto Promedio", format_cop(scenario_results['avg_impact']))
            with col3:
                st.metric("Impacto Total", format_cop(scenario_results['total_impact']))
            
            # Distribución de segmentos
            st.subheader("🎯 Distribución de Segmentos en el Escenario")
            segment_dist = scenario_results['segment_distribution']
            segment_labels = [st.session_state.data_generator.get_segment_description(seg) for seg in segment_dist.keys()]
            
            fig_segment = px.pie(
                values=list(segment_dist.values()),
                names=segment_labels,
                title="Distribución de Segmentos"
            )
            st.plotly_chart(fig_segment, use_container_width=True)
            
            # Recomendaciones detalladas
            st.subheader("💡 **RECOMENDACIONES ESTRATÉGICAS DETALLADAS**")
            recommendations = generate_recommendations(scenario_results, selected_scenario, test_customers)
            
            # Mostrar recomendaciones con formato
            for i, rec in enumerate(recommendations):
                if rec.startswith("🎯 **") or rec.startswith("💰 **") or rec.startswith("📊 **"):
                    st.markdown(f"### {rec}")
                elif rec.startswith("  •"):
                    st.markdown(f"**{rec}**")
                elif rec.startswith("  🏆") or rec.startswith("  💎") or rec.startswith("  🤝") or rec.startswith("  📱"):
                    st.markdown(f"> {rec}")
                elif rec == "":
                    st.markdown("")
                else:
                    st.write(rec)

def generate_recommendations(scenario_results, scenario_type, test_customers):
    """Genera recomendaciones estratégicas detalladas basadas en el análisis"""
    recommendations = []
    
    segment_dist = scenario_results['segment_distribution']
    avg_impact = scenario_results['avg_impact']
    total_customers = scenario_results['total_customers']
    
    # --- ANÁLISIS DE SEGMENTOS DOMINANTES ---
    dominant_segment = max(segment_dist, key=segment_dist.get)
    segment_name = st.session_state.data_generator.get_segment_description(dominant_segment)
    segment_percentage = (segment_dist[dominant_segment] / total_customers) * 100
    
    # --- ANÁLISIS DE COMPORTAMIENTO POR SEGMENTO ---
    segment_analysis = {}
    for customer in test_customers:
        segment = st.session_state.ai_model.predict_segment(customer)
        if segment not in segment_analysis:
            segment_analysis[segment] = {
                'count': 0,
                'total_income': 0,
                'total_purchase': 0,
                'avg_age': 0,
                'avg_loyalty': 0
            }
        segment_analysis[segment]['count'] += 1
        segment_analysis[segment]['total_income'] += customer['ingreso_mensual']
        segment_analysis[segment]['total_purchase'] += customer['valor_promedio_compra']
        segment_analysis[segment]['avg_age'] += customer['edad']
        segment_analysis[segment]['avg_loyalty'] += customer['lealtad_marca']
    
    # Calcular promedios
    for segment in segment_analysis:
        count = segment_analysis[segment]['count']
        segment_analysis[segment]['avg_income'] = segment_analysis[segment]['total_income'] / count
        segment_analysis[segment]['avg_purchase'] = segment_analysis[segment]['total_purchase'] / count
        segment_analysis[segment]['avg_age'] = segment_analysis[segment]['avg_age'] / count
        segment_analysis[segment]['avg_loyalty'] = segment_analysis[segment]['avg_loyalty'] / count
    
    # --- RECOMENDACIONES GENERALES ---
    recommendations.append(f"🎯 **SEGMENTO DOMINANTE**: {segment_name} ({segment_percentage:.1f}% del total)")
    
    # Recomendación basada en impacto
    if avg_impact > 5000000:  # 5 millones COP
        recommendations.append("💰 **IMPACTO ALTO**: El escenario muestra un impacto potencial significativo. Considerar implementación gradual con monitoreo constante.")
    elif avg_impact > 2000000:  # 2 millones COP
        recommendations.append("📊 **IMPACTO MODERADO**: El escenario tiene un impacto viable. Requiere seguimiento periódico y ajustes basados en resultados.")
    else:
        recommendations.append("⚠️ **IMPACTO BAJO**: El escenario tiene un impacto limitado. Evaluar si justifica la inversión o buscar alternativas más rentables.")
    
    # --- RECOMENDACIONES ESPECÍFICAS POR TIPO DE ESCENARIO ---
    if "Lanzamiento" in scenario_type:
        recommendations.extend([
            "🚀 **LANZAMIENTO DE PRODUCTO**:",
            "  • Priorizar segmentos con alta lealtad y capacidad de compra",
            "  • Considerar estrategia de penetración de mercado con precios competitivos",
            "  • Planear campaña de marketing dirigida al segmento dominante",
            "  • Establecer indicadores clave de desempeño (KPI) para medir éxito",
            "  • Preparar plan de contingencia para escenarios de bajo rendimiento"
        ])
        
    elif "Segmentación" in scenario_type:
        recommendations.extend([
            "🎯 **SEGMENTACIÓN DE CLIENTES**:",
            "  • Personalizar ofertas según características demográficas y de comportamiento",
            "  • Desarrollar programas de fidelización específicos para cada segmento",
            "  • Optimizar canales de comunicación según preferencias del segmento dominante",
            "  • Implementar estrategia de pricing diferencial por segmento",
            "  • Crear métricas de satisfacción por grupo demográfico"
        ])
        
    elif "Expansión" in scenario_type:
        recommendations.extend([
            "📈 **EXPANSIÓN DE PORTAFOLIO**:",
            "  • Identificar segmentos con mayor potencial de crecimiento",
            "  • Evaluar barreras de entrada y competencia en nuevos mercados",
            "  • Desarrollar estrategia de posicionamiento diferencial",
            "  • Considerar alianzas estratégicas con empresas complementarias",
            "  • Planear escalabilidad del sistema para manejar mayor demanda"
        ])
        
    elif "Abastecimiento" in scenario_type:
        recommendations.extend([
            "📦 **ESTRATEGIA DE ABASTECIMIENTO**:",
            "  • Optimizar cadenas de suministro basado en comportamiento por segmento",
            "  • Diversificar proveedores para reducir riesgos operativos",
            "  • Implementar sistema de inventario predictivo según demanda",
            "  • Negociar condiciones comerciales específicas con proveedores clave",
            "  • Establecer indicadores de desempeño logístico (KPIs)"
        ])
        
    elif "Inversión" in scenario_type:
        recommendations.extend([
            "💼 **INVERSIÓN COMERCIAL**:",
            "  • Evaluar ROI por segmento y priorizar inversiones con mayor retorno",
            "  • Considerar horizonte temporal de recuperación de inversión",
            "  • Analizar sensibilidad del escenario a variables macroeconómicas",
            "  • Diversificar portafolio de inversiones para mitigar riesgos",
            "  • Establecer puntos de control y evaluación periódica"
        ])
    
    # --- ANÁLISIS DE SEGMENTOS DETALLADO ---
    recommendations.append("\n📊 **ANÁLISIS DETALLADO POR SEGMENTO**:")
    
    # Ordenar segmentos por impacto en el escenario
    sorted_segments = sorted(segment_analysis.items(), 
                           key=lambda x: x[1]['avg_income'], reverse=True)
    
    for segment_id, analysis in sorted_segments:
        segment_name = st.session_state.data_generator.get_segment_description(segment_id)
        avg_income = analysis['avg_income']
        avg_purchase = analysis['avg_purchase']
        avg_age = int(analysis['avg_age'])
        avg_loyalty = analysis['avg_loyalty']
        segment_count = analysis['count']
        
        recommendations.append(f"  • **{segment_name}** ({segment_count} clientes):")
        recommendations.append(f"    - Edad promedio: {avg_age} años")
        recommendations.append(f"    - Ingreso mensual: ${avg_income:,.0f} COP")
        recommendations.append(f"    - Valor promedio de compra: ${avg_purchase:,.0f} COP")
        recommendations.append(f"    - Lealtad a marca: {avg_loyalty:.1f}%")
        
        # Recomendación específica para este segmento
        if segment_id == dominant_segment:
            recommendations.append(f"    🏆 **SEGMENTO PRIORITARIO** - Enfocar esfuerzos principales aquí")
        elif avg_income > 4000000:
            recommendations.append(f"    💎 **ALTA CAPACIDAD ADQUISITIVA** - Ofrecer productos premium")
        elif avg_loyalty > 60:
            recommendations.append(f"    🤝 **ALTA LEALTAD** - Implementar programas de fidelización")
        elif avg_age < 30:
            recommendations.append(f"    📱 **JÓVENES DIGITALES** - Enfocar estrategia digital")
        else:
            recommendations.append(f"    🎯 **OPORTUNIDAD DE CRECIMIENTO** - Desarrollar estrategias específicas")
    
    # --- RECOMENDACIONES ESTRATÉGICAS FINALES ---
    recommendations.append("\n🎯 **RECOMENDACIONES ESTRATÉGICAS FINALES**:")
    
    # Análisis de riesgo
    if avg_impact > 8000000:
        recommendations.append("  ⚠️ **RIESGO ALTO**: Considerar implementación piloto antes de despliegue completo")
    elif avg_impact > 3000000:
        recommendations.append("  📊 **RIESGO MODERADO**: Monitoreo constante con ajustes basados en resultados")
    else:
        recommendations.append("  ✅ **RIESGO BAJO**: Implementación directa con controles básicos")
    
    # Recomendación de escalabilidad
    if total_customers > 200:
        recommendations.append("  🚀 **ESCALABILIDAD**: El escenario permite expansión a mayor escala")
    elif total_customers > 100:
        recommendations.append("  📈 **CRECIMIENTO**: Potencial de expansión con optimización")
    else:
        recommendations.append("  🎯 **ENFOQUE**: Priorizar calidad sobre cantidad en implementación")
    
    # Recomendación temporal
    if "Lanzamiento" in scenario_type or "Expansión" in scenario_type:
        recommendations.append("  ⏰ **HORIZONTE TEMPORAL**: Implementación a 3-6 meses con evaluación trimestral")
    elif "Inversión" in scenario_type:
        recommendations.append("  💰 **HORIZONTE TEMPORAL**: Evaluación a 12 meses con revisiones semestrales")
    else:
        recommendations.append("  📊 **HORIZONTE TEMPORAL**: Monitoreo continuo con evaluaciones mensuales")
    
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
    
    # Barra lateral con navegación
    st.sidebar.title("🔧 Menú de Navegación")
    page = st.sidebar.selectbox(
        "Seleccionar página:",
        ["Dashboard Principal", "Datos de Clientes", "Modelos de IA", "Análisis de Escenarios"]
    )
    
    if page == "Dashboard Principal":
        st.header("📊 Dashboard Principal")
        
        # Resumen del proyecto
        st.subheader("🎯 Resumen del Proyecto")
        st.markdown("""
        **Prototipo de IA para Soporte en Toma de Decisiones Estratégicas**
        
        Este prototipo permite analizar diferentes escenarios de negocio y recomendar alternativas estratégicas basadas en evidencia analítica.
        """)
        
        # Estado del sistema
        st.subheader("📈 Estado del Sistema")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.session_state.customer_data is not None:
                st.metric("✅ Datos Generados", "Sí")
            else:
                st.metric("❌ Datos Generados", "No")
                
        with col2:
            if st.session_state.model_metrics is not None:
                st.metric("✅ Modelos Entrenados", "Sí")
            else:
                st.metric("❌ Modelos Entrenados", "No")
                
        with col3:
            if st.session_state.ai_model.is_trained:
                st.metric("✅ Sistema Activo", "Sí")
            else:
                st.metric("❌ Sistema Activo", "No")
        
        # Botones de acción rápidos
        st.subheader("🚀 Acciones Rápidas")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Generar Datos", type="primary"):
                generate_sample_data()
                
        with col2:
            if st.button("Entrenar Modelos", type="secondary"):
                train_models()
                
    elif page == "Datos de Clientes":
        st.header("📊 Datos de Clientes")
        show_data_overview()
            
    elif page == "Modelos de IA":
        st.header("🤖 Modelos de IA")
        show_model_performance()
            
    elif page == "Análisis de Escenarios":
        st.header("🎯 Análisis de Escenarios")
        create_scenario_analyzer()

if __name__ == "__main__":
    main()
