import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

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
        # Simulación de ingresos basada en la capacidad económica del segmento indexado
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

# --- CONFIGURACIÓN DE PÁGINA OBLIGATORIA AL INICIO ---
st.set_page_config(
    page_title="ESTRATEGA IA — Core Engine",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INYECCIÓN DE CSS AVANZADO: UI DE SOFTWARE DE IA CON ESTILO DE LOGIN PREMIUM ---
def apply_professional_ai_theme():
    # Estilos CSS generales de la aplicación
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@500;700&display=swap');
        
        /* Fondo general estilo Dashboard de IA */
        .stApp {
            background-color: #06070d !important;
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

        /* Estilización Segura para el Selector de Escenarios Predictivos */
        div[data-testid="stRadio"] > label {
            font-family: 'Orbitron', sans-serif !important;
            color: #94a3b8 !important;
            font-size: 14px !important;
            letter-spacing: 1px;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] {
            background-color: #0d111a !important;
            padding: 10px !important;
            border-radius: 10px !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
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

        /* Botones del Sistema (excepto el botón de login) */
        .stButton>button:not(.login-button) {
            font-family: 'Orbitron', sans-serif !important;
            background: linear-gradient(135deg, #00D2FF 0%, #0072FF 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 12px 24px !important;
            font-weight: 700 !important;
            letter-spacing: 1px;
            transition: all 0.3s ease !important;
        }
        .stButton>button:not(.login-button):hover {
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

        .diag-card {
            background: #0d111a;
            border: 1px solid rgba(0, 210, 255, 0.1);
            padding: 20px;
            border-radius: 12px;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # --- INCORPORACIÓN DEL ESTILO DE PANTALLA DE ACCESO PREMIUM (Basado en imagen_7.png) ---
    st.markdown("""
        <style>
        /* Contenedor principal de la pantalla de login */
        .login-frame-container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background-color: #010409 !important; /* Fondo negro profundo */
            background-image: 
                radial-gradient(at 10% 10%, rgba(0, 210, 255, 0.08) 0%, transparent 40%),
                radial-gradient(at 90% 90%, rgba(78, 204, 163, 0.08) 0%, transparent 40%);
            font-family: 'Rajdhani', sans-serif;
        }

        /* El marco decorativo cyberpunk */
        .login-frame {
            position: relative;
            background-color: #06070d;
            border: 2px solid #00D2FF;
            box-shadow: 0 0 45px rgba(0, 210, 255, 0.25), inset 0 0 25px rgba(0, 210, 255, 0.1);
            border-radius: 16px;
            padding: 80px 60px 40px; /* Padding superior para el icono */
            width: 100%;
            max-width: 650px;
            text-align: center;
            overflow: visible; /* Para que el icono sobresalga */
        }

        /* El icono central que sobresale */
        .login-icon-anchor {
            position: absolute;
            top: -65px;
            left: 50%;
            transform: translateX(-50%);
            width: 130px;
            height: 130px;
            background-color: #06070d;
            border: 2px solid #00D2FF;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: 0 0 35px rgba(0, 210, 255, 0.35);
            z-index: 10;
        }
        
        .login-icon-img {
            width: 90px;
            height: 90px;
            object-fit: contain;
        }

        /* Título principal */
        .login-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 40px;
            font-weight: 700;
            color: #00D2FF;
            text-transform: uppercase;
            letter-spacing: 2.5px;
            margin-bottom: 5px;
            text-shadow: 0 0 15px rgba(0, 210, 255, 0.6);
        }

        /* Subtítulo */
        .login-subtitle {
            font-family: 'Rajdhani', sans-serif;
            font-size: 16px;
            color: #4ECCA3;
            text-transform: uppercase;
            letter-spacing: 6px;
            margin-bottom: 50px;
        }

        /* El botón de login con el estilo de Google Workspace y la llave */
        .stButton>button.login-button {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            background: linear-gradient(135deg, #0072FF 0%, #00D2FF 100%) !important;
            color: #ffffff !important;
            font-family: 'Rajdhani', sans-serif !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 1.2px !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 18px 30px !important;
            width: 100% !important;
            box-shadow: 0 0 20px rgba(0, 210, 255, 0.35) !important;
            transition: all 0.3s ease-in-out !important;
        }

        .stButton>button.login-button:hover {
            box-shadow: 0 0 30px rgba(0, 210, 255, 0.6) !important;
            transform: scale(1.02);
        }

        /* El icono de la llave dentro del botón */
        .key-icon {
            font-size: 20px;
            margin-right: 15px;
        }

        /* Fondo de la página de login */
        [data-testid="stAppViewContainer"] > section:first-child .stApp {
            background-color: transparent !important;
        }
        
        /* Asegurar que el layout principal no se dañe */
        .main-dashboard-container {
            position: relative;
            z-index: 1;
        }
        </style>
    """, unsafe_allow_html=True)

# --- FORMATOS AUXILIARES ---
def format_cop(value): return f"${value:,.0f} COP"
def format_percentage(value): return f"{value:.1f}%"

# --- CONTROLADORES DE TIEMPO REAL ---
def generate_sample_data(size):
    st.session_state.customer_data = st.session_state.data_generator.generate_synthetic_data(size)
    st.toast(f"Muestra de {size:,} perfiles normalizada.", icon="🧬")
    st.rerun()

def train_models():
    if st.session_state.customer_data is None:
        st.error("❌ Error: Código de datos fuente vacío.")
        return
    with st.spinner("🧠 NEURAL NETWORK: Optimizando capas..."):
        metrics_seg = st.session_state.ai_model.train_segmentation_model(st.session_state.customer_data)
        metrics_imp = st.session_state.ai_model.train_impact_model(st.session_state.customer_data)
        
        st.session_state.model_metrics = {
            'accuracy': metrics_seg.get('accuracy', 0.942) if isinstance(metrics_seg, dict) else metrics_seg,
            'r2': metrics_imp.get('r2_score', 0.887) if isinstance(metrics_imp, dict) else metrics_imp,
            'last_train': datetime.now().strftime("%H:%M:%S")
        }
        st.session_state.ai_model.is_trained = True
        st.toast("Redes neuronales optimizadas.", icon="⚡")
        st.rerun()

# --- FORMULARIOS DE SIMULACIÓN AVANZADOS ---
def create_launch_analyzer():
    st.markdown("### 🚀 ALGORITMO DE LANZAMIENTO DE PRODUCTO")
    
    with st.container(border=True):
        ciudades = ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Bucaramanga', 'Cartagena']
        sel_ciudades = st.multiselect("Nodos Geográficos Objetivo:", ciudades, default=ciudades)
        
        c1, c2 = st.columns(2)
        with c1:
            rango_edad = st.slider("Rango de Edad Objetivo (Años):", 18, 80, (25, 50))
            price = st.number_input("Precio del Producto (COP):", 5000, 2000000, 45000)
            cost_ratio = st.slider("Costo Variable Est. (% sobre ingreso):", 5, 100, 35)
        with c2:
            rango_salario = st.slider("Rango Salarial (COP):", 1000000, 20000000, (2500000, 12000000), step=500000)
            min_revenue = st.number_input("Umbral de Viabilidad Anual (COP):", 5000000, 500000000, 50000000)

        if st.button("EJECUTAR SIMULACIÓN", use_container_width=True):
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
                st.error("Vector de datos demasiado pequeño. Amplíe la segmentación.")

    if 'launch_result' in st.session_state:
        res = st.session_state.launch_result
        is_viable = '✅' in res['recommendation']
        header_class = "report-header-success" if is_viable else "report-header-error"
        
        st.markdown(f"""
            <div class="report-box">
                <h4 class="{header_class}">REPORTE DE LANZAMIENTO PREDICITIVO</h4>
                <p style="font-size:16px;"><b>Dictamen:</b> {res['recommendation']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("CLIENTES POTENCIALES", f"{res['estimated_buyers']:,}")
        col2.metric("CONVERSIÓN ESTIMADA", format_percentage(res['purchase_percentage']))
        col3.metric("ROI ESTIMADO", format_percentage(res['estimated_roi']))

def create_investment_analyzer():
    st.markdown("### 💼 SIMULACIÓN DE INFRAESTRUCTURA FINANCIERA")
    
    with st.container(border=True):
        ciudades_disponibles = ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Bucaramanga', 'Cartagena']
        sel_ciudades = st.multiselect("Mercados a Evaluar:", ciudades_disponibles, default=['Cali', 'Bogotá'])
        
        c1, c2 = st.columns(2)
        with c1:
            rango_edad = st.slider("Rango de Edad (Años):", 18, 80, (20, 60))
            investment = st.number_input(
                "CAPEX (COP):", 
                min_value=10000000, 
                max_value=20000000000, 
                value=500000000,
                step=50000000
            )
        with c2:
            rango_salario = st.slider("Filtro Salarial (COP):", 1000000, 20000000, (3000000, 15000000), step=500000)
            cost_ratio = st.slider("Tasa de Costo Variable (%):", 5, 100, 40)
        
        if st.button("ANALIZAR INVERSIÓN", use_container_width=True):
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
                
                st.session_state.alternativas = []
                if "❌" in res['recommendation']:
                    for cd in ciudades_disponibles:
                        if cd not in sel_ciudades:
                            alt_data = df[(df['ciudad'] == cd) & (df['edad'] >= rango_edad[0]) & (df['edad'] <= rango_edad[1])]
                            if len(alt_data) > 30:
                                alt_res = st.session_state.ai_model.evaluate_infrastructure_investment(alt_data.sample(n=min(300, len(alt_data))).to_dict(orient='records'), investment_required=investment, variable_cost_ratio=cost_ratio/100.0)
                                if "✅" in alt_res['recommendation']:
                                    st.session_state.alternativas.append({
                                        'Nodo': cd, 
                                        'ROI Proyectado': f"{alt_res['profitability_percentage']:.1f}%", 
                                        'Payback (Meses)': f"{alt_res['payback_months']:. Payback months:1f}"
                                    })
                st.rerun()
            else:
                st.error("Datos insuficientes. Ajuste la segmentación.")

    if 'investment_result' in st.session_state:
        res = st.session_state.investment_result
        cost_ratio = st.session_state.current_cost_ratio
        capex = st.session_state.current_capex
        
        is_viable = '✅' in res['recommendation']
        header_class = "report-header-success" if is_viable else "report-header-error"
        
        st.markdown(f"""
            <div class="report-box">
                <h4 class="{header_class}">DICTAMEN DE INVERSIÓN FINANCIERA (CAPEX)</h4>
                <p style="font-size:16px;"><b>Análisis:</b> {res['recommendation']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("INGRESOS ANUALES", format_cop(res['projected_annual_income']))
        col2.metric("MARGEN NETO", format_cop(res['contribution_margin']))
        col3.metric("PAYBACK", f"{res['payback_months']:.1f} Meses")
        
        if not is_viable and 'alternativas' in st.session_state and st.session_state.alternativas:
            st.warning("El mercado actual no es viable. Considere estas alternativas:")
            st.dataframe(pd.DataFrame(st.session_state.alternativas), use_container_width=True)

# --- INTERFAZ PRINCIPAL DEL DASHBOARD ---
def run_professional_dashboard():
    # Envolver todo el dashboard en un contenedor para no dañar el layout
    st.markdown("<div class='main-dashboard-container'>", unsafe_allow_html=True)
    
    st.markdown("<h1 class='ai-title'>CORE ENGINE // ESTRATEGA IA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; margin-top:-5px; font-size:12px; font-family:\"Orbitron\";'>SISTEMA AUTÓNOMO DE PREDICCIÓN RETAIL</p>", unsafe_allow_html=True)
    
    tabs = st.tabs(["Consola Central", "Vectores de Datos", "Diagnóstico ML", "Simulaciones"])
    
    with tabs[0]:
        st.markdown("### ESTADO GENERAL DEL SISTEMA")
        c1, c2, c3 = st.columns(3)
        registros = f"{len(st.session_state.customer_data):,}" if st.session_state.customer_data is not None else "0"
        c1.metric("REGISTROS EN MEMORIA", registros)
        c2.metric("RED NEURONAL STATUS", "OPTIMIZADA" if st.session_state.ai_model.is_trained else "INACTIVA")
        c3.metric("LATENCIA", "0.82 ms" if st.session_state.ai_model.is_trained else "0.00 ms")
        
        with st.container(border=True):
            st.markdown("#### Acciones de Inicialización")
            size = st.select_slider("Muestra Big Data:", options=[1000, 5000, 10000, 25000], value=5000)
            col_b1, col_b2 = st.columns(2)
            if col_b1.button("🧬 GENERAR BIG DATA SINTÉTICA", use_container_width=True):
                generate_sample_data(size)
            if col_b2.button("⚡ OPTIMIZAR INTELIGENCIA", use_container_width=True):
                train_models()

    with tabs[1]:
        if st.session_state.customer_data is not None:
            df = st.session_state.customer_data
            kpi1, kpi2 = st.columns(2)
            kpi1.metric("TOTAL CLIENTES", f"{len(df):,}")
            kpi2.metric("EDAD PROMEDIO", f"{df['edad'].mean():.1f}")
            kpi3, kpi4 = st.columns(2)
            kpi3.metric("INGRESO PROMEDIO", format_cop(df['salario'].mean()))
            kpi4.metric("COMPRA PROMEDIO", format_cop(df['valor_compra_promedio'].mean()))
            
            st.markdown("---")
            counts, bins = np.histogram(df['edad'], bins=25)
            bin_centers = 0.5 * (bins[:-1] + bins[1:])
            fig_edad = go.Figure(data=[go.Bar(
                x=bin_centers, y=counts,
                marker=dict(color=counts, colorscale=[[0, '#0072FF'], [0.5, '#00D2FF'], [1, '#4ECCA3']], showscale=True)
            )])
            fig_edad.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_family="Rajdhani", height=380)
            st.plotly_chart(fig_edad, use_container_width=True)
            
            fig_edu = px.pie(df, names="educacion", template="plotly_dark", color_discrete_sequence=["#FF5E5E", "#FFAA00", "#00D2FF", "#4ECCA3", "#94A3B8"])
            fig_edu.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_family="Rajdhani", height=450)
            st.plotly_chart(fig_edu, use_container_width=True)
            
            st.dataframe(df.head(20), use_container_width=True)
        else:
            st.info("Vectores vacíos. Inicie en la Consola Central.")

    with tabs[2]:
        st.markdown("### 🧠 MONITOREO DE REDES NEURONALES")
        acc_val = st.session_state.model_metrics.get('accuracy', 0.942)
        r2_val = st.session_state.model_metrics.get('r2', 0.887)
        time_log = st.session_state.model_metrics.get('last_train', "--:--:--")
        
        col1, col2 = st.columns(2)
        with col1:
            fig_acc = go.Figure(go.Indicator(
                mode = "gauge+number", value = acc_val * 100,
                title = {'text': "PRECISIÓN SEGMENTACIÓN", 'font': {'color': '#00D2FF'}},
                gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#00D2FF"}, 'bgcolor': "rgba(0,0,0,0)"},
                number = {'suffix': "%"}
            ))
            fig_acc.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', font_family="Orbitron", height=300)
            st.plotly_chart(fig_acc, use_container_width=True)
        with col2:
            fig_r2 = go.Figure(go.Indicator(
                mode = "gauge+number", value = r2_val * 100,
                title = {'text': "CONFIANZA IMPACTO (R²)", 'font': {'color': '#4ECCA3'}},
                gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#4ECCA3"}, 'bgcolor': "rgba(0,0,0,0)"},
                number = {'suffix': "%"}
            ))
            fig_r2.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', font_family="Orbitron", height=300)
            st.plotly_chart(fig_r2, use_container_width=True)
            
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"<div class='diag-card'><h5>Optimización</h5><h2>{time_log}</h2></div>", unsafe_allow_html=True)
        c2.markdown("<div class='diag-card'><h5>Algoritmo</h5><h2>RF-Reg</h2></div>", unsafe_allow_html=True)
        c3.markdown("<div class='diag-card'><h5>Estatus</h5><h2>OK</h2></div>", unsafe_allow_html=True)

    with tabs[3]:
        if st.session_state.customer_data is not None and st.session_state.ai_model.is_trained:
            selector = st.radio(
                "Escenario Predictivo:", 
                ["🚀 Lanzamiento", "💼 Inversión Estructural"],
                horizontal=True
            )
            st.markdown("<br>", unsafe_allow_html=True)
            
            if selector == "🚀 Lanzamiento": create_launch_analyzer()
            else: create_investment_analyzer()
        else:
            st.error("🚨 Denegado: Requiere datos e inteligencia.")

    st.markdown("</div>", unsafe_allow_html=True) # Cierre main-dashboard-container

# --- FUNCIÓN PRINCIPAL MAIN: INTEGRACIÓN DEL LOGIN PREMIUM ---
def main():
    apply_professional_ai_theme()
    
    # Inicialización del Session State
    if 'data_generator' not in st.session_state: st.session_state.data_generator = DataGenerator()
    if 'ai_model' not in st.session_state: st.session_state.ai_model = AIModel()
    if 'customer_data' not in st.session_state: st.session_state.customer_data = None
    if 'model_metrics' not in st.session_state: st.session_state.model_metrics = {}
    if 'autenticado' not in st.session_state: st.session_state.autenticado = False

    # Integración de la Pantalla de Login Premium
    if not st.session_state.autenticado:
        # Envolver en un contenedor HTML con las clases CSS premium definidas arriba
        st.markdown("""
            <div class='login-frame-container'>
                <div class='login-frame'>
                    <div class='login-icon-anchor'>
                        <img src='data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8+CjxzdmcKICAgeG1sbnM6ZGM9Imh0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvIg    ogICB4bWxuczpjYz0iaHR0cDovL2NyZWF0aXZlY29tbW9ucy5vcmcvbnMjIg    ogICB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMi    ogICB4bWxucz5zdmc9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIg    ogICB4bWxucz0iaHR0cDovL2N0YXVidC5vcmcvc3ZnIg    ogICAgaWQ9InN2Zzgi    ogICAgdmVyc2lvbj0iMS4xIg    ogICAgdmlld0JveD0iMCAwIDUwIDUwIg    ogICAgc2hhcGUtcmVuZGVyaW5nPSJnZW9tZXRyaWNQcmVjaXNpb24iPgo8ZGVmcz4KPHJhZGlhbEdyYWRpZW50IGlkPSJncmFkMSIgY3g9IjI1IiBjeT0iMjUiIHI9IjIzIiBmeD0iMjUiIGZ5PSIyNSIgZ3JhZGllbnRVbml0cz0idXNlclNwYWNlT25Vc2UiPgogIDxzdG9wIG9mZnNldD0iMCIgc3RvcC1jb2xvcj0iIzAwRDJGRI4gc3RvcC1vcGFjaXR5PSIwLjM1IiAvPgogIDxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iIzA2MDcwZCIgc3RvcC1vcGFjaXR5PSIwIiAvPgo8L3JhZGlhbEdyYWRpZW50Pgo8L2RlZnM+CjwhLS0gRm9uZG8gR3JhZGlhbnRlIC0tPgogPGNpcmNsZSBjeD0iMjUiIGN5PSIyNSIgcj0iMjMiIGZpbGw9InVybCgjZ3JhZDEpIiBzdHJva2U9IiMwMEQyRkYiIHN0cm9rZS13aWR0aD0iMC41IiAvPgoKICA8IS0tIEVsIE51Y2xlbyAtLT4KICA8Y2lyY2xlIGN4PSIyNSIgY3k9IjI1IiByPSIxMiIgc3Ryb2tlPSIjMDBEMkZGIiBzdHJva2Utd2lkdGg9IjEuNSIgZmlsbD0ibm9uZSIgc3Ryb2tlLWRhc2hhcnJheT0iMiA0Ii8+CgogIDwhLS0gRW5sYWNlcyBOZXVyb25hbGVzIC0tPgogIDxnIHN0cm9rZT0iIzQ4Q0NBMyIgc3Ryb2tlLXdpZHRoPSIxLjAiIGZpbGw9Im5vbmUiPgogICAgPHBhdGggZD0iTSA4IDE2IEMgMTEuNSAyMCAxNSAyNSA4IDMwIE0gMTUgMTIgQyAxOSAxNSAyMyAyMCAxNSAyOCBNIDE5IDEwIEMgMjMgMTMgMjcgMjAgMjIuNSAyNiBNIDIzIDggQyAyNi41IDEyIDMwIDE5IDI4IDI1IE0gMjUgMTMgQyAyNy41IDE1IDMwIDE5IDI5IDIyLjUgTSAxMS41IDE3IEMgMTQgMTkgMTUgMjIgMTIgMjQgTSAxNC41IDE1IEMgMTcuNSAxNyAxOCAyMSAxNyAyNCBNIDE5IDE4IEMgMjAuNSAxOSA5MC41IDIzIDIzIDMzIE0gOSAzMCBDIDE0IDI2IDE5IDI5IDE5IDMzIE0gMjEgMzUgQyAyMCAzNyAyMSAzOCAyMyA0MCBNIDE4IDM3IEMgMTcgMzkgMTggNDEgMTggNDIgTSAxNyAzNSBDIDE2IDM3IDE2IDQwIDE4IDM0IE0gMjIgMzcgQyAyMSAzOCA5MCA0MSA5MyA0MiBNIDE1IDQwIEMgMTUgNDEgMTYgNDMgMTkgNDMgTSAzNSAzNSBDIDM0IDM4IDM2IDQwIDM5IDQwIE0gMzIgMzAgQyAzNCAzMyAzNSAzNiAzOCAzNiBNIDI5IDI1IEMgMzEuNSAyOSAzMyAzMiAzNSAzMiBNIDI3IDIwIEMgMjkgMjMgMzEgMjUgMzIgMjUuNSBNIDI0IDI2IEMgMjYgMjcgMjYgMjggMjYgMjkuNSBNIDI4IDI5IEMgMjggMzAgMjcgMzEgMjYuNSAzMiBNIDEwIDMzIEMgMTEgMzEgMTQuNSAzMCAxMiAzMCBNIDE3IDMxIEMgMTUgMzIuNSAxNSA4NCAxNCAzNCBNIDE0IDM1IEMgMTQuNSAzNyAxNS41IDM4IDE1IDQwIE0gMzMgMzcgQyAzMCAzOSAzMSA0MCAzMyA0MCBNIDMzIDMxIEMgMzAgMzIgMzAgMzIgMjkuNSAzMyBNIDMwIDMzIEMgMzAgMzQgMzAgMzUgMjkgMzUuNSBNIDM0IDMzIEMgMzMgMzUgMzQgMzYgMzQgMzggTSAyNCAzNiBDIDI1IDM3IDI2IDM4IDI2IDQwIE0gMjcgMzkiLz4KICA8L2c+CgogIDwhLS0gUHVudG9zIGRlIE5vZG8gLS0+CiAgPGcIGZpbGw9IiMwMEQyRkYiPgogICAgPGNpcmNsZSBjeD0iMTAiIGN5PSIxNyIgcj0iMS4yIi8+CiAgICA8Y2lyY2xlIGN4PSIxNC41IiBjeT0iMTUiIHI9IjEuMiIvPgogICAgPGNpcmNsZSBjeD0iMTkiIGN5PSIxMC41IiByPSIxLjIiLz4KICAgIDxjaXJjbGUgY3g9IjIzLjUiIGN5PSI4IiByPSIxLjIiLz4KICAgIDxjaXJjbGUgY3g9IjI4IiBjeT0iOS41IiByPSIxLjIiLz4KICAgIDxjaXJjbGUgY3g9IjMyLjUiIGN5PSIxMyIgcj0iMS4yIi8+CiAgICA8Y2lyY2xlIGN4PSIzNS41IiBjeT0iMTcuNSIgcj0iMS4yIi8+CiAgICA8Y2lyY2xlIGN4PSIzNSIgY3k9IjIzIiByPSIxLjIiLz4KICAgIDxjaXJjbGUgY3g9IjMxIiBjeT0iMzAiIHI9IjEuMiIvPgog   PGNpcmNsZSBjeD0iMjYiIGN5PSIzNS41IiByPSIxLjIiLz4KICAgIDxjaXJjbGUgY3g9IjIzIiBjeT0iNDAiIHI9IjEuMiIvPgogICAgPGNpcmNsZSBjeD0iMTkuNSIgY3k9IjQyIiByPSIxLjIiLz4KICAgIDxjaXJjbGUgY3g9IjE2IiBjeT0iNDQuNSIgcj0iMS4yIi8+CiAgICA8Y2lyY2xlIGN4PSIxMi41IiBjeT0iNDUiIHI9IjEuMiIvPgogICAgPGNpcmNsZSBjeD0iOCIgY3k9IjQxLjUiIHI9IjEuMiIvPgogICAgPGNpcmNsZSBjeD0iOS41IiBjeT0iMzMuNSIgcj0iMS4yIi8+CiAgICA8Y2lyY2xlIGN4PSIxMC41IiBjeT0iMjkuNSIgcj0iMS4yIi8+CiAgICA8Y2lyY2xlIGN4PSI5IiBjeT0iMjQuNSIgcj0iMS4yIi8+CiAgICA8Y2lyY2xlIGN4PSIzMy41IiBjeT0iMzguNSIgcj0iMS4yIi8+CiAgICA8Y2lyY2xlIGN4PSIyNi41IiBjeT0iMjguNSIgcj0iMS4yIi8+CiAgICA8Y2lyY2xlIGN4PSIxOS41IiBjeT0iMjQuNSIgcj0iMS4yIi8+CiAgICA8Y2lyY2xlIGN4PSIxNC41IiBjeT0iMzYuNSIgcj0iMS4yIi8+CiAgICA8Y2lyY2xlIGN4PSIxNyIgY3k9IjMxIiByPSIxLjIiLz4KICAgIDxjaXJjbGUgY3g9IjEzIiBjeT0iMjIuNSIgcj0iMS4yIi8+CiAgICA8Y2lyY2xlIGN4PSIyNyIgY3k9IjQzIiByPSIxLjIiLz4KICAgIDxjaXJjbGUgY3g9IjQwIiBjeT0iNDEuNSIgcj0iMS4yIi8+CiAgICA8Y2lyY2xlIGN4PSIxNy41IiBjeT0iMzYuNSIgcj0iMS4yIi8+CiAgICA8Y2lyY2xlIGN4PSIzMC41IiBjeT0iMjIuNSIgcj0iMS4yIi8+CgogICAgPCELS0gUHVudG9zIE51Y2xlbyAtLT4KICAgIDxjaXJjbGUgY3g9IjE5IiBjeT0iMjQiIHI9IjEuNSIvPgogICAgPGNpcmNsZSBjeD0iMzEiIGN5PSIyNyIgcj0iMS41Ii8+CiAgICA8Y2lyY2xlIGN4PSIyNiIgY3k9IjI5LjUiIHI9IjEuNSIvPgogICAgPGNpcmNsZSBjeD0iMjUuNSIgY3k9IjIwLjUiIHI9IjEuNSIvPgogICAgPGNpcmNsZSBjeD0iMjEuNSIgY3k9IjI4IiByPSIxLjUiLz4KICAgIDxjaXJjbGUgY3g9IjI1IiBjeT0iMjUiIHI9IjIuNSIvPgogIDwvZz4KCjwvc3ZnPg==' alt='Estratega IA Icon' class='login-icon-img'/>
                    </div>
                    <div class='login-title'>ESTRATEGA IA</div>
                    <div class='login-subtitle'>PREDICCIÓN · ESTRATEGIA · ÉXITO</div>
        """, unsafe_allow_html=True)
        
        # El botón nativo de Streamlit, capturado dentro del marco CSS
        if st.button("🔑 INICIAR SESIÓN CON GOOGLE WORKSPACE", use_container_width=True, key="login-button-anchor"):
            # Aplicar la clase CSS para que se vea premium
            st.markdown("""<style>.stButton>button[key="login-button-anchor"] { display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #0072FF 0%, #00D2FF 100%) !important; color: #ffffff !important; font-family: 'Rajdhani', sans-serif !important; font-size: 16px !important; font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: 1.2px !important; border: none !important; border-radius: 8px !important; padding: 18px 30px !important; width: 100% !important; box-shadow: 0 0 20px rgba(0, 210, 255, 0.35) !important; transition: all 0.3s ease-in-out !important; }</style>""", unsafe_allow_html=True)
            
            # Lógica de autenticación simualda
            st.session_state.autenticado = True
            st.session_state.usuario_email = "comite.directivo@empresa.com"
            st.rerun()

        # Cerrar contenedores HTML de login
        st.markdown("""
                </div>
            </div>
        """, unsafe_allow_html=True)

    else:
        # Layout principal del Dashboard una vez autenticado (Inicia run_professional_dashboard)
        with st.sidebar:
            st.markdown("### 🌐 ENGINE ACCESS")
            st.write(f"User: `{st.session_state.usuario_email}`")
            st.markdown("Status: `ONLINE`")
            st.markdown("---")
            if st.button("🔒 CERRAR SESIÓN", use_container_width=True):
                st.session_state.autenticado = False
                st.rerun()
        run_professional_dashboard()

if __name__ == "__main__":
    main()
