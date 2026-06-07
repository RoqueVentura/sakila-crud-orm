# config.py
import os

DB_CONFIG = {
    'host':     'localhost',
    'port':     3306,
    'database': 'sakila',
    'user':     'root',
    'password': os.environ.get('DB_PASSWORD', 'FuesHAJX@dsdsw1'),
}

def get_config() -> dict:
    """Retorna el diccionario de configuración de la BD."""
    return DB_CONFIG
