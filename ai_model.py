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
