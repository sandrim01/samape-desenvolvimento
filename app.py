import os
import logging
from datetime import timedelta

from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from werkzeug.middleware.proxy_fix import ProxyFix

from database import db
from jinja_filters import nl2br, format_document, format_currency, status_color, absolute_value, safe_float, safe_money

# Configure logging - optimized for production
log_level = logging.WARNING if os.getenv('RAILWAY_ENVIRONMENT') == 'production' or os.getenv('FLASK_ENV') == 'production' else logging.INFO
logging.basicConfig(
    level=log_level,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[logging.StreamHandler()]
)

# Initialize extensions
login_manager = LoginManager()
csrf = CSRFProtect()

# Create application
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "development_key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure database with optimized pool settings
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "postgresql://postgres:qUngJAyBvLWQdkmSkZEjjEoMoDVzOBnx@trolley.proxy.rlwy.net:22285/railway")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 1800,  # 30 minutes instead of 5 minutes
    "pool_pre_ping": True,
    "pool_size": 10,       # Increase pool size
    "max_overflow": 20,    # Allow more overflow connections
    "pool_timeout": 30,    # Connection timeout
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configure session
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=1)
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# Configure CSRF protection - TEMPORARIAMENTE DESABILITADO PARA DEBUG
app.config["WTF_CSRF_ENABLED"] = False  # DESABILITADO TEMPORARIAMENTE
app.config["WTF_CSRF_TIME_LIMIT"] = 3600  # 1 hour
app.config["WTF_CSRF_SSL_STRICT"] = False  # Para ambiente de desenvolvimento

# Disable template cache for debugging
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.jinja_env.auto_reload = True
app.jinja_env.cache = {}

# Initialize extensions with app
db.init_app(app)
login_manager.init_app(app)

# CSRF TEMPORARIAMENTE DESABILITADO PARA DEBUG
# csrf.init_app(app)
# csrf.exempt('/clientes/<int:id>/excluir')
# csrf.exempt('/admin/clientes/<int:id>/excluir-direto')
# csrf.exempt('/os/<int:id>/update-ajax')

# Configure login manager
login_manager.login_view = "login"
login_manager.login_message = "Por favor, faÃ§a login para acessar esta pÃ¡gina."
login_manager.login_message_category = "warning"

# Import models 
import models

# Add no-cache headers to prevent browser caching issues
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = "0" 
    response.headers["Pragma"] = "no-cache"
    return response

# Context processor para CSRF (funciona mesmo com CSRF desabilitado)
@app.context_processor
def inject_csrf_token():
    try:
        if app.config.get("WTF_CSRF_ENABLED", True):
            from flask_wtf.csrf import generate_csrf
            return dict(csrf_token=generate_csrf)
        else:
            # Se CSRF estiver desabilitado, retornar token vazio
            return dict(csrf_token=lambda: "")
    except Exception:
        # Em caso de erro, retornar token vazio
        return dict(csrf_token=lambda: "")

# Setup user loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    try:
        from models import User
        if user_id is None or user_id == 'None':
            return None
        return User.query.get(int(user_id))
    except (ValueError, TypeError):
        return None

# Register Jinja filters
app.jinja_env.filters['nl2br'] = nl2br
app.jinja_env.filters['format_document'] = format_document
app.jinja_env.filters['format_currency'] = format_currency
app.jinja_env.filters['status_color'] = status_color
app.jinja_env.filters['abs'] = absolute_value
app.jinja_env.filters['safe_float'] = safe_float
app.jinja_env.filters['safe_money'] = safe_money
app.jinja_env.globals['hasattr'] = hasattr

# Create application context first
with app.app_context():
    # Rota de teste para CSRF
    @app.route('/test-csrf')
    def test_csrf():
        from flask_wtf.csrf import generate_csrf
        token = generate_csrf()
        return f"""
        <html>
        <head>
            <meta name="csrf-token" content="{token}">
            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        </head>
        <body>
            <h1>Teste CSRF Token</h1>
            <p><strong>Token gerado pelo Flask:</strong> {token}</p>
            <button onclick="testToken()">Testar Acesso via JavaScript</button>
            <div id="result"></div>
            
            <script>
            function testToken() {{
                const token = $('meta[name=csrf-token]').attr('content');
                document.getElementById('result').innerHTML = 
                    '<p><strong>Token lido pelo JS:</strong> ' + (token || 'VAZIO') + '</p>';
                console.log('Token CSRF:', token);
            }}
            </script>
        </body>
        </html>
        """
    
    # Import and register routes after app context is available
    from routes import register_routes
    register_routes(app)
    
    # Importa e registra o blueprint do controle de ponto
    from ponto import bp_ponto
    app.register_blueprint(bp_ponto)
    
    # Create initial admin user if needed
    if hasattr(app, 'create_initial_admin'):
        app.create_initial_admin()

# Executa o servidor Flask localmente
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

