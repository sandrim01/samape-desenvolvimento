import os
import logging
from datetime import timedelta

from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from werkzeug.middleware.proxy_fix import ProxyFix

from database import db
from jinja_filters import nl2br, format_document, format_currency, status_color, absolute_value


# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize extensions
login_manager = LoginManager()
csrf = CSRFProtect()

# Create application
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "development_key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "postgresql://postgres:qUngJAyBvLWQdkmSkZEjjEoMoDVzOBnx@trolley.proxy.rlwy.net:22285/railway")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configure session
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=1)
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# Configure CSRF protection (temporariamente desabilitado para resolver problemas)
app.config["WTF_CSRF_ENABLED"] = False 
app.config["WTF_CSRF_TIME_LIMIT"] = 3600  # 1 hour
app.config["WTF_CSRF_SSL_STRICT"] = False  # Para ambiente de desenvolvimento

# Initialize extensions with app
db.init_app(app)
login_manager.init_app(app)

# Adicionar exceção CSRF para as rotas de exclusão de cliente
csrf.init_app(app)
csrf.exempt('/clientes/<int:id>/excluir')
csrf.exempt('/admin/clientes/<int:id>/excluir-direto')

# Configure login manager
login_manager.login_view = "login"
login_manager.login_message = "Por favor, faça login para acessar esta página."
login_manager.login_message_category = "warning"

# Import models 
import models

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


# Import and register routes
from routes import register_routes
register_routes(app)

# Importa e registra o blueprint do controle de ponto
from ponto import bp_ponto
app.register_blueprint(bp_ponto)

# Create initial admin user if needed
with app.app_context():
    if hasattr(app, 'create_initial_admin'):
        app.create_initial_admin()
