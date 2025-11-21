from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.database import Database
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='')
    
    # Carregar configurações
    app.config.from_object(Config)
    
    # Configurar CORS para permitir requisições do front-end
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "PATCH"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Inicializar pool de conexões do banco de dados
    try:
        Database.initialize_pool()
        logger.info("✓ Pool de conexões MySQL inicializado com sucesso")
        
        # Testar conexão
        if Database.test_connection():
            logger.info("✓ Conexão com banco de dados MySQL testada com sucesso")
        else:
            logger.warning("⚠ Falha ao testar conexão com banco de dados")
    except Exception as e:
        logger.error(f"✗ Erro ao inicializar banco de dados: {e}")
        logger.warning("⚠ A aplicação continuará sem banco de dados")
    
    # Importar e registrar rotas
    with app.app_context():
        from app import routes
        logger.info("✓ Rotas da API registradas com sucesso")
    
    return app
