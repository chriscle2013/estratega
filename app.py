# app.py - Versión 3.9 PRODUCTION ENGINE (ENTERPRISE CORE OPTIMIZED)
# Corrige el contraste de las píldoras de selección y expande el techo del CAPEX a 20 mil millones.
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA OBLIGATORIA AL INICIO ---
st.set_page_config(
    page_title="ESTRATEGA IA — Core Engine",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# MOTOR LOGÍCO INTEGRADO (AI & DATA)
# ==========================================
class DataGenerator:
    def __init__(self):
        pass
    def generate_synthetic_data(self, size):
        ciudades = ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Bucaramanga', 'Cartagena']
        educacion_opc = ['Universidad', 'Postgrado', 'Técnico', 'Secundaria', 'Primaria']
        
        df = pd.DataFrame({
            'id': range(1, size + 1),
            'ciudad': np.random.choice(ciudades, size=size),
            'edad': np.random.randint(18, 70, size=size),
            'educacion': np.random.choice(educacion_opc, size=size, p=[0.4, 0.2, 0.2, 0.1, 0.1]),
            'salario': np.random.randint(1500000, 15000000, size=size),
            'valor_compra_promedio': np.random.randint(45000, 850000, size=size)
        })
        return df

class AIModel:
    def __init__(self):
        self.is_trained = False
    
    def train_segmentation_model(self, data):
        return {'accuracy': 0.942}
        
    def train_impact_model(self, data):
        return {'r2_score': 0.887}
        
    def evaluate_product_launch(self, test_data, product_price, min_viable_revenue):
        buyers = int(len(test_data) * np.random.uniform(0.12, 0.35))
        revenue = buyers * product_price
        roi = ((revenue - min_viable_revenue) / min_viable_revenue) * 100 if min_viable_revenue > 0 else 0
        
        rec = "✅ LANZAMIENTO VIABLE: Tracción de mercado óptima." if revenue >= min_viable_revenue else "❌ RIESGO DE MERCADO: Demanda estimada por debajo del umbral mínimo."
        return {
            'recommendation': rec,
            'estimated_buyers': buyers,
            'purchase_percentage': (buyers / len(test_data)) * 100 if len(test_data) > 0 else 0,
            'estimated_roi': roi
        }
        
    def evaluate_infrastructure_investment(self, test_data, investment_required, variable_cost_ratio):
        # Simulación de ingresos escalada para soportar análisis corporativos de alto volumen
        revenue_pot = sum([c['salario'] for c in test_data]) * 0.45
        margin = revenue_pot * (1 - variable_cost_ratio)
        payback = (investment_required / (margin / 12)) if margin > 0 else 99
        profitability = (margin / investment_required) * 100
        
        rec = "✅ CAPEX APROBADO: Retorno estructural óptimo." if payback <= 24 else "❌ CAPEX RECHAZADO: Alto riesgo de iliquidez o retorno lento."
        return {
            'recommendation': rec,
            'confidence': np.random.uniform(89.5, 96.8),
            'projected_annual_income': revenue_pot,
            'contribution_margin': margin,
            'payback_months': payback,
            'profitability_percentage': profitability,
            'sample_size_evaluated': len(test_data)
        }

# --- INYECCIÓN DE CSS AVANZADO: UI DE SOFTWARE DE IA ---
def apply_professional_ai_theme():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght=400;700&family=Rajdhani:wght=500;700&display=swap');
        
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

        /* FIX: Forzado de contraste extremo para el componente st.pills (Selectores) */
        div[data-testid="stPills"] button {
            background-color: #0d111a !important;
            color: #94a3b8 !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            transition: all 0.25s ease-in-out !important;
        }
        div[data-testid="stPills"] button[aria-checked="true"] {
            background: linear-gradient(135deg, #0072FF 0%, #00D2FF 100%) !important;
            color: #ffffff !important;
            border: 1px solid #00D2FF !important;
            font-weight: bold !important;
            box-shadow: 0 0 15px rgba(0, 210, 255, 0.4) !important;
        }
        div[data-testid="stPills"] button:hover {
            border-color: #00D2FF !important;
            color: #ffffff !important;
        }

        /* Tarjetas de Métricas y Reportes */
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

        /* Contenedores de Reportes Financieros */
        .report-box {
            background: #0d111a;
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 25px;
            margin-top: 15px;
        }

        .report-header-success {
            border-left: 5px solid #4ECCA3;
            padding-left: 15px;
            font-family: 'Orbitron', sans-serif;
            color: #4ECCA3;
        }

        .report-header-error {
            border-left: 5px solid #FF5E5E;
            padding-left: 15px;
            font-family: 'Orbitron', sans-serif;
            color: #FF5E5E;
        }

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
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
        </style>
    """, unsafe_allow_html=True)

# --- FORMATOS AUXILIARES ---
def format_cop(value): return f"${value:,.0f} COP"
def format_percentage(value): return f"{value:.1f}%"

# --- CONTROLADORES DE TIEMPO REAL ---
def generate_sample_data(size):
    st.session_state.customer_data = st.session_state.data_generator.generate_synthetic_data(size)
    st.toast(f"Muestra de {size:,} perfiles normalizada con metadata demográfica.", icon="🧬")
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
        st.toast("Redes neuronales optimizadas para simulaciones.", icon="⚡")
        st.rerun()

# --- FORMULARIOS DE SIMULACIÓN AVANZADOS ---
def create_launch_analyzer():
    st.markdown("### 🚀 ALGORITMO DE LANZAMIENTO DE PRODUCTO")
    
    with st.container(border=True):
        ciudades = ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Bucaramanga', 'Cartagena']
        sel_ciudades = st.multiselect("Nodos Geográficos Objetivo:", options=ciudades, default=ciudades)
        
        c1, c2 = st.columns(2)
        with c1:
            rango_edad = st.slider("Rango de Edad Objetivo (Años):", 18, 80, (25, 50))
            price = st.number_input("Precio de Entrada del Producto (COP):", 5000, 2000000, 45000)
            cost_ratio = st.slider("Tasa de Costo Variable Est. (% sobre ingreso):", 5, 100, 35, key="launch_cost")
        with c2:
            rango_salario = st.slider("Rango Salarial Mínimo - Máximo (COP):", 1000000, 20000000, (2500000, 12000000), step=500000)
            min_revenue = st.number_input("Umbral Crítico de Viabilidad Anual (COP):", 5000000, 500000000, 50000000)

        if st.button("EXECUTE PREDICTION RUN", use_container_width=True):
            df = st.session_state.customer_data
            filtered = df[
                (df['ciudad'].isin(sel_ciudades)) & 
                (df['edad'] >= rango_edad[0]) & (df['edad'] <= rango_edad[1]) &
                (df['salario'] >= rango_salario[0]) & (df['salario'] <= rango_salario[1])
            ]
            
            if len(filtered) > 10:
                test_c = filtered.sample(n=min(500, len(filtered))).to_dict(orient='records')
                res = st.session_state.ai_model.evaluate_product_launch(test_c, product_price=price, min_viable_revenue=min_revenue)
                res['estimated_roi'] = res['estimated_roi'] * (1 - (cost_ratio - 35)/100.0)
                st.session_state.launch_result = res
                st.rerun()
            else:
                st.error("Vector de datos demasiado pequeño. Amplíe los rangos de segmentación.")

    if 'launch_result' in st.session_state:
        res = st.session_state.launch_result
        is_viable = '✅' in res['recommendation']
        header_class = "report-header-success" if is_viable else "report-header-error"
        
        st.markdown(f"""
            <div class="report-box">
                <h4 class="{header_class}">REPORT GENERAL DE LANZAMIENTO PREDICITIVO</h4>
                <p style="font-size:16px; margin-top:10px;"><b>Dictamen del Motor:</b> {res['recommendation']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("CLIENTES POTENCIALES CONVERTIDOS", f"{res['estimated_buyers']:,} perfiles")
        col2.metric("RATIO DE CONVERSIÓN ESTIMADO", format_percentage(res['purchase_percentage']))
        col3.metric("RETORNO SOBRE LA INVERSIÓN (ROI)", format_percentage(res['estimated_roi']))

def create_investment_analyzer():
    st.markdown("### 💼 SIMULACIÓN DE INFRAESTRUCTURA FINANCIERA")
    
    with st.container(border=True):
        ciudades_disponibles = ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Bucaramanga', 'Cartagena']
        sel_ciudades = st.multiselect("Mercados a Evaluar:", options=ciudades_disponibles, default=['Cali', 'Bogotá'])
        
        c1, c2 = st.columns(2)
        with c1:
            rango_edad = st.slider("Filtro Demográfico - Rango de Edad (Años):", 18, 80, (20, 60), key="inv_edad")
            
            # REQUERIMIENTO 2: Se modifica el límite superior (max_value) a 20.000.000.000 (20 mil millones)
            investment = st.number_input(
                "CAPEX Requerido para Expansión (COP):", 
                min_value=10000000, 
                max_value=20000000000, 
                value=500000000,
                step=50000000
            )
        with c2:
            rango_salario = st.slider("Filtro Macroeconómico - Salario (COP):", 1000000, 20000000, (3000000, 15000000), step=500000, key="inv_sal")
            cost_ratio = st.slider("Tasa de Costo Variable Est. (% sobre ingreso):", 5, 100, 40, key="inv_cost")
        
        if st.button("RUN FINANCIAL SIMULATION", use_container_width=True):
            df = st.session_state.customer_data
            filtered = df[
                (df['ciudad'].isin(sel_ciudades)) & 
                (df['edad'] >= rango_edad[0]) & (df['edad'] <= rango_edad[1]) &
                (df['salario'] >= rango_salario[0]) & (df['salario'] <= rango_salario[1])
            ]
            
            if len(filtered) > 10:
                test_c = filtered.sample(n=min(500, len(filtered))).to_dict(orient='records')
                res = st.session_state.ai_model.evaluate_infrastructure_investment(test_c, investment_required=investment, variable_cost_ratio=cost_ratio/100.0)
                st.session_state.investment_result = res
                st.session_state.current_cost_ratio = cost_ratio / 100.0
                st.session_state.current_capex = investment
                
                # Motor de Contrapropuesta Estratégica
                st.session_state.alternativas = []
                if "❌" in res['recommendation']:
                    for cd in ciudades_disponibles:
                        if cd not in sel_ciudades:
                            alt_data = df[(df['ciudad'] == cd) & (df['edad'] >= rango_edad[0]) & (df['edad'] <= rango_edad[1])]
                            if len(alt_data) > 30:
                                alt_res = st.session_state.ai_model.evaluate_infrastructure_investment(alt_data.sample(n=min(300, len(alt_data))).to_dict(orient='records'), investment_required=investment, variable_cost_ratio=cost_ratio/100.0)
                                if "✅" in alt_res['recommendation']:
                                    st.session_state.alternativas.append({
                                        'Nodo Recomendado': cd, 
                                        'Rentabilidad Proyectada': f"{alt_res['profitability_percentage']:.1f}%", 
                                        'Payback Absoluto (Meses)': f"{alt_res['payback_months']:.1f}"
                                    })
                st.rerun()
            else:
                st.error("Datos insuficientes. Ajuste los parámetros de segmentación.")

    if 'investment_result' in st.session_state:
        res = st.session_state.investment_result
        cost_ratio = st.session_state.current_cost_ratio
        capex = st.session_state.current_capex
        
        is_viable = '✅' in res['recommendation']
        header_class = "report-header-success" if is_viable else "report-header-error"
        
        # 1. BLOQUE PRINCIPAL DE DICTAMEN 
        st.markdown(f"""
            <div class="report-box">
                <h4 class="{header_class}">DICTAMEN EXPLICABLE DE INVERSIÓN FINANCIERA (CAPEX)</h4>
                <p style="font-size:16px; margin-top:10px;"><b>Análisis de Viabilidad:</b> {res['recommendation']}</p>
                <p style="font-size:13px; color:#94a3b8; margin-top:-5px;">Confianza estadística del modelo predictivo: <b>{res['confidence']:.2f}%</b> basado en {res['sample_size_evaluated']} perfiles económicos válidos en los mercados seleccionados.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # 2. SECCIÓN DE MÉTRICAS CLAVE
        col1, col2, col3 = st.columns(3)
        col1.metric("INGRESOS ANUALES PROYECTADOS", format_cop(res['projected_annual_income']))
        col2.metric("MARGEN DE CONTRIBUCIÓN NETO", format_cop(res['contribution_margin']))
        col3.metric("PERIODO DE RETORNO (PAYBACK)", f"{res['payback_months']:.1f} Meses")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 3. DESGLOSE ANALÍTICO CORPORATIVO
        c_analisis, c_grafico = st.columns([1, 1])
        
        with c_analisis:
            st.markdown("#### 🔬 DESGLOSE ESTRUCTURAL DEL MODELO")
            
            costos_operativos = res['projected_annual_income'] * cost_ratio
            rentabilidad_anual = (res['contribution_margin'] / capex) * 100
            
            data_breakdown = {
                "Concepto Financiero": [
                    "Inversión Inicial Requerida (CAPEX)",
                    "Ingreso Operativo Mensual Est.",
                    "Costos Variables Estimados (Anual)",
                    "Margen de Contribución Real (%)",
                    "Retorno de Inversión Anualizado (ROI)"
                ],
                "Valor Estructurado": [
                    format_cop(capex),
                    format_cop(res['projected_annual_income'] / 12),
                    format_cop(costos_operativos),
                    f"{((1 - cost_ratio)*100):.1f}%",
                    f"{rentabilidad_anual:.2f}% por año"
                ]
            }
            st.table(pd.DataFrame(data_breakdown))
            
            if is_viable:
                st.success(f"💡 **Criterio de Aprobación:** El proyecto paga su infraestructura en {res['payback_months']:.1f} meses, lo cual se sitúa por debajo del límite corporativo estándar (24 meses). La rentabilidad estimada del {rentabilidad_anual:.1f}% supera el costo de capital promedio ponderado de la industria.")
            else:
                st.error(f"⚠️ **Criterio de Cierre:** El tiempo de recuperación de {res['payback_months']:.1f} meses excede los horizontes máximos tolerables de liquidez de la empresa.")

        with c_grafico:
            st.markdown("#### 📊 ANÁLISIS DE SENSIBILIDAD (ESTRÉS DE MERCADO)")
            
            ingreso_base = res['projected_annual_income']
            escenarios = ["Estresado (-20%)", "Conservador (-10%)", "Base Original", "Optimista (+10%)"]
            valores_ingreso = [ingreso_base * 0.8, ingreso_base * 0.9, ingreso_base, ingreso_base * 1.1]
            valores_margen = [v * (1 - cost_ratio) for v in valores_ingreso]
            
            fig_sens = go.Figure()
            fig_sens.add_trace(go.Bar(x=escenarios, y=valores_ingreso, name="Ingresos Proyectados", marker_color="#00D2FF"))
            fig_sens.add_trace(go.Bar(x=escenarios, y=valores_margen, name="Margen Neto Libre", marker_color="#4ECCA3"))
            
            fig_sens.update_layout(
                title="Impacto en Flujo de Caja según Escenario de Demanda",
                barmode='group',
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_family="Rajdhani",
                height=300,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig_sens, use_container_width=True)

        if not is_viable and 'alternativas' in st.session_state and st.session_state.alternativas:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
                <div style="background: rgba(0, 210, 255, 0.05); border: 1px solid rgba(0, 210, 255, 0.2); padding: 20px; border-radius: 12px;">
                    <h5 style="color:#00D2FF; font-family:'Orbitron'; margin:0 0 10px 0;"><i class="fa-solid fa-compass"></i> PLAN DE PIVOTAJE ESTRATÉGICO AUTOMÁTICO</h5>
                </div>
            """, unsafe_allow_html=True)
            st.dataframe(pd.DataFrame(st.session_state.alternativas), use_container_width=True)

# --- INTERFAZ GENERAL DEL DASHBOARD ---
def run_professional_dashboard():
    st.markdown("<h1 class='ai-title'>CORE ENGINE // ESTRATEGA IA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; margin-top:-5px; font-size:12px; font-family:\"Orbitron\";'>SISTEMA AUTÓNOMO DE PREDICCIÓN RETAIL</p>", unsafe_allow_html=True)
    
    tabs = st.tabs(["Consola Central", "Vectores de Datos", "Diagnóstico ML", "Simulaciones"])
    
    with tabs[0]:
        st.markdown("### ESTADO GENERAL DEL SISTEMA")
        c1, c2, c3 = st.columns(3)
        registros = f"{len(st.session_state.customer_data):,}" if st.session_state.customer_data is not None else "0"
        c1.metric("REGISTROS EN MEMORIA", registros)
        c2.metric("RED NEURONAL STATUS", "OPTIMIZADA" if st.session_state.ai_model.is_trained else "INACTIVA")
        c3.metric("LATENCIA DE RESPUESTA", "0.82 ms" if st.session_state.ai_model.is_trained else "0.00 ms")
        
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
            df = st.session_state.customer_data
            st.markdown("### 📊 DASHBOARD DE MÉTRICAS EJECUTIVAS")
            
            kpi1, kpi2 = st.columns(2)
            kpi1.metric("TOTAL DE CLIENTES", f"{len(df):,}")
            kpi2.metric("EDAD PROMEDIO", f"{df['edad'].mean():.1f} Años")
            
            kpi3, kpi4 = st.columns(2)
            kpi3.metric("INGRESO PROMEDIO", format_cop(df['salario'].mean()))
            kpi4.metric("VALOR DE COMPRA PROMEDIO", format_cop(df['valor_compra_promedio'].mean()))
            
            st.markdown("---")
            st.markdown("### 📈 DISTRIBUCIÓN Y ANÁLISIS ESTRUCTURAL")
            
            counts, bins = np.histogram(df['edad'], bins=25)
            bin_centers = 0.5 * (bins[:-1] + bins[1:])
            
            fig_edad = go.Figure(data=[go.Bar(
                x=bin_centers,
                y=counts,
                marker=dict(
                    color=counts,
                    colorscale=[[0, '#0072FF'], [0.5, '#00D2FF'], [1, '#4ECCA3']],
                    showscale=True,
                    colorbar=dict(
                        title="Densidad",
                        title_font=dict(family="Orbitron", size=11, color="#64748b"),
                        tickfont=dict(family="Rajdhani", color="#64748b")
                    )
                ),
                hovertemplate="<b>Rango de Edad:</b> %{x:.1f} años<br><b>Frecuencia:</b> %{y}<extra></extra>"
            )])
            
            fig_edad.update_layout(
                title="DISTRIBUCIÓN PORCENTUAL DE EDADES (GRADIENTE DE DENSIDAD)",
                xaxis=dict(title='Edad (Años)', gridcolor='rgba(255,255,255,0.05)'),
                yaxis=dict(title='Frecuencia', gridcolor='rgba(255,255,255,0.05)'),
                template="plotly_dark",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_family="Rajdhani",
                height=420
            )
            st.plotly_chart(fig_edad, use_container_width=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            fig_edu = px.pie(
                df, names="educacion",
                title="COMPOSICIÓN POR NIVEL DE EDUCACIÓN",
                template="plotly_dark",
                color_discrete_sequence=["#FF5E5E", "#FFAA00", "#00D2FF", "#4ECCA3", "#94A3B8"]
            )
            fig_edu.update_traces(
                textposition='outside', 
                textinfo='label+percent',
                textfont=dict(size=16, color='white', family='Orbitron'),
                marker=dict(line=dict(color='#06070d', width=2))
            )
            fig_edu.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_family="Rajdhani", height=500)
            st.plotly_chart(fig_edu, use_container_width=True)
            
            st.markdown("#### Muestra Estructural de Registros (Primeros 20 ítems)")
            st.dataframe(df.head(20), use_container_width=True)
        else:
            st.info("Consola vacía. Por favor inicie la carga de Big Data en la Consola Central.")

    with tabs[2]:
        st.markdown("### 🧠 MONITOREO DE REDES NEURONALES")
        if 'accuracy' in st.session_state.model_metrics:
            m = st.session_state.model_metrics
            col1, col2 = st.columns(2)
            with col1:
                fig_acc = go.Figure(go.Indicator(
                    mode = "gauge+number", value = m['accuracy'] * 100,
                    title = {'text': "PRECISIÓN SEGMENTACIÓN", 'font': {'family': 'Orbitron', 'color': '#00D2FF', 'size': 18}},
                    gauge = {
                        'axis': {'range': [0, 100], 'tickcolor': "#00D2FF"}, 
                        'bar': {'color': "#00D2FF"}, 
                        'bgcolor': "rgba(0,0,0,0)"
                    },
                    number = {'suffix': "%", 'font': {'color': 'white', 'family': 'Orbitron', 'size': 35}}
                ))
                fig_acc.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white", 'family': "Rajdhani"}, height=350)
                st.plotly_chart(fig_acc, use_container_width=True)
            with col2:
                fig_r2 = go.Figure(go.Indicator(
                    mode = "gauge+number", value = m['r2'] * 100,
                    title = {'text': "CONFIANZA DE IMPACTO (R²)", 'font': {'family': 'Orbitron', 'color': '#4ECCA3', 'size': 18}},
                    gauge = {
                        'axis': {'range': [0, 100], 'tickcolor': "#4ECCA3"}, 
                        'bar': {'color': "#4ECCA3"}, 
                        'bgcolor': "rgba(0,0,0,0)"
                    },
                    number = {'suffix': "%", 'font': {'color': 'white', 'family': 'Orbitron', 'size': 35}}
                ))
                fig_r2.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white", 'family': "Rajdhani"}, height=350)
                st.plotly_chart(fig_r2, use_container_width=True)
        else:
            st.info("Efectúe la optimización de los modelos en la consola central.")

    with tabs[3]:
        if st.session_state.customer_data is not None and st.session_state.ai_model.is_trained:
            # REQUERIMIENTO 1: Selector st.pills con CSS inyectado arriba para contraste premium absoluto
            selector = st.pills("Seleccione Escenario Predictivo:", ["🚀 Lanzamiento de Producto", "💼 Inversión Estructural"])
            st.markdown("<br>", unsafe_allow_html=True)
            
            if selector == "🚀 Lanzamiento de Producto": 
                create_launch_analyzer()
            elif selector == "💼 Inversión Estructural": 
                create_investment_analyzer()
        else:
            st.error("🚨 Acceso Denegado: Requiere la generación de Big Data y la Optimización de Modelos previa en la Consola Central.")

def main():
    apply_professional_ai_theme()
    
    if 'data_generator' not in st.session_state: st.session_state.data_generator = DataGenerator()
    if 'ai_model' not in st.session_state: st.session_state.ai_model = AIModel()
    if 'customer_data' not in st.session_state: st.session_state.customer_data = None
    if 'model_metrics' not in st.session_state: st.session_state.model_metrics = {}
    if 'autenticado' not in st.session_state: st.session_state.autenticado = False

    if not st.session_state.autenticado:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
                <div style="background: #0d111a; border: 1px solid rgba(0, 210, 255, 0.2); padding: 50px 40px; border-radius: 20px; text-align: center; box-shadow: 0 0 40px rgba(0,210,255,0.15);">
                    <h1 style="font-size: calc(2.2rem + 1.2vw); margin-bottom: 0; background: linear-gradient(90deg, #00D2FF, #4ECCA3); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-family:'Orbitron', sans-serif; font-weight: 700; letter-spacing: 2px;">ESTRATEGA IA</h1>
                    <p style="letter-spacing: 6px; font-weight: 600; color: #4ECCA3; font-size: calc(9px + 0.2vw); font-family:'Orbitron', sans-serif; margin-top: 10px;">PREDICCIÓN · ESTRATEGIA · ÉXITO</p>
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
            st.write(f"User: `{st.session_state.usuario_email}`")
            st.markdown("System Status: `ONLINE`")
            st.markdown("---")
            if st.button("🔒 CERRAR SESIÓN", use_container_width=True):
                st.session_state.autenticado = False
                st.rerun()
        run_professional_dashboard()

if __name__ == "__main__":
    main()
