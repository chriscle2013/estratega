import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de la aplicación
APP_CONFIG = {
    'title': 'Prototipo IA para Toma de Decisiones Estratégicas',
    'port': 8501,
    'debug': True,
    'data_path': './data/'
}

# Configuración de modelos
MODEL_CONFIG = {
    'random_state': 42,
    'test_size': 0.2,
    'cv_folds': 5
}

# Configuración de datos simulados
DATA_CONFIG = {
    'n_samples': 1000,
    'n_features': 8,
    'n_classes': 4
}
