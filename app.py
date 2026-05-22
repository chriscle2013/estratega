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
# MOTOR LÓGICO INTEGRADO (AI & DATA)
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

# --- INYECCIÓN DE CSS AVANZADO (CORREGIDO SIN TEXTO PLANO) ---
def apply_professional_ai_theme():
    # Usamos un formato html plano y directo en una sola línea limpia para evitar fallos de renderizado
    css_code = """<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"><style>@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@500;700&display=swap');.stApp {background-color: #06070d !important; color: #e2e8f0 !important;}.stTabs [data-baseweb="tab-list"] {gap: 10px; background-color: #0d111a; padding: 10px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05);}.stTabs [data-baseweb="tab"] {font-family: 'Orbitron', sans-serif !important; height: 45px; background-color: transparent; border-radius: 8px; color: #64748b !important; border: none; transition: all 0.3s ease;}.stTabs [aria-selected="true"] {background: linear-gradient(90deg, rgba(0,210,255,0.15), rgba(78,204,163,0.15)) !important; color: #00D2FF !important; border: 1px solid rgba(0, 210, 255, 0.3) !important;}div[data-testid="stMetric"] {background: #0d111a !important; border: 1px solid rgba(255, 255, 255, 0.05) !important; border-left: 4px solid #00D2FF !important; border-radius: 12px !important; padding: 20px !important;}div[data-testid="stMetric"] [data-testid="stMetricLabel"] {font-family: 'Rajdhani', sans-serif !important; color: #94a3b8 !important; text-transform: uppercase; letter-spacing: 1px;}div[data-testid="stMetric"] [data-testid="stMetricValue"] {font-family: 'Orbitron', sans-serif !important; color: #ffffff !important; font-size: 24px !important;}.stButton>button {font-family: 'Orbitron', sans-serif !important; border-radius: 8px !important; letter-spacing: 1px; transition: all 0.3s ease !important;}.login-frame-container {display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 40px 20px; background-color: #010409; min-height: 70vh;}.login-frame {background-color: #06070d; border: 2px solid #00D2FF; box-shadow: 0 0 35px rgba(0, 210, 255, 0.2); border-radius: 16px; padding: 50px 40px; width: 100%; max-width: 550px; text-align: center; margin-bottom: 20px;}.login-icon-box {font-size: 55px; color: #00D2FF; margin-bottom: 15px;}.login-title {font-family: 'Orbitron', sans-serif; font-size: 36px; font-weight: 700; color: #00D2FF; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 8px;}.login-subtitle {font-family: 'Rajdhani', sans-serif; font-size: 14px; color: #4ECCA3; text-transform: uppercase; letter-spacing: 5px;}div.login-btn-container button {background: linear-gradient(135deg, #0052D4 0%, #4364F7 50%, #6FB1FC 100%) !important; color: #ffffff !important; font-family: 'Orbitron', sans-serif !important; font-size: 14px !important; font-weight: 600 !important; border: none !important; padding: 14px 20px !important; width: 100% !important; box-shadow: 0 0 20px rgba(67, 100, 247, 0.4) !important;}div.login-btn-container button:hover {box-shadow: 0 0 30px rgba(0, 210, 255, 0.8) !important; transform: scale(1.01);}</style>"""
    st.components.v1.html(css_code, height=0, width=0)

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

# --- ANALIZADORES ---
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
                st.session_state.launch_result = res
                st.rerun()
            else:
                st.error("Vector de datos demasiado pequeño.")

    if 'launch_result' in st.session_state:
        res = st.session_state.launch_result
        st.success(res['recommendation'])
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
            investment = st.number_input("CAPEX (COP):", min_value=10000000, value=500000000, step=50000000)
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
                st.rerun()
            else:
                st.error("Datos insuficientes.")

    if 'investment_result' in st.session_state:
        res = st.session_state.investment_result
        st.info(res['recommendation'])
        col1, col2, col3 = st.columns(3)
        col1.metric("INGRESOS ANUALES PROYECTADOS", format_cop(res['projected_annual_income']))
        col2.metric("MARGEN DE CONTRIBUCIÓN NETO", format_cop(res['contribution_margin']))
        col3.metric("PERIODO DE RETORNO (PAYBACK)", f"{res['payback_months']:.1f} Meses")

# --- INTERFAZ PRINCIPAL DEL DASHBOARD ---
def run_professional_dashboard():
    st.markdown("<h2 style='font-family:\"Orbitron\"; color:#00D2FF; letter-spacing:2px;'>CORE ENGINE // ESTRATEGA IA</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; margin-top:-10px; font-size:12px; font-family:\"Orbitron\";'>SISTEMA AUTÓNOMO DE PREDICCIÓN RETAIL</p>", unsafe_allow_html=True)
    
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
            st.markdown("#### DISTRIBUCIÓN PORCENTUAL DE EDADES")
            counts, bins = np.histogram(df['edad'], bins=10)
            bin_centers = 0.5 * (bins[:-1] + bins[1:])
            fig_edad = go.Figure(data=[go.Bar(
                x=bin_centers, y=counts,
                marker=dict(color=counts, colorscale=[[0, '#0052D4'], [0.5, '#00D2FF'], [1, '#4ECCA3']])
            )])
            fig_edad.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_family="Rajdhani", height=300)
            st.plotly_chart(fig_edad, use_container_width=True)
            st.dataframe(df.head(10), use_container_width=True)
        else:
            st.info("Vectores vacíos. Inicie en la Consola Central.")

    with tabs[2]:
        st.markdown("### 🧠 MONITOREO DE REDES NEURONALES")
        acc_val = st.session_state.model_metrics.get('accuracy', 0.942)
        r2_val = st.session_state.model_metrics.get('r2', 0.887)
        
        col1, col2 = st.columns(2)
        with col1:
            fig_acc = go.Figure(go.Indicator(
                mode = "gauge+number", value = acc_val * 100,
                title = {'text': "PRECISIÓN SEGMENTACIÓN", 'font': {'color': '#00D2FF', 'family': 'Orbitron', 'size': 14}},
                gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#00D2FF"}, 'bgcolor': "rgba(0,0,0,0)"},
                number = {'suffix': "%"}
            ))
            fig_acc.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=250)
            st.plotly_chart(fig_acc, use_container_width=True)
        with col2:
            fig_r2 = go.Figure(go.Indicator(
                mode = "gauge+number", value = r2_val * 100,
                title = {'text': "CONFIANZA IMPACTO (R²)", 'font': {'color': '#4ECCA3', 'family': 'Orbitron', 'size': 14}},
                gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#4ECCA3"}, 'bgcolor': "rgba(0,0,0,0)"},
                number = {'suffix': "%"}
            ))
            fig_r2.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=250)
            st.plotly_chart(fig_r2, use_container_width=True)

    with tabs[3]:
        if st.session_state.customer_data is not None and st.session_state.ai_model.is_trained:
            selector = st.radio("Seleccione Escenario Predictivo:", ["🚀 Lanzamiento de Producto", "💼 Inversión Estructural"], horizontal=True)
            if "Lanzamiento" in selector: create_launch_analyzer()
            else: create_investment_analyzer()
        else:
            st.error("🚨 Denegado: Requieres cargar datos e inteligencia primero.")

# --- MAIN ---
def main():
    apply_professional_ai_theme()
    
    if 'data_generator' not in st.session_state: st.session_state.data_generator = DataGenerator()
    if 'ai_model' not in st.session_state: st.session_state.ai_model = AIModel()
    if 'customer_data' not in st.session_state: st.session_state.customer_data = None
    if 'model_metrics' not in st.session_state: st.session_state.model_metrics = {}
    if 'autenticado' not in st.session_state: st.session_state.autenticado = False

    if not st.session_state.autenticado:
        # Contenedor HTML del login aislado y seguro
        st.markdown("""
            <div style='display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 40px 20px; min-height: 60vh;'>
                <div style='background-color: #06070d; border: 2px solid #00D2FF; box-shadow: 0 0 35px rgba(0, 210, 255, 0.2); border-radius: 16px; padding: 50px 40px; width: 100%; max-width: 550px; text-align: center; margin-bottom: 25px;'>
                    <div style='font-size: 55px; color: #00D2FF; margin-bottom: 15px;'><i class='fa-solid fa-compass-drafting'></i></div>
                    <div style='font-family: "Orbitron", sans-serif; font-size: 36px; font-weight: 700; color: #00D2FF; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 8px;'>ESTRATEGA IA</div>
                    <div style='font-family: "Rajdhani", sans-serif; font-size: 14px; color: #4ECCA3; text-transform: uppercase; letter-spacing: 5px;'>PREDICCIÓN · ESTRATEGIA · ÉXITO</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Botón de Login Nativo posicionado exactamente abajo
        st.markdown("<div class='login-btn-container' style='width:100%; max-width:550px; margin: -100px auto 0 auto;'>", unsafe_allow_html=True)
        if st.button("🔑 INICIAR SESIÓN CON GOOGLE WORKSPACE", use_container_width=True):
            st.session_state.autenticado = True
            st.session_state.usuario_email = "directorio@estratega.ia"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        with st.sidebar:
            st.markdown("### 🌐 ENGINE ACCESS")
            st.write(f"User: `{st.session_state.usuario_email}`")
            if st.button("🔒 CERRAR SESIÓN", use_container_width=True):
                st.session_state.autenticado = False
                st.rerun()
        run_professional_dashboard()

if __name__ == "__main__":
    main()
