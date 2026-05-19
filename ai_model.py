import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, mean_squared_error, classification_report
import joblib
import os

class AIModel:
    def __init__(self):
        self.segment_model = None
        self.impact_model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = None
        self.is_trained = False
    
    def prepare_data(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Prepara los datos para entrenamiento"""
        # Seleccionar características para segmentación
        feature_cols = ['edad', 'ingreso_mensual', 'educacion', 'frecuencia_compra', 
                       'valor_promedio_compra', 'lealtad_marca', 'crecimiento_mercado', 
                       'nivel_competencia']
        
        X = df[feature_cols].copy()
        y_segment = df['segmento_cliente']
        
        # Codificar variables categóricas
        for col in ['educacion']:
            if col in X.columns:
                le = LabelEncoder()
                X[col] = le.fit_transform(X[col])
                self.label_encoders[col] = le
        
        # Escalar características
        X_scaled = self.scaler.fit_transform(X)
        self.feature_names = feature_cols
        
        return X_scaled, y_segment
    
    def train_segmentation_model(self, df: pd.DataFrame) -> Dict:
        """Entrena el modelo de segmentación de clientes"""
        X, y = self.prepare_data(df)
        
        # Dividir datos
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Entrenar modelo de segmentación
        self.segment_model = RandomForestClassifier(
            n_estimators=100, 
            random_state=42,
            max_depth=10,
            min_samples_split=5
        )
        
        self.segment_model.fit(X_train, y_train)
        
        # Evaluar modelo
        y_pred = self.segment_model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Validación cruzada
        cv_scores = cross_val_score(self.segment_model, X, y, cv=5, scoring='accuracy')
        
        return {
            'accuracy': accuracy,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'classification_report': classification_report(y_test, y_pred, output_dict=True)
        }
    
    def train_impact_model(self, df: pd.DataFrame) -> Dict:
        """Entrena el modelo de impacto de decisiones"""
        # Crear variable objetivo de impacto (puede ser ingreso promedio o valor de compra)
        y_impact = df['valor_promedio_compra']
        
        X, _ = self.prepare_data(df)
        
        # Dividir datos
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_impact, test_size=0.2, random_state=42
        )
        
        # Entrenar modelo de impacto
        self.impact_model = RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            max_depth=10
        )
        
        self.impact_model.fit(X_train, y_train)
        
        # Evaluar modelo
        y_pred = self.impact_model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        return {
            'rmse': rmse,
            'r2_score': self.impact_model.score(X_test, y_test)
        }
    
    def predict_segment(self, customer_data: Dict) -> int:
        """Predice el segmento de un cliente"""
        if not self.is_trained:
            raise ValueError("El modelo no ha sido entrenado")
        
        # Convertir diccionario a DataFrame
        df = pd.DataFrame([customer_data])
        
        # Preparar datos igual que en entrenamiento
        for col in self.label_encoders:
            if col in df.columns:
                df[col] = self.label_encoders[col].transform(df[col])
        
        # Escalar características
        X_scaled = self.scaler.transform(df[self.feature_names])
        
        # Predecir segmento
        segment = self.segment_model.predict(X_scaled)[0]
        return int(segment)
    
    def predict_impact(self, customer_data: Dict) -> float:
        """Predice el impacto económico de una decisión"""
        if not self.is_trained:
            raise ValueError("El modelo no ha sido entrenado")
        
        # Convertir diccionario a DataFrame
        df = pd.DataFrame([customer_data])
        
        # Preparar datos igual que en entrenamiento
        for col in self.label_encoders:
            if col in df.columns:
                df[col] = self.label_encoders[col].transform(df[col])
        
        # Escalar características
        X_scaled = self.scaler.transform(df[self.feature_names])
        
        # Predecir impacto
        impact = self.impact_model.predict(X_scaled)[0]
        return float(impact)
    
    def calculate_purchase_propensity(self, customer_data: Dict) -> float:
        """Calcula la propensión de compra de un cliente (0-1)"""
        # Normalizar valores
        lealtad_norm = customer_data.get('lealtad_marca', 50) / 100.0  # 0-1
        valor_compra_norm = min(customer_data.get('valor_promedio_compra', 30000) / 100000.0, 1.0)  # 0-1
        frecuencia_norm = min(customer_data.get('frecuencia_compra', 3) / 10.0, 1.0)  # 0-1
        
        # Propensión = ponderado de factores
        propensity = (lealtad_norm * 0.4) + (valor_compra_norm * 0.3) + (frecuencia_norm * 0.3)
        return min(max(propensity, 0), 1)  # Asegurar rango 0-1
    
    def evaluate_product_launch(self, scenario_data: List[Dict], 
                               product_price: float = 25000,
                               min_viable_revenue: float = 30000000) -> Dict:
        """Evalúa si es viable lanzar un producto
        
        Responde: ¿La población objetivo COMPRARÁ el producto?
                  ¿Generará VENTAS SUFICIENTES?
        """
        if not self.is_trained:
            raise ValueError("El modelo no ha sido entrenado")
        
        # Calcular propensión de compra para cada cliente
        propensities = [self.calculate_purchase_propensity(customer) for customer in scenario_data]
        
        # Estimar compradores (propensión > 0.5)
        estimated_buyers = sum(1 for p in propensities if p > 0.5)
        purchase_percentage = (estimated_buyers / len(scenario_data)) * 100 if scenario_data else 0
        
        # Proyectar ingresos
        projected_revenue = estimated_buyers * product_price
        avg_propensity = np.mean(propensities) if propensities else 0
        estimated_roi = ((projected_revenue - min_viable_revenue) / min_viable_revenue * 100) if min_viable_revenue > 0 else 0
        
        # Determinar viabilidad
        is_viable = projected_revenue >= min_viable_revenue
        
        # Calcular confianza (0-100)
        confidence = (avg_propensity * 100) * 0.5 + (min(purchase_percentage, 100) * 0.5)
        
        # Generar justificación
        justification = self._generate_launch_justification({
            'avg_propensity': avg_propensity,
            'purchase_percentage': purchase_percentage,
            'estimated_roi': estimated_roi,
            'projected_revenue': projected_revenue,
            'min_viable_revenue': min_viable_revenue
        })
        
        return {
            'recommendation': '✅ LANZAR PRODUCTO' if is_viable else '❌ NO LANZAR',
            'is_viable': is_viable,
            'estimated_buyers': estimated_buyers,
            'total_customers': len(scenario_data),
            'purchase_percentage': round(purchase_percentage, 2),
            'projected_revenue': round(projected_revenue, 2),
            'min_viable_revenue': round(min_viable_revenue, 2),
            'avg_propensity': round(avg_propensity * 100, 2),
            'estimated_roi': round(estimated_roi, 2),
            'confidence': round(confidence, 1),
            'justification': justification
        }
    
    def evaluate_infrastructure_investment(self, scenario_data: List[Dict],
                                         investment_required: float = 100000000) -> Dict:
        """Evalúa si es viable hacer inversión en infraestructura
        
        Responde: ¿El mercado objetivo generará INGRESOS SUFICIENTES?
                  ¿RECUPERARÉ la inversión en tiempo razonable?
        """
        if not self.is_trained:
            raise ValueError("El modelo no ha sido entrenado")
        
        # Calcular propensión de compra
        propensities = [self.calculate_purchase_propensity(customer) for customer in scenario_data]
        avg_propensity = np.mean(propensities) if propensities else 0
        
        # Calcular ingresos anuales proyectados
        # Ingresos = Clientes × Propensión × Ingreso mensual × 12
        total_monthly_income = sum(customer.get('ingreso_mensual', 3000000) for customer in scenario_data)
        avg_monthly_income = total_monthly_income / len(scenario_data) if scenario_data else 0
        projected_annual_income = len(scenario_data) * avg_propensity * avg_monthly_income * 12
        
        # Criterios de viabilidad
        criteria_met = {}
        
        # Criterio 1: Tamaño mínimo de mercado
        criteria_met['market_size'] = len(scenario_data) >= 500
        
        # Criterio 2: Ingresos >= 50% de inversión
        criteria_met['income_ratio'] = projected_annual_income >= (investment_required * 0.5)
        
        # Criterio 3: Período de recuperación <= 18 meses
        payback_months = (investment_required / (projected_annual_income / 12)) if projected_annual_income > 0 else float('inf')
        criteria_met['payback'] = payback_months <= 18
        
        # Criterio 4: Propensión >= 45%
        criteria_met['propensity'] = avg_propensity >= 0.45
        
        # Decisión: >= 3 de 4 criterios
        criteria_count = sum(1 for v in criteria_met.values() if v)
        is_viable = criteria_count >= 3
        
        # Calcular rentabilidad
        profitability = ((projected_annual_income - investment_required) / investment_required * 100) if investment_required > 0 else 0
        
        # Confianza basada en criterios cumplidos
        confidence = (criteria_count / 4) * 100
        
        # Generar justificación
        justification = self._generate_investment_justification({
            'criteria_met': criteria_met,
            'projected_annual_income': projected_annual_income,
            'investment_required': investment_required,
            'payback_months': payback_months,
            'profitability': profitability,
            'avg_propensity': avg_propensity
        })
        
        return {
            'recommendation': '✅ INVERTIR' if is_viable else '❌ NO INVERTIR',
            'is_viable': is_viable,
            'investment_required': round(investment_required, 2),
            'projected_annual_income': round(projected_annual_income, 2),
            'total_customers': len(scenario_data),
            'payback_months': round(payback_months, 1),
            'profitability_percentage': round(profitability, 2),
            'avg_propensity': round(avg_propensity * 100, 2),
            'confidence': round(confidence, 1),
            'criteria_met': criteria_met,
            'justification': justification
        }
    
    def _generate_launch_justification(self, analysis: Dict) -> List[str]:
        """Genera justificación automática para decisión de lanzamiento"""
        justifications = []
        
        avg_propensity = analysis['avg_propensity'] * 100
        purchase_pct = analysis['purchase_percentage']
        roi = analysis['estimated_roi']
        revenue = analysis['projected_revenue']
        min_revenue = analysis['min_viable_revenue']
        
        # Análisis de propensión
        if avg_propensity >= 70:
            justifications.append(f"✅ Propensión: Excelente nivel de interés ({avg_propensity:.1f}%)")
        elif avg_propensity >= 50:
            justifications.append(f"⚠️ Propensión: Moderada ({avg_propensity:.1f}%)")
        else:
            justifications.append(f"❌ Propensión: Baja ({avg_propensity:.1f}%)")
        
        # Análisis de ingresos
        if revenue >= min_revenue * 1.5:
            justifications.append(f"💰 Ingresos: Proyección muy favorable (${revenue/1e6:.1f}M >> ${min_revenue/1e6:.1f}M)")
        elif revenue >= min_revenue:
            justifications.append(f"📊 Ingresos: Proyección favorable (${revenue/1e6:.1f}M >= ${min_revenue/1e6:.1f}M)")
        else:
            justifications.append(f"⚠️ Ingresos: Por debajo del mínimo viable (${revenue/1e6:.1f}M < ${min_revenue/1e6:.1f}M)")
        
        # Análisis de ROI
        if roi > 100:
            justifications.append(f"📈 ROI: Excelente retorno esperado ({roi:.1f}%)")
        elif roi > 0:
            justifications.append(f"📈 ROI: Retorno positivo esperado ({roi:.1f}%)")
        else:
            justifications.append(f"⚠️ ROI: Retorno negativo ({roi:.1f}%)")
        
        # Análisis de demanda
        if purchase_pct >= 60:
            justifications.append(f"🎯 Demanda: Alta ({purchase_pct:.1f}% de clientes)")
        elif purchase_pct >= 40:
            justifications.append(f"📊 Demanda: Moderada ({purchase_pct:.1f}% de clientes)")
        else:
            justifications.append(f"⚠️ Demanda: Baja ({purchase_pct:.1f}% de clientes)")
        
        return justifications
    
    def _generate_investment_justification(self, analysis: Dict) -> List[str]:
        """Genera justificación automática para decisión de inversión"""
        justifications = []
        
        criteria_met = analysis['criteria_met']
        income = analysis['projected_annual_income']
        investment = analysis['investment_required']
        payback = analysis['payback_months']
        profitability = analysis['profitability']
        propensity = analysis['avg_propensity'] * 100
        
        criteria_count = sum(1 for v in criteria_met.values() if v)
        
        # Análisis de criterios
        if criteria_met['market_size']:
            justifications.append("✅ Tamaño de mercado: Suficiente (>= 500 clientes)")
        else:
            justifications.append("❌ Tamaño de mercado: Insuficiente (< 500 clientes)")
        
        if criteria_met['income_ratio']:
            justifications.append(f"✅ Ingresos anuales: ${income/1e6:.1f}M >= 50% inversión")
        else:
            justifications.append(f"❌ Ingresos anuales: ${income/1e6:.1f}M < 50% inversión")
        
        if criteria_met['payback']:
            justifications.append(f"✅ Período de recuperación: {payback:.1f} meses (<= 18 meses)")
        else:
            justifications.append(f"⚠️ Período de recuperación: {payback:.1f} meses (> 18 meses)")
        
        if criteria_met['propensity']:
            justifications.append(f"✅ Propensión de compra: {propensity:.1f}% (>= 45%)")
        else:
            justifications.append(f"❌ Propensión de compra: {propensity:.1f}% (< 45%)")
        
        # Análisis de rentabilidad
        if profitability > 50:
            justifications.append(f"💎 Rentabilidad: Excelente (+{profitability:.1f}%)")
        elif profitability > 0:
            justifications.append(f"📈 Rentabilidad: Positiva (+{profitability:.1f}%)")
        else:
            justifications.append(f"📉 Rentabilidad: Negativa ({profitability:.1f}%)")
        
        # Resumen
        justifications.append(f"\n📊 Criterios cumplidos: {criteria_count}/4")
        
        return justifications
    
    def analyze_scenario(self, scenario_data: List[Dict]) -> Dict:
        """Analiza un escenario de negocio completo"""
        results = []
        
        for customer in scenario_data:
            segment = self.predict_segment(customer)
            impact = self.predict_impact(customer)
            
            results.append({
                'segment': segment,
                'impact': impact,
                'customer_data': customer
            })
        
        # Agregar métricas de resumen
        segments = [r['segment'] for r in results]
        impacts = [r['impact'] for r in results]
        
        return {
            'total_customers': len(results),
            'segment_distribution': pd.Series(segments).value_counts().to_dict(),
            'avg_impact': np.mean(impacts),
            'total_impact': np.sum(impacts),
            'segment_details': results
        }
    
    def save_model(self, filepath: str):
        """Guarda el modelo entrenado"""
        model_data = {
            'segment_model': self.segment_model,
            'impact_model': self.impact_model,
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'feature_names': self.feature_names,
            'is_trained': self.is_trained
        }
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(model_data, filepath)
    
    def load_model(self, filepath: str):
        """Carga un modelo entrenado"""
        if os.path.exists(filepath):
            model_data = joblib.load(filepath)
            self.segment_model = model_data['segment_model']
            self.impact_model = model_data['impact_model']
            self.scaler = model_data['scaler']
            self.label_encoders = model_data['label_encoders']
            self.feature_names = model_data['feature_names']
            self.is_trained = model_data['is_trained']
        else:
            raise FileNotFoundError(f"Model file not found: {filepath}")
