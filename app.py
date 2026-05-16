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
        self.data_generator = DataGenerator()
        self.ai_model = AIModel()
        self.customer_data = None
        self.model_metrics = None
        
    def setup_page(self):
        """Configuración inicial de la página"""
        st.set_page_config(
            page_title="Prototipo IA para Toma de Decisiones",
            page_icon="🤖",
            layout="wide"
        )
        
        st.title("🤖 Prototipo IA para Soporte en Toma de Decisiones Estratégicas")
        st.markdown("---")
        
    def generate_sample_data(self):
        """Genera datos de muestra para el prototipo"""
        with st.spinner("Generando datos de clientes..."):
            self.customer_data = self.data_generator.generate_synthetic_data(1000)
            st.success(f"✅ Datos generados: {len(self.customer_data)} clientes")
            
    def train_models(self):
        """Entrena los modelos de IA"""
        if self.customer_data is None:
            st.error("❌ Primero genere los datos de clientes")
            return
            
        with st.spinner("Entrenando modelos de IA..."):
            # Entrenar modelo de segmentación
            segment_metrics = self.ai_model.train_segmentation_model(self.customer_data)
            
            # Entrenar modelo de impacto
            impact_metrics = self.ai_model.train_impact_model(self.customer_data)
            
            self.model_metrics = {
                'segmentation': segment_metrics,
                'impact': impact_metrics
            }
            
            self.ai_model.is_trained = True
            st.success("✅ Modelos de IA entrenados exitosamente")
            
    def show_data_overview(self):
        """Muestra overview de los datos"""
        if self.customer_data is None:
            return
            
        st.subheader("📊 Vista General de Datos de Clientes")
        
        # Métricas básicas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Clientes", len(self.customer_data))
            
        with col2:
            st.metric("Edad Promedio", f"{self.customer_data['edad'].mean():.1f} años")
            
        with col3:
            st.metric("Ingreso Promedio", f"${self.customer_data['ingreso_mensual'].mean():,.0f}")
            
        with col4:
            st.metric("Valor Promedio Compra", f"${self.customer_data['valor_promedio_compra'].mean():,.2f}")
        
        # Distribución de segmentos
        st.subheader("🎯 Distribución de Segmentos de Clientes")
        segment_counts = self.customer_data['segmento_cliente'].value_counts()
        segment_labels = [self.data_generator.get_segment_description(seg) for seg in segment_counts.index]
        
        fig_pie = px.pie(
            values=segment_counts.values,
            names=segment_labels,
            title="Distribución de Segmentos"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Estadísticas por segmento
        st.subheader("📈 Estadísticas por Segmento")
        segment_stats = self.customer_data.groupby('segmento_cliente').agg({
            'edad': 'mean',
            'ingreso_mensual': 'mean',
            'valor_promedio_compra': 'mean',
            'lealtad_marca': 'mean'
        }).round(2)
        
        segment_stats.index = [self.data_generator.get_segment_description(seg) for seg in segment_stats.index]
        st.dataframe(segment_stats)
        
    def show_model_performance(self):
        """Muestra el rendimiento de los modelos"""
        if self.model_metrics is None:
            return
            
        st.subheader("📊 Rendimiento de Modelos de IA")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Modelo de Segmentación")
            metrics = self.model_metrics['segmentation']
            
            st.metric("Precisión", f"{metrics['accuracy']:.3f}")
            st.metric("Validación Cruzada", f"{metrics['cv_mean']:.3f} ± {metrics['cv_std']:.3f}")
            
            # Reporte de clasificación
            st.write("Reporte de Clasificación:")
            report_df = pd.DataFrame(metrics['classification_report']).transpose()
            st.dataframe(report_df)
            
        with col2:
            st.subheader("Modelo de Impacto")
            metrics = self.model_metrics['impact']
            
            st.metric("RMSE", f"{metrics['rmse']:.2f}")
            st.metric("R² Score", f"{metrics['r2_score']:.3f}")
            
            # Gráfico de dispersión
            y_true = self.customer_data['valor_promedio_compra'].values
            X, _ = self.ai_model.prepare_data(self.customer_data)
            y_pred = self.ai_model.impact_model.predict(X)
            
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
                xaxis_title='Valor Real',
                yaxis_title='Predicción'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def create_scenario_analyzer(self):
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
                min_age = st.number_input("Edad mínima:", 18, 80, 25)
                max_age = st.number_input("Edad máxima:", 18, 80, 45)
                
            with col2:
                min_income = st.number_input("Ingreso mínimo ($):", 1000, 50000, 30000)
                max_income = st.number_input("Ingreso máximo ($):", 1000, 50000, 80000)
            
            if st.button("Generar clientes de prueba"):
                test_customers = []
                for i in range(n_customers):
                    customer = {
                        'edad': np.random.uniform(min_age, max_age),
                        'ingreso_mensual': np.random.uniform(min_income, max_income),
                        'educacion': np.random.choice(['Primaria', 'Secundaria', 'Universidad', 'Posgrado']),
                        'frecuencia_compra': np.random.poisson(3),
                        'valor_promedio_compra': np.random.exponential(50) + 10,
                        'lealtad_marca': np.random.beta(2, 2) * 100,
                        'crecimiento_mercado': np.random.uniform(0.05, 0.15),
                        'nivel_competencia': np.random.uniform(1, 10)
                    }
                    test_customers.append(customer)
                
                # Analizar escenario
                with st.spinner("Analizando escenario..."):
                    scenario_results = self.ai_model.analyze_scenario(test_customers)
                
                # Mostrar resultados
                st.subheader("📈 Resultados del Análisis")
                
                col1, col2, col3 = st.columns
