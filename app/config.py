import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DB_HOST: str = os.getenv("DB_HOST", "instancia-rds-iot.cgnw48eewetu.us-east-1.rds.amazonaws.com")
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    DB_USER: str = os.getenv("DB_USER", "admin")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "Admin1234#")
    DB_NAME: str = os.getenv("DB_NAME", "vehiculo_iot")

settings = Settings()