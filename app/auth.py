"""
Auth - Decorators e funções para autenticação e autorização
"""

from functools import wraps
from flask import request, jsonify
import jwt
from datetime import datetime, timedelta
from app.config import Config

def create_token(user_data):
    """
    Cria um token JWT para o usuário
    
    Args:
        user_data (dict): Dados do usuário (id, email, tipo_acesso, role)
    
    Returns:
        str: Token JWT
    """
    payload = {
        'user_id': user_data['ID_USUARIO'],
        'email': user_data['EMAIL'],
        'tipo_acesso': user_data['TIPO_ACESSO'],
        'role': user_data['ROLE_MYSQL'],
        'exp': datetime.utcnow() + timedelta(days=1)  # Expira em 1 dia
    }
    
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
    return token

def verify_token(token):
    """
    Verifica e decodifica um token JWT
    
    Args:
        token (str): Token JWT
    
    Returns:
        dict: Dados do usuário ou None se inválido
    """
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """
    Decorator que exige um token JWT válido
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Procurar token no header Authorization
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # "Bearer <token>"
            except IndexError:
                return jsonify({'message': 'Token inválido'}), 401
        
        if not token:
            return jsonify({'message': 'Token não fornecido'}), 401
        
        # Verificar token
        user_data = verify_token(token)
        if not user_data:
            return jsonify({'message': 'Token inválido ou expirado'}), 401
        
        # Adicionar dados do usuário ao request
        request.user = user_data
        
        return f(*args, **kwargs)
    
    return decorated

def role_required(allowed_roles):
    """
    Decorator que exige uma role específica (ADM, VET, CLI)
    
    Args:
        allowed_roles (list): Lista de roles permitidas
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # Primeiro verifica se há token
            token = None
            if 'Authorization' in request.headers:
                auth_header = request.headers['Authorization']
                try:
                    token = auth_header.split(' ')[1]
                except IndexError:
                    return jsonify({'message': 'Token inválido'}), 401
            
            if not token:
                return jsonify({'message': 'Token não fornecido'}), 401
            
            user_data = verify_token(token)
            if not user_data:
                return jsonify({'message': 'Token inválido ou expirado'}), 401
            
            # Verificar role
            user_role = user_data.get('role')
            if user_role not in allowed_roles:
                return jsonify({'message': 'Acesso negado. Permissão insuficiente.'}), 403
            
            request.user = user_data
            return f(*args, **kwargs)
        
        return decorated
    return decorator

def require_admin(f):
    """Decorator que exige role de administrador"""
    return role_required(['ADM'])(f)

def require_vet(f):
    """Decorator que exige role de veterinário ou admin"""
    return role_required(['ADM', 'VET'])(f)

def require_client(f):
    """Decorator que exige role de cliente"""
    return role_required(['ADM', 'CLI'])(f)
