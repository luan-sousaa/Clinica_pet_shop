import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    """Configurações da aplicação Flask e banco de dados"""
    
    # Configurações Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = FLASK_ENV == 'development'
    
    # Configurações do banco de dados MySQL
    DB_CONFIG = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'petCare'),
        'charset': 'utf8mb4',
        'collation': 'utf8mb4_general_ci',
        'autocommit': False,
        'raise_on_warnings': True
    }
    
    # Pool de conexões
    POOL_NAME = 'petcare_pool'
    POOL_SIZE = 5
    POOL_RESET_SESSION = True

    @staticmethod
    def get_db_config():
        """Retorna a configuração do banco de dados"""
        return Config.DB_CONFIG.copy()
