import pymysql
from pymysql.cursors import DictCursor
from app.config import settings

class DatabaseManager:
    """Administrador de conexión orientado a objetos hacia Amazon RDS."""
    
    @classmethod
    def get_connection(cls):
        return pymysql.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME,
            cursorclass=DictCursor,
            autocommit=False
        )