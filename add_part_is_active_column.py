"""
Script para adicionar coluna is_active na tabela part
"""
from app import app, db
from models import Part
from sqlalchemy import text

def add_is_active_column():
    with app.app_context():
        try:
            # Adicionar coluna is_active na tabela part
            with db.engine.connect() as conn:
                conn.execute(text('ALTER TABLE part ADD COLUMN is_active BOOLEAN DEFAULT TRUE NOT NULL'))
                conn.commit()
            print("Coluna 'is_active' adicionada com sucesso na tabela 'part'!")
        except Exception as e:
            if "already exists" in str(e).lower() or "duplicate column" in str(e).lower():
                print("Coluna 'is_active' já existe na tabela 'part'.")
            else:
                print(f"Erro ao adicionar coluna: {e}")

if __name__ == '__main__':
    add_is_active_column()
