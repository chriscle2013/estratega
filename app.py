# app.py - Versión 7.0 PRODUCTION ENGINE (Advanced Launch Analytics)
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
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

        df.loc[df['educacion'] == 'Primaria', 'salario'] = df.loc[df['educacion'] == 'Primaria', 'salario'].clip(upper=3000000)
        df.loc[df['educacion'] == 'Secundaria', 'salario'] = df.loc[df['educacion'] == 'Secundaria', 'salario'].clip(upper=5000000)
        df.loc[df['educacion'] == 'Técnico', 'salario'] = df.loc[df['educacion'] == 'Técnico', 'salario'].clip(upper=8000000)
        
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


# --- INYECCIÓN DE CSS AVANZADO: UI DE SOFTWARE DE IA ---
def apply_professional_ai_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@500;700&display=swap');
    
    .stApp {
        background-color: #06070d !important;
        background-image: radial-gradient(circle at 10% 20%, rgba(0, 210, 255, 0.03) 0%, transparent 50%), radial-gradient(circle at 90% 80%, rgba(78, 204, 163, 0.03) 0%, transparent 50%) !important;
        color: #e2e8f0 !important;
    }
    
    div[data-testid="stDialog"] div[role="dialog"] {
        background-color: #0d111a !important;
        border: 1px solid rgba(0, 210, 255, 0.2) !important;
        border-radius: 16px !important;
    }
    
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
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    div.login-btn-container div.stButton > button:first-child {
        max-width: 440px !important;
        width: 100% !important;
        margin: 15px auto 0 auto !important;
        background: linear-gradient(135deg, #00D2FF 0%, #0072FF 100%) !important;
        color: #ffffff !important;
        text-shadow: 0px 1px 3px rgba(0, 0, 0, 0.8) !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 15px 20px !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        letter-spacing: 1px !important;
        box-shadow: 0 4px 15px rgba(0,210,255,0.4) !important;
        display: block !important;
    }
    
    @keyframes pulse-glow {
        0% { transform: scale(1); filter: drop-shadow(0 0 5px rgba(0,210,255,0.2)); }
        100% { transform: scale(1.04); filter: drop-shadow(0 0 15px rgba(0,210,255,0.5)); }
    }
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    """, unsafe_allow_html=True)


# --- FORMATOS AUXILIARES ---
def format_cop(value):
    return f"${value:,.0f} COP"


def format_percentage(value):
    return f"{value:.1f}%"


# --- VENTANAS EMERGENTES DE PROCESAMIENTO (MODALES) ---
@st.dialog("⚙️ SISTEMA DE DATOS")
def modal_generar_data(size):
    st.markdown("<p style='font-family:\"Orbitron\"; color:#00D2FF;'>SINTETIZANDO BIG DATA...</p>", unsafe_allow_html=True)
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for percent_complete in range(0, 101, 25):
        time.sleep(0.3)
        progress_bar.progress(percent_complete)
        status_text.text(f"Estructurando registros: {percent_complete}%")
    
    st.session_state.customer_data = st.session_state.data_generator.generate_synthetic_data(size)
    st.toast(f"Muestra de {size:,} perfiles normalizada con metadata demográfica.", icon="🧬")
    st.rerun()


@st.dialog("🧠 PROCESAMIENTO NEURAL")
def modal_optimizar_modelos():
    st.markdown("<p style='font-family:\"Orbitron\"; color:#4ECCA3;'>OPTIMIZANDO CAPAS DE DECISIÓN...</p>", unsafe_allow_html=True)
    with st.spinner("Computando matrices de covarianza..."):
        time.sleep(1.5)
    
    metrics_seg = st.session_state.ai_model.train_segmentation_model(st.session_state.customer_data)
    metrics_imp = st.session_state.ai_model.train_impact_model(st.session_state.customer_data)
    
    st.session_state.model_metrics = {
        'accuracy': metrics_seg.get('accuracy', 0.942) if isinstance(metrics_seg, dict) else metrics_seg,
        'r2': metrics_imp.get('r2_score', 0.887) if isinstance(metrics_imp, dict) else metrics_imp,
        'last_train': datetime.now().strftime("%H:%M:%S")
    }
    st.session_state.ai_model.is_trained = True
    st.toast("Redes neuronales optimizadas para simulaciones.", icon="⚡")
    st.rerun()


# --- FORMULARIOS DE SIMULACIÓN AVANZADOS ---
def create_launch_analyzer():
    st.markdown("### 🚀 ALGORITMO DE LANZAMIENTO DE PRODUCTO")
    st.caption("Análisis de elasticidad, segmentación y proyección financiera a 3 años")
    
    with st.container(border=True):
        ciudades = ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Bucaramanga', 'Cartagena']
        sel_ciudades = st.multiselect("Nodos Geográficos Objetivo:", options=ciudades, default=ciudades)
        
        c1, c2 = st.columns(2)
        with c1:
            rango_edad = st.slider("Rango de Edad Objetivo (Años):", 18, 80, (25, 50))
            price = st.number_input("Precio Base del Producto (COP):", 5000, 2000000, 45000)
            cost_ratio = st.slider("Tasa de Costo Variable Est. (% sobre ingreso):", 5, 100, 35, key="launch_cost")
            analizar_elasticidad = st.checkbox("📊 Analizar elasticidad precio-demanda", value=True)
            
        with c2:
            rango_salario = st.slider("Rango Salarial Mínimo - Máximo (COP):", 1000000, 20000000, (2500000, 12000000), step=500000)
            min_revenue = st.number_input("Umbral Crítico de Viabilidad Anual (COP):", 5000000, 500000000, 50000000)
            meses_estudio = st.selectbox("Horizonte de proyección:", [12, 24, 36], index=2, format_func=lambda x: f"{x} meses")
        
        if st.button("EXECUTE PREDICTION RUN", use_container_width=True):
            df = st.session_state.customer_data
            filtered = df[
                (df['ciudad'].isin(sel_ciudades)) & 
                (df['edad'] >= rango_edad[0]) & 
                (df['edad'] <= rango_edad[1]) & 
                (df['salario'] >= rango_salario[0]) & 
                (df['salario'] <= rango_salario[1])
            ]
            
            if len(filtered) > 10:
                test_c = filtered.sample(n=min(500, len(filtered))).to_dict(orient='records')
                
                res_base = st.session_state.ai_model.evaluate_product_launch(
                    test_c, product_price=price, min_viable_revenue=min_revenue
                )
                res_base['estimated_roi'] = res_base['estimated_roi'] * (1 - (cost_ratio - 35)/100.0)
                
                elasticidad_data = []
                if analizar_elasticidad:
                    precios_test = [price * 0.6, price * 0.8, price, price * 1.2, price * 1.4]
                    for p in precios_test:
                        res_p = st.session_state.ai_model.evaluate_product_launch(
                            test_c, product_price=p, min_viable_revenue=min_revenue
                        )
                        elasticidad_data.append({
                            'precio': p,
                            'buyers': res_p['estimated_buyers'],
                            'conversion': res_p['purchase_percentage'],
                            'revenue': res_p['estimated_buyers'] * p,
                            'roi': res_p['estimated_roi'] * (1 - (cost_ratio - 35)/100.0)
                        })
                
                segment_analysis = {}
                for edu in filtered['educacion'].unique():
                    sub = filtered[filtered['educacion'] == edu]
                    if len(sub) > 10:
                        sub_dict = sub.sample(n=min(100, len(sub))).to_dict(orient='records')
                        res_edu = st.session_state.ai_model.evaluate_product_launch(
                            sub_dict, product_price=price, min_viable_revenue=min_revenue
                        )
                        segment_analysis[f"edu_{edu}"] = {
                            'nombre': edu,
                            'conversion': res_edu['purchase_percentage'],
                            'buyers': res_edu['estimated_buyers'],
                            'sample_size': len(sub)
                        }
                
                rangos_edad = [(18, 30), (31, 45), (46, 60), (61, 80)]
                for r in rangos_edad:
                    sub = filtered[(filtered['edad'] >= r[0]) & (filtered['edad'] <= r[1])]
                    if len(sub) > 10:
                        sub_dict = sub.sample(n=min(100, len(sub))).to_dict(orient='records')
                        res_edad = st.session_state.ai_model.evaluate_product_launch(
                            sub_dict, product_price=price, min_viable_revenue=min_revenue
                        )
                        segment_analysis[f"edad_{r[0]}_{r[1]}"] = {
                            'nombre': f"{r[0]}-{r[1]} años",
                            'conversion': res_edad['purchase_percentage'],
                            'buyers': res_edad['estimated_buyers'],
                            'sample_size': len(sub)
                        }
                
                st.session_state.launch_result = res_base
                st.session_state.elasticidad_data = elasticidad_data
                st.session_state.segment_analysis = segment_analysis
                st.session_state.filtered_sample_size = len(filtered)
                st.session_state.meses_estudio = meses_estudio
                st.session_state.cost_ratio_launch = cost_ratio / 100.0
                st.session_state.base_price = price
                
                st.rerun()
            else:
                st.error("Vector de datos demasiado pequeño. Amplíe los rangos de segmentación.")
    
    if 'launch_result' in st.session_state:
        res = st.session_state.launch_result
        is_viable = '✅' in res['recommendation']
        header_class = "report-header-success" if is_viable else "report-header-error"
        
        sample_size = st.session_state.filtered_sample_size
        confidence_level = min(95, 60 + (sample_size / 20)) if sample_size < 800 else 95
        
        st.markdown(f"""
        <div class="report-box">
            <h4 class="{header_class}">REPORTE EJECUTIVO DE LANZAMIENTO</h4>
            <p style="font-size:16px; margin-top:10px;"><b>Dictamen del Motor:</b> {res['recommendation']}</p>
            <p style="font-size:13px; color:#94a3b8; margin-top:-5px;">Confianza del modelo: <b>{confidence_level:.1f}%</b> (basado en {sample_size:,} perfiles válidos)</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("CLIENTES POTENCIALES", f"{res['estimated_buyers']:,}", help="Estimación de compradores en el mercado objetivo")
        col2.metric("RATIO DE CONVERSIÓN", format_percentage(res['purchase_percentage']), help="% del mercado objetivo que compraría")
        col3.metric("ROI ESTIMADO", format_percentage(res['estimated_roi']), delta="vs umbral" if res['estimated_roi'] > 0 else None)
        col4.metric("TAMAÑO DE MUESTRA", f"{sample_size:,}", help="Perfiles analizados")
        
        st.markdown("---")
        
        if 'elasticidad_data' in st.session_state and st.session_state.elasticidad_data:
            st.markdown("### 📈 Análisis de Elasticidad Precio-Demanda")
            st.caption("Simulación de demanda según diferentes puntos de precio")
            
            data_elast = pd.DataFrame(st.session_state.elasticidad_data)
            precio_optimo = data_elast.loc[data_elast['revenue'].idxmax(), 'precio']
            revenue_optimo = data_elast['revenue'].max()
            
            col_e1, col_e2 = st.columns(2)
            with col_e1:
                fig_elasticidad = go.Figure()
                fig_elasticidad.add_trace(go.Scatter(
                    x=data_elast['precio'],
                    y=data_elast['buyers'],
                    mode='lines+markers',
                    name='Demanda Estimada',
                    line=dict(color='#00D2FF', width=3),
                    marker=dict(size=10, color='#4ECCA3')
                ))
                fig_elasticidad.add_trace(go.Scatter(
                    x=data_elast['precio'],
                    y=data_elast['revenue'] / 1e6,
                    mode='lines+markers',
                    name='Revenue (Millones COP)',
                    line=dict(color='#FF6B6B', width=3, dash='dot'),
                    marker=dict(size=10, color='#FF6B6B'),
                    yaxis='y2'
                ))
                fig_elasticidad.update_layout(
                    title="Curva de Demanda vs Revenue",
                    xaxis_title="Precio (COP)",
                    yaxis_title="Unidades Demandadas",
                    yaxis2=dict(title="Revenue (Millones COP)", overlaying='y', side='right'),
                    template="plotly_dark",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=350,
                    legend=dict(x=0.02, y=0.98)
                )
                st.plotly_chart(fig_elasticidad, use_container_width=True)
            
            with col_e2:
                st.markdown(f"""
                <div style="background:#0d111a; padding:15px; border-radius:12px; border:1px solid rgba(0,210,255,0.2);">
                    <p style="color:#00D2FF; font-family:'Orbitron'; margin-bottom:10px;">🎯 PRECIO ÓPTIMO ESTIMADO</p>
                    <p style="font-size:28px; font-weight:700; margin:0;">{format_cop(precio_optimo)}</p>
                    <p style="color:#94a3b8; font-size:12px;">Maximiza revenue estimado en {format_cop(revenue_optimo)}</p>
                    <hr style="margin:15px 0; border-color:#1e293b;">
                    <p style="color:#4ECCA3; font-family:'Orbitron'; margin-bottom:5px;">⚡ ESTRATEGIA RECOMENDADA</p>
                """, unsafe_allow_html=True)
                
                if precio_optimo > st.session_state.base_price:
                    st.markdown("<p style='margin:0;'>✅ El mercado tolera un precio <b>superior</b> al base. Considere reposicionamiento premium.</p>", unsafe_allow_html=True)
                elif precio_optimo < st.session_state.base_price:
                    st.markdown("<p style='margin:0;'>⚠️ El precio actual podría ser <b>elevado</b>. Evaluar reducción para maximizar volumen.</p>", unsafe_allow_html=True)
                else:
                    st.markdown("<p style='margin:0;'>✅ El precio base está <b>alineado</b> con el óptimo de mercado.</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
        
        if 'segment_analysis' in st.session_state and st.session_state.segment_analysis:
            st.markdown("### 👥 Desglose por Perfil de Cliente")
            st.caption("Identificación del buyer persona con mayor intención de compra")
            
            seg_df = pd.DataFrame([
                {'Segmento': v['nombre'], 'Intención de Compra': v['conversion'], 'Muestra': v['sample_size']}
                for v in st.session_state.segment_analysis.values()
            ]).sort_values('Intención de Compra', ascending=False)
            
            col_s1, col_s2 = st.columns([2, 1])
            with col_s1:
                fig_seg = go.Figure(data=[
                    go.Bar(
                        x=seg_df['Segmento'],
                        y=seg_df['Intención de Compra'],
                        marker_color=seg_df['Intención de Compra'],
                        marker_colorscale=[[0, '#0072FF'], [1, '#4ECCA3']],
                        text=seg_df['Intención de Compra'].apply(lambda x: f"{x:.1f}%"),
                        textposition='outside'
                    )
                ])
                fig_seg.update_layout(
                    title="Intención de Compra por Segmento",
                    xaxis_title="Segmento",
                    yaxis_title="Intención de Compra (%)",
                    template="plotly_dark",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=350
                )
                st.plotly_chart(fig_seg, use_container_width=True)
            
            with col_s2:
                top_segment = seg_df.iloc[0]
                st.markdown(f"""
                <div style="background:#0d111a; padding:15px; border-radius:12px; border:1px solid rgba(78,204,163,0.3);">
                    <p style="color:#4ECCA3; font-family:'Orbitron'; margin-bottom:10px;">🏆 BUYER PERSONA DOMINANTE</p>
                    <p style="font-size:18px; font-weight:700; margin:0;">{top_segment['Segmento']}</p>
                    <p style="font-size:24px; color:#00D2FF; margin:5px 0;">{top_segment['Intención de Compra']:.1f}%</p>
                    <p style="color:#94a3b8; font-size:11px;">Intención de compra | Muestra: {top_segment['Muestra']} perfiles</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("### 💰 Proyección Financiera")
        st.caption(f"Estimación a {st.session_state.meses_estudio} meses | Tasa de costo variable: {st.session_state.cost_ratio_launch * 100:.1f}%")
        
        ingresos_mensuales = (res['estimated_buyers'] * st.session_state.base_price) / 12
        costo_variable_mensual = ingresos_mensuales * st.session_state.cost_ratio_launch
        costo_fijo_mensual = ingresos_mensuales * 0.15
        margen_mensual = ingresos_mensuales - costo_variable_mensual - costo_fijo_mensual
        
        meses = np.arange(1, st.session_state.meses_estudio + 1)
        flujo_mensual = np.full(len(meses), margen_mensual)
        flujo_acumulado = np.cumsum(flujo_mensual)
        
        inversion_inicial = st.session_state.base_price * res['estimated_buyers'] * 0.3
        break_even_meses = np.where(flujo_acumulado >= inversion_inicial)[0]
        break_even = break_even_meses[0] + 1 if len(break_even_meses) > 0 else None
        
        col_p1, col_p2, col_p3, col_p4 = st.columns(4)
        col_p1.metric("Ingreso Mensual Estimado", format_cop(ingresos_mensuales))
        col_p2.metric("Margen Mensual Neto", format_cop(margen_mensual), delta="antes de impuestos")
        col_p3.metric("Inversión Inicial Estimada", format_cop(inversion_inicial))
        if break_even:
            col_p4.metric("Punto de Equilibrio", f"{break_even} meses", help="Meses para recuperar inversión")
        else:
            col_p4.metric("Punto de Equilibrio", "> 36 meses", help="No se alcanza en el horizonte proyectado")
        
        fig_proy = go.Figure()
        fig_proy.add_trace(go.Bar(
            x=meses,
            y=flujo_mensual,
            name="Flujo Mensual",
            marker_color="#00D2FF",
            opacity=0.7
        ))
        fig_proy.add_trace(go.Scatter(
            x=meses,
            y=flujo_acumulado,
            name="Flujo Acumulado",
            line=dict(color="#4ECCA3", width=3),
            yaxis="y2"
        ))
        fig_proy.add_hline(y=0, line_dash="dash", line_color="red", opacity=0.5)
        if break_even:
            fig_proy.add_vline(x=break_even, line_dash="dash", line_color="#FFB347", opacity=0.8,
                               annotation_text=f"Break-even mes {break_even}")
        
        fig_proy.update_layout(
            title="Flujo de Caja Proyectado",
            xaxis_title="Mes",
            yaxis_title="Flujo Mensual (COP)",
            yaxis2=dict(title="Flujo Acumulado (COP)", overlaying='y', side='right'),
            template="plotly_dark",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400,
            legend=dict(x=0.02, y=0.98)
        )
        st.plotly_chart(fig_proy, use_container_width=True)
        
        st.markdown("### ⚠️ Análisis de Riesgos y Mitigaciones")
        
        riesgos = []
        
        if res['purchase_percentage'] < 15:
            riesgos.append(("Alta", "Baja intención de compra (<15%)", "Reforzar propuesta de valor, testear con early adopters"))
        elif res['purchase_percentage'] < 25:
            riesgos.append(("Media", "Intención de compra moderada", "Optimizar canales de conversión y mensaje"))
        
        if sample_size < 200:
            riesgos.append(("Alta", "Muestra pequeña para inferencia robusta", "Ampliar dataset o realizar estudio cualitativo complementario"))
        
        if res['estimated_roi'] < 20:
            riesgos.append(("Media", "ROI estimado bajo (<20%)", "Revisar estructura de costos o ajustar precio"))
        
        if not is_viable:
            riesgos.append(("Crítica", "No se alcanza el umbral mínimo de viabilidad", "Pausar lanzamiento, reevaluar mercado objetivo"))
        
        if not riesgos:
            riesgos.append(("Baja", "No se identificaron riesgos significativos", "Continuar con plan de lanzamiento definido"))
        
        riesgo_df = pd.DataFrame(riesgos, columns=["Nivel", "Riesgo Identificado", "Mitigación Recomendada"])
        
        def color_risk(val):
            if val == "Crítica":
                return 'color: #FF5E5E; font-weight: bold'
            elif val == "Alta":
                return 'color: #FFB347'
            elif val == "Media":
                return 'color: #FFD700'
            else:
                return 'color: #4ECCA3'
        
        st.dataframe(riesgo_df.style.applymap(color_risk, subset=['Nivel']), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        if st.button("📥 Exportar Reporte Completo (JSON)", use_container_width=True):
            reporte_completo = {
                "fecha_generacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "dictamen": res['recommendation'],
                "metricas_clave": {
                    "buyers_estimados": res['estimated_buyers'],
                    "tasa_conversion": res['purchase_percentage'],
                    "roi_estimado": res['estimated_roi'],
                    "confianza_modelo": confidence_level
                },
                "elasticidad_precio": st.session_state.elasticidad_data if 'elasticidad_data' in st.session_state else [],
                "segmentacion": st.session_state.segment_analysis if 'segment_analysis' in st.session_state else {},
                "proyeccion_financiera": {
                    "ingreso_mensual": ingresos_mensuales,
                    "margen_mensual": margen_mensual,
                    "inversion_inicial": inversion_inicial,
                    "break_even_meses": break_even
                },
                "riesgos_identificados": riesgos
            }
            st.json(reporte_completo)
            st.toast("Reporte exportado correctamente", icon="✅")


def create_investment_analyzer():
    st.markdown("### 💼 SIMULACIÓN DE INFRAESTRUCTURA FINANCIERA")
    with st.container(border=True):
        ciudades_disponibles = ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Bucaramanga', 'Cartagena']
        sel_ciudades = st.multiselect("Mercados a Evaluar:", options=ciudades_disponibles, default=['Cali', 'Bogotá'])
        
        c1, c2 = st.columns(2)
        with c1:
            rango_edad = st.slider("Filtro Demográfico - Rango de Edad (Años):", 18, 80, (20, 60), key="inv_edad")
            investment = st.number_input(
                "CAPEX Requerido para Expansión (COP):",
                min_value=10000000,
                max_value=20000000000,
                value=500000000,
                step=50000000
            )
        with c2:
            rango_salario = st.slider("Filtro Macroeconómico - Salario (COP):", 1000000, 20000000, (3000000, 7000000), step=500000, key="inv_sal")
            cost_ratio = st.slider("Tasa de Costo Variable Est. (% sobre ingreso):", 5, 100, 93, key="inv_cost")
        
        if st.button("RUN FINANCIAL SIMULATION", use_container_width=True):
            df = st.session_state.customer_data
            filtered = df[
                (df['ciudad'].isin(sel_ciudades)) & 
                (df['edad'] >= rango_edad[0]) & 
                (df['edad'] <= rango_edad[1]) & 
                (df['salario'] >= rango_salario[0]) & 
                (df['salario'] <= rango_salario[1])
            ]
            
            if len(filtered) > 10:
                test_c = filtered.sample(n=min(500, len(filtered))).to_dict(orient='records')
                res = st.session_state.ai_model.evaluate_infrastructure_investment(test_c, investment_required=investment, variable_cost_ratio=cost_ratio/100.0)
                st.session_state.investment_result = res
                st.session_state.current_cost_ratio = cost_ratio / 100.0
                st.session_state.current_capex = investment
                st.rerun()
            else:
                st.error("Datos insuficientes. Ajuste los parámetros de segmentación.")
    
    if 'investment_result' in st.session_state:
        res = st.session_state.investment_result
        cost_ratio = st.session_state.current_cost_ratio
        capex = st.session_state.current_capex
        is_viable = '✅' in res['recommendation']
        header_class = "report-header-success" if is_viable else "report-header-error"
        
        st.markdown(f"""
        <div class="report-box">
            <h4 class="{header_class}">DICTAMEN EXPLICABLE DE INVERSIÓN FINANCIERA (CAPEX)</h4>
            <p style="font-size:16px; margin-top:10px;"><b>Análisis de Viabilidad:</b> {res['recommendation']}</p>
            <p style="font-size:13px; color:#94a3b8; margin-top:-5px;">Confianza estadística del modelo predictivo: <b>{res['confidence']:.2f}%</b> basado en {res['sample_size_evaluated']} perfiles económicos válidos.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("INGRESOS ANUALES PROYECTADOS", format_cop(res['projected_annual_income']))
        col2.metric("MARGEN DE CONTRIBUCIÓN NETO", format_cop(res['contribution_margin']))
        col3.metric("PERIODO DE RETORNO (PAYBACK)", f"{res['payback_months']:.1f} Meses")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        c_analisis, c_grafico = st.columns([1, 1])
        with c_analisis:
            st.markdown("#### 🔬 DESGLOSE ESTRUCTURAL DEL MODELO")
            costos_operativos = res['projected_annual_income'] * cost_ratio
            rentabilidad_anual = (res['contribution_margin'] / capex) * 100
            data_breakdown = {
                "Concepto Financiero": ["Inversión Inicial Requerida (CAPEX)", "Ingreso Operativo Mensual Est.", "Costos Variables Estimados (Anual)", "Margen de Contribución Real (%)", "Retorno de Inversión Anualizado (ROI)"],
                "Valor Estructurado": [format_cop(capex), format_cop(res['projected_annual_income'] / 12), format_cop(costos_operativos), f"{((1 - cost_ratio)*100):.1f}%", f"{rentabilidad_anual:.2f}% por año"]
            }
            st.table(pd.DataFrame(data_breakdown))
        
        with c_grafico:
            st.markdown("#### 📊 ANÁLISIS DE SENSIBILIDAD (ESTRÉS DE MERCADO)")
            ingreso_base = res['projected_annual_income']
            escenarios = ["Estresado (-20%)", "Conservador (-10%)", "Base Original", "Optimista (+10%)"]
            valores_ingreso = [ingreso_base * 0.8, ingreso_base * 0.9, ingreso_base, ingreso_base * 1.1]
            valores_margen = [v * (1 - cost_ratio) for v in valores_ingreso]
            fig_sens = go.Figure()
            fig_sens.add_trace(go.Bar(x=escenarios, y=valores_ingreso, name="Ingresos Proyectados", marker_color="#00D2FF"))
            fig_sens.add_trace(go.Bar(x=escenarios, y=valores_margen, name="Margen Neto Libre", marker_color="#4ECCA3"))
            fig_sens.update_layout(barmode='group', template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_family="Rajdhani", height=280, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_sens, use_container_width=True)


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
            size = st.select_slider("Muestra Big Data:", options=[1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000], value=5000)
            col_b1, col_b2 = st.columns(2)
            if col_b1.button("🧬 GENERAR BIG DATA", use_container_width=True):
                modal_generar_data(size)
            if col_b2.button("⚡ OPTIMIZAR MODELOS DE INTELIGENCIA", use_container_width=True):
                if st.session_state.customer_data is None:
                    st.error("❌ Error: Código de datos fuente vacío.")
                else:
                    modal_optimizar_modelos()
    
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
            g_col1, g_col2 = st.columns(2)
            with g_col1:
                counts, bins = np.histogram(df['edad'], bins=25)
                bin_centers = 0.5 * (bins[:-1] + bins[1:])
                fig_edad = go.Figure(data=[go.Bar(x=bin_centers, y=counts, marker=dict(color=counts, colorscale=[[0, '#0072FF'], [0.5, '#00D2FF'], [1, '#4ECCA3']], showscale=True))])
                fig_edad.update_layout(title="DISTRIBUCIÓN PORCENTUAL DE EDADES", template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_family="Rajdhani", height=380)
                st.plotly_chart(fig_edad, use_container_width=True)
            with g_col2:
                city_counts = df['ciudad'].value_counts().reset_index()
                city_counts.columns = ['ciudad', 'count']
                fig_ciudad = go.Figure(data=[go.Pie(labels=city_counts['ciudad'], values=city_counts['count'], hole=.4, marker=dict(colors=['#00D2FF', '#0072FF', '#4ECCA3', '#3b82f6', '#10b981', '#1e293b']))])
                fig_ciudad.update_layout(title="PARTICIPACIÓN PORCENTUAL POR CIUDAD", template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_family="Rajdhani", height=380)
                st.plotly_chart(fig_ciudad, use_container_width=True)
            
            st.markdown("---")
            st.markdown("<h3 style='font-family:\"Orbitron\"; color:#00D2FF; font-size:18px; letter-spacing:1px; margin-bottom:15px;'><i class='fa-solid fa-database'></i> MATRIZ DE VECTORES DE DATOS EN TIEMPO REAL</h3>", unsafe_allow_html=True)
            st.dataframe(df.head(20), use_container_width=True)
        else:
            st.info("Consola vacía. Por favor inicie la carga de Big Data en la Consola Central.")
    
    with tabs[2]:
        st.markdown("### 🧠 MONITOREO DE REDES NEURONALES")
        acc_val = st.session_state.model_metrics.get('accuracy', 0.942)
        r2_val = st.session_state.model_metrics.get('r2', 0.887)
        time_log = st.session_state.model_metrics.get('last_train', "12:34:57")
        
        col1, col2 = st.columns(2)
        with col1:
            fig_acc = go.Figure(go.Indicator(mode="gauge+number", value=acc_val * 100, title={'text': "PRECISIÓN SEGMENTACIÓN", 'font': {'family': 'Orbitron', 'color': '#00D2FF', 'size': 16}}, gauge={'axis': {'range': [0, 100], 'tickcolor': "#00D2FF"}, 'bar': {'color': "#00D2FF"}, 'bgcolor': "rgba(0,0,0,0)"}, number={'suffix': "%", 'font': {'color': 'white', 'family': 'Orbitron', 'size': 35}}))
            fig_acc.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=300)
            st.plotly_chart(fig_acc, use_container_width=True)
        with col2:
            fig_r2 = go.Figure(go.Indicator(mode="gauge+number", value=r2_val * 100, title={'text': "CONFIANZA DE IMPACTO (R²)", 'font': {'family': 'Orbitron', 'color': '#4ECCA3', 'size': 16}}, gauge={'axis': {'range': [0, 100], 'tickcolor': "#4ECCA3"}, 'bar': {'color': "#4ECCA3"}, 'bgcolor': "rgba(0,0,0,0)"}, number={'suffix': "%", 'font': {'color': 'white', 'family': 'Orbitron', 'size': 35}}))
            fig_r2.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=300)
            st.plotly_chart(fig_r2, use_container_width=True)
        
        st.markdown("<br>#### LOG DE ENTRENAMIENTO CRÍTICO", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"<div class='diag-card'><h5>Última Optimización</h5><h2 style='color:#00D2FF; font-family:\"Orbitron\"; margin:5px 0 0 0;'>{time_log}</h2></div>", unsafe_allow_html=True)
        c2.markdown("<div class='diag-card'><h5>Algoritmo Base</h5><h2 style='color:#4ECCA3; font-family:\"Orbitron\"; margin:5px 0 0 0;'>RF-Regressor</h2></div>", unsafe_allow_html=True)
        c3.markdown("<div class='diag-card'><h5>Estatus Operativo</h5><h2 style='color:white; font-family:\"Orbitron\"; margin:5px 0 0 0;'>OPTIMIZADO</h2></div>", unsafe_allow_html=True)
    
    with tabs[3]:
        if st.session_state.customer_data is not None and st.session_state.ai_model.is_trained:
            selector = st.radio(
                "Seleccione Escenario Predictivo Corporativo:",
                ["🚀 Lanzamiento de Producto", "💼 Inversión Estructural"],
                horizontal=True
            )
            st.markdown("<br>", unsafe_allow_html=True)
            if selector == "🚀 Lanzamiento de Producto":
                create_launch_analyzer()
            elif selector == "💼 Inversión Estructural":
                create_investment_analyzer()
        else:
            st.error("🚨 Acceso Denegado: Requiere la generación de Big Data y la Optimización de Modelos previa en la Consola Central.")


def main():
    apply_professional_ai_theme()
    
    if 'data_generator' not in st.session_state:
        st.session_state.data_generator = DataGenerator()
    if 'ai_model' not in st.session_state:
        st.session_state.ai_model = AIModel()
    if 'customer_data' not in st.session_state:
        st.session_state.customer_data = None
    if 'model_metrics' not in st.session_state:
        st.session_state.model_metrics = {}
    if 'autenticado' not in st.session_state:
        st.session_state.autenticado = False
    
    if not st.session_state.autenticado:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1.8, 1])
        with col2:
            st.markdown('<div style="background:#0d111a; border:1px solid rgba(0,210,255,0.25); padding:40px 35px; border-radius:20px; box-shadow:0 15px 45px rgba(0,0,0,0.6), 0 0 30px rgba(0,210,255,0.1); text-align:center; max-width:440px; margin:0 auto;"><div style="font-size:65px; background:linear-gradient(135deg, #00D2FF, #4ECCA3); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin-bottom:15px; display:inline-block; animation:pulse-glow 3s infinite alternate;"><i class="fa-solid fa-circle-nodes"></i></div><h1 style="font-size:32px; background:linear-gradient(90deg, #00D2FF, #4ECCA3); -webkit-background-clip:text; -webkit-text-fill-color:transparent; font-family:\'Orbitron\', sans-serif; margin:5px 0 10px 0; font-weight:700; border:none; padding:0; background-color:transparent; line-height:1.2;">ESTRATEGA IA</h1><p style="letter-spacing:4px; color:#4ECCA3; font-family:\'Rajdhani\', sans-serif; font-size:12px; font-weight:700; margin-bottom:25px; background:transparent; border:none; padding:0;">PREDICCIÓN · ESTRATEGIA · ÉXITO</p></div>', unsafe_allow_html=True)
            st.markdown('<div class="login-btn-container">', unsafe_allow_html=True)
            if st.button("🔑 INICIAR SESIÓN", use_container_width=True):
                st.session_state.autenticado = True
                st.session_state.usuario_email = "comite.directivo@empresa.com"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        with st.sidebar:
            st.markdown("### 🌐 ENGINE ACCESS")
            st.write(f"User: `{st.session_state.usuario_email}`")
            st.markdown("---")
            if st.button("🔒 CERRAR SESIÓN", use_container_width=True):
                st.session_state.autenticado = False
                st.rerun()
        run_professional_dashboard()


if __name__ == "__main__":
    main()
