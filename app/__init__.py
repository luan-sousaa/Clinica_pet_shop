from flask import Flask

def create_app():
    app = Flask(__name__)    
    # Importar e registrar rotas
    with app.app_context():
        from app import routes
    return app
