
import os
from sqlalchemy import create_engine, text


def migrate_tables():
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        print("DATABASE_URL não encontrada. Configure a variável de ambiente corretamente.")
        return
    engine = create_engine(DATABASE_URL)
    try:
        with engine.connect() as conn:
            # Adiciona coluna profile_image_data na tabela user, se não existir
            try:
                conn.execute(text('ALTER TABLE "user" ADD COLUMN IF NOT EXISTS profile_image_data TEXT;'))
                print('Coluna profile_image_data adicionada na tabela user.')
            except Exception as e:
                print('Coluna profile_image_data já existe ou erro:', e)
            # Adiciona latitude e longitude na tabela ponto, se não existirem
            try:
                conn.execute(text('ALTER TABLE ponto ADD COLUMN IF NOT EXISTS latitude DOUBLE PRECISION;'))
                print('Coluna latitude adicionada na tabela ponto.')
            except Exception as e:
                print('Coluna latitude já existe ou erro:', e)
            try:
                conn.execute(text('ALTER TABLE ponto ADD COLUMN IF NOT EXISTS longitude DOUBLE PRECISION;'))
                print('Coluna longitude adicionada na tabela ponto.')
            except Exception as e:
                print('Coluna longitude já existe ou erro:', e)
            conn.commit()
    except Exception as e:
        print(f'Erro geral na migração: {e}')

if __name__ == '__main__':
    migrate_tables()
