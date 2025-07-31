from app import app
from database import db
from sqlalchemy import text

def atualizar_ponto_lat_long():
    try:
        with app.app_context():
            with db.engine.connect() as conn:
                # Remove a coluna foto_base64 se existir
                try:
                    conn.execute(text('ALTER TABLE ponto DROP COLUMN foto_base64;'))
                except Exception as e:
                    print('Coluna foto_base64 não existe ou já foi removida.')
                # Adiciona latitude e longitude
                try:
                    conn.execute(text('ALTER TABLE ponto ADD COLUMN latitude FLOAT;'))
                except Exception as e:
                    print('Coluna latitude já existe.')
                try:
                    conn.execute(text('ALTER TABLE ponto ADD COLUMN longitude FLOAT;'))
                except Exception as e:
                    print('Coluna longitude já existe.')
                print('Tabela ponto atualizada para localização!')
    except Exception as e:
        print(f'Erro ao atualizar tabela: {e}')

if __name__ == '__main__':
    atualizar_ponto_lat_long()
