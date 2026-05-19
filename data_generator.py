# data_generator.py - Versión con edad correlacionada a segmentos y selector de muestras
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
        self.segment_age_ranges = {
            0: (18, 30),     # Jóvenes Urbanos: 18-30 años
            1: (25, 50),     # Profesionales Establecidos: 25-50 años
            2: (30, 55),     # Familias con Hijos: 30-55 años
            3: (50, 80)      # Adultos Mayores: 50-80 años
        }
    
    def get_available_sample_sizes(self) -> List[int]:
        """Retorna lista de tamaños de muestra disponibles"""
        # Se agrega el 10000 para permitir la inversión/muestra requerida
        return [1000, 2000, 3000, 4000, 5000]
    
    def generate_synthetic_data(self, n_samples: int = 1000) -> pd.DataFrame:
        """Genera datos simulados de clientes con edad correlacionada a segmentos"""
        
        # Validar tamaño de muestra
        available_sizes = self.get_available_sample_sizes()
        if n_samples not in available_sizes:
            raise ValueError(f"Tamaño de muestra debe ser uno de: {available_sizes}")
        
        np.random.seed(42)
        
        # Segmentos con diferentes rangos de edad e ingresos
        segment_incomes = {
            0: (1500000, 4000000),   # Jóvenes Urbanos: 1.5M - 4M COP
            1: (3000000, 8000000),   # Profesionales Establecidos: 3M - 8M COP
            2: (2000000, 5000000),   # Familias con Hijos: 2M - 5M COP
            3: (1200000, 3000000)    # Adultos Mayores: 1.2M - 3M COP
        }
        
        data = {
            'educacion': np.random.choice(['Primaria', 'Secundaria', 'Universidad', 'Posgrado'], n_samples, p=[0.1, 0.2, 0.5, 0.2]),
            'frecuencia_compra': np.random.poisson(3, n_samples),
            'valor_promedio_compra': np.random.exponential(50000, n_samples) + 5000,
            'lealtad_marca': np.random.beta(2, 2, n_samples),
            'crecimiento_mercado': np.random.uniform(0.05, 0.15, n_samples),
            'nivel_competencia': np.random.uniform(1, 10, n_samples),
            'segmento_cliente': np.random.choice([0, 1, 2, 3], n_samples, p=[0.25, 0.35, 0.25, 0.15])
        }
        
        # Asignar edad según segmento (Mismo algoritmo original tuyo)
        edades = []
        ingresos = []
        
        for segment in data['segmento_cliente']:
            min_age, max_age = self.segment_age_ranges[segment]
            min_income, max_income = segment_incomes[segment]
            
            # Generar edad dentro del rango del segmento
            age = np.random.randint(min_age, max_age + 1)
            income = np.random.uniform(min_income, max_income)
            
            edades.append(age)
            ingresos.append(income)
        
        data['edad'] = edades
        data['ingreso_mensual'] = ingresos
        
        df = pd.DataFrame(data)
        df['lealtad_marca'] = df['lealtad_marca'] * 100  # Convertir a porcentaje
        df['valor_promedio_compra'] = df['valor_promedio_compra'].round(2)
        
        return df
    
    def get_segment_description(self, segment_id: int) -> str:
        return self.customer_segments.get(segment_id, "Segmento Desconocido")
