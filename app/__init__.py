from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='')
    
    # Configurar CORS para permitir requisições do front-end
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "PATCH"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Importar e registrar rotas
    with app.app_context():
        from app import routes
    
    return app
