from app import app
from database import db
from sqlalchemy import text

def add_foto_base64_column():
    try:
        with app.app_context():
            with db.engine.connect() as conn:
                conn.execute(text('ALTER TABLE ponto ADD COLUMN foto_base64 TEXT;'))
                print('Coluna foto_base64 adicionada com sucesso!')
    except Exception as e:
        print(f'Erro ao adicionar coluna: {e}')

if __name__ == '__main__':
    add_foto_base64_column()
