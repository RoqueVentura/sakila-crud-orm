import os
import mysql.connector
from mysql.connector.connection import MySQLConnection


class DbContext:
    """
    Centraliza la conexión a MySQL.
    Todos los modelos reciben esta instancia; ninguno abre su propia conexión.
    Configuración por variables de entorno o valores por defecto.
    """

    _config = {
        'host':     os.environ.get('DB_HOST',     'localhost'),
        'port':     int(os.environ.get('DB_PORT', 3306)),
        'database': os.environ.get('DB_NAME',     'sakila'),
        'user':     os.environ.get('DB_USER',     'root'),
        'password': os.environ.get('DB_PASSWORD', 'FuesHAJX@dsdsw1'),
        'charset':  'utf8mb4',
    }

    def get_connection(self) -> MySQLConnection:
        return mysql.connector.connect(**self._config)

    def test_connection(self) -> bool:
        try:
            conn = self.get_connection()
            conn.close()
            print(f'[DbContext] Conexión exitosa → {self._config["database"]}')
            return True
        except Exception as e:
            print(f'[DbContext] Error: {e}')
            return False


# Instancia global compartida por toda la aplicación
db = DbContext()
