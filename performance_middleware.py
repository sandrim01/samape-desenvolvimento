"""
Middleware de performance para otimizar o carregamento da aplicação
"""
import time
from functools import wraps
from flask import request, g, current_app, make_response
import hashlib
import os

def performance_headers():
    """Adiciona headers de performance para otimizar cache do navegador"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            response = make_response(f(*args, **kwargs))
            
            # Cache agressivo para recursos estáticos
            if request.endpoint and 'static' in request.endpoint:
                response.headers['Cache-Control'] = 'public, max-age=31536000'  # 1 ano
                response.headers['Expires'] = 'Thu, 31 Dec 2025 23:59:59 GMT'
            else:
                # Cache mais conservador para páginas dinâmicas
                response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                response.headers['Pragma'] = 'no-cache'
                response.headers['Expires'] = '0'
            
            # Headers de segurança e performance
            response.headers['X-Content-Type-Options'] = 'nosniff'
            response.headers['X-Frame-Options'] = 'DENY'
            response.headers['X-XSS-Protection'] = '1; mode=block'
            
            return response
        return decorated_function
    return decorator

def track_performance():
    """Middleware para monitorar performance das requisições"""
    def init_app(app):
        @app.before_request
        def before_request():
            g.start_time = time.time()
            
        @app.after_request
        def after_request(response):
            # Só loggar tempos em desenvolvimento ou se for muito lento
            if hasattr(g, 'start_time'):
                duration = time.time() - g.start_time
                is_production = os.getenv('RAILWAY_ENVIRONMENT') == 'production'
                
                # Em produção, só loggar se for muito lento (>2s)
                if not is_production or duration > 2.0:
                    current_app.logger.warning(
                        f'Request to {request.endpoint} took {duration:.2f}s'
                    )
                    
                # Adicionar header de timing (só em desenvolvimento)
                if not is_production:
                    response.headers['X-Response-Time'] = f'{duration:.2f}s'
            
            return response
    
    return init_app

def etag_cache():
    """Implementa cache ETag simples para respostas"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Gerar ETag baseado na URL e parâmetros
            etag_data = f"{request.url}:{str(kwargs)}"
            etag = hashlib.md5(etag_data.encode()).hexdigest()
            
            # Verificar se cliente já tem o recurso
            if request.headers.get('If-None-Match') == etag:
                return '', 304
            
            response = make_response(f(*args, **kwargs))
            response.headers['ETag'] = etag
            return response
        
        return decorated_function
    return decorator