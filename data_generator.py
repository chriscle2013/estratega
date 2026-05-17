# data_generator.py - Versión corregida con valores colombianos realistas
import pandas as pd
import numpy as np
from typing import Dict, List

class DataGenerator:
    def __init__(self):
        self.customer_segments = {
            0: "Jóvenes Urbanos",
            1: "Profesionales Establecidos", 
            2: "Familias con Hijos",
            3: "Adultos Mayores"
        }
    
    def generate_synthetic_data(self, n_samples: int = 1000) -> pd.DataFrame:
        """Genera datos simulados de clientes con valores realistas para Colombia"""
        np.random.seed(42)
        
        data = {
            'edad': np.random.normal(35, 15, n_samples).clip(18, 80),
            # Ingresos mensuales en COP (1,000,000 - 8,000,000 COP)
            'ingreso_mensual': np.random.lognormal(13.5, 0.8, n_samples) * 1000,
            'educacion': np.random.choice(['Primaria', 'Secundaria', 'Universidad', 'Posgrado'], n_samples, p=[0.1, 0.2, 0.5, 0.2]),
            'frecuencia_compra': np.random.poisson(3, n_samples),
            # Valor promedio de compra en COP (5,000 - 500,000 COP)
            'valor_promedio_compra': np.random.exponential(50000, n_samples) + 5000,
            'lealtad_marca': np.random.beta(2, 2, n_samples),
            'crecimiento_mercado': np.random.uniform(0.05, 0.15, n_samples),
            'nivel_competencia': np.random.uniform(1, 10, n_samples),
            'segmento_cliente': np.random.choice([0, 1, 2, 3], n_samples, p=[0.25, 0.35, 0.25, 0.15])
        }
        
        df = pd.DataFrame(data)
        df['lealtad_marca'] = df['lealtad_marca'] * 100  # Convertir a porcentaje
        df['valor_promedio_compra'] = df['valor_promedio_compra'].round(2)
        
        return df
    
    def get_segment_description(self, segment_id: int) -> str:
        return self.customer_segments.get(segment_id, "Segmento Desconocido")
