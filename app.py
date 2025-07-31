import os
import logging
from datetime import timedelta

from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from werkzeug.middleware.proxy_fix import ProxyFix

from database import db, init_db
from config import Config
from jinja_filters import nl2br, format_document, format_currency, status_color, absolute_value

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize extensions
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Initialize database
    init_db(app)
    
    # Initialize extensions
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Configure login manager
    login_manager.login_view = "login"
    login_manager.login_message = "Por favor, faça login para acessar esta página."
    login_manager.login_message_category = "warning"
    
    @login_manager.user_loader
    def load_user(user_id):
        try:
            from models import User
            if user_id is None or user_id == 'None':
                return None
            return User.query.get(int(user_id))
        except (ValueError, TypeError):
            return None
    
    # Handle proxy headers
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    
    # Register custom filters
    app.jinja_env.filters['nl2br'] = nl2br
    app.jinja_env.filters['format_document'] = format_document
    app.jinja_env.filters['format_currency'] = format_currency
    app.jinja_env.filters['status_color'] = status_color
    app.jinja_env.filters['abs'] = absolute_value
    
    # Import and register routes
    from routes import register_routes
    register_routes(app)
    
    return app

# Create app instance
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
