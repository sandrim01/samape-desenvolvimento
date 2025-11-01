"""
Script para adicionar as colunas de KM e valores no banco de dados
Executa as alterações necessárias na tabela service_order
"""
import psycopg2

def add_columns():
    """Adiciona as colunas faltantes na tabela service_order"""
    
    # String de conexão direta para psycopg2 (não SQLAlchemy)
    # postgresql://postgres:qUngJAyBvLWQdkmSkZEjjEoMoDVzOBnx@trolley.proxy.rlwy.net:22285/railway
    conn_string = "host='trolley.proxy.rlwy.net' port=22285 dbname='railway' user='postgres' password='qUngJAyBvLWQdkmSkZEjjEoMoDVzOBnx'"
    
    # Conectar ao banco de dados
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    
    try:
        print("Verificando e adicionando colunas na tabela service_order...")
        
        # Lista de colunas a serem adicionadas
        columns_to_add = [
            ("km_inicial", "NUMERIC(10, 2) DEFAULT 0"),
            ("km_final", "NUMERIC(10, 2) DEFAULT 0"),
            ("km_total", "NUMERIC(10, 2) DEFAULT 0"),
            ("km_rate", "NUMERIC(10, 2) DEFAULT 0"),
            ("km_value", "NUMERIC(10, 2) DEFAULT 0"),
            ("labor_value", "NUMERIC(10, 2) DEFAULT 0"),
            ("parts_value", "NUMERIC(10, 2) DEFAULT 0"),
            ("total_value", "NUMERIC(10, 2) DEFAULT 0"),
        ]
        
        for column_name, column_type in columns_to_add:
            try:
                # Verificar se a coluna já existe
                cur.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='service_order' 
                    AND column_name=%s
                """, (column_name,))
                
                if cur.fetchone() is None:
                    # Coluna não existe, adicionar
                    sql = f"ALTER TABLE service_order ADD COLUMN {column_name} {column_type}"
                    print(f"Adicionando coluna: {column_name}")
                    cur.execute(sql)
                    conn.commit()
                    print(f"✓ Coluna {column_name} adicionada com sucesso!")
                else:
                    print(f"○ Coluna {column_name} já existe, pulando...")
                    
            except Exception as e:
                print(f"✗ Erro ao adicionar coluna {column_name}: {e}")
                conn.rollback()
        
        print("\n" + "="*60)
        print("Script finalizado!")
        print("="*60)
        
    except Exception as e:
        print(f"\n✗ Erro geral: {e}")
        conn.rollback()
        
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    print("="*60)
    print("SCRIPT DE MIGRAÇÃO - Adicionar colunas em service_order")
    print("="*60)
    print("\nEste script irá adicionar as seguintes colunas:")
    print("  - km_inicial, km_final, km_total")
    print("  - km_rate, km_value")
    print("  - labor_value, parts_value, total_value")
    print("\n" + "="*60 + "\n")
    
    add_columns()
