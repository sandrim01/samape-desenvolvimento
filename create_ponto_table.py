from app import app
from database import db

def create_ponto_table():
    with app.app_context():
        from models import Ponto
        db.create_all()
        print('Tabela ponto criada com sucesso!')

if __name__ == "__main__":
    create_ponto_table()
