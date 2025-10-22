"""
Extensões Flask compartilhadas para evitar imports circulares
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

# Instâncias das extensões
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
