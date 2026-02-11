import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv

# Cargamos las variables del .env
load_dotenv()

class DatabaseManager:
    _connection_pool = None

    @classmethod
    def initialize(cls):
        """Crea un pool de conexiones para que el servidor sea rápido."""
        try:
            cls._connection_pool = psycopg2.pool.SimpleConnectionPool(
                1, 10, # Mínimo 1 conexión, máximo 10
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                database=os.getenv('DB_NAME')
            )
            print(" Pool de conexiones de PostgreSQL inicializado.")
        except Exception as e:
            print(f" Error al crear el pool: {e}")

    @classmethod
    def get_connection(cls):
        return cls._connection_pool.getconn()

    @classmethod
    def return_connection(cls, connection):
        cls._connection_pool.putconn(connection)

# Inicializamos el gestor al importar
DatabaseManager.initialize()