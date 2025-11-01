"""
Script para criar as tabelas de Listagem de Peças e adicionar coluna parts_list_number na ServiceOrder
"""
import psycopg2
from config import Config

def create_parts_list_tables():
    """Cria as tabelas parts_list e parts_list_item, e adiciona coluna parts_list_number em service_order"""
    
    # Conectar ao banco de dados Railway
    conn = psycopg2.connect(
        host="trolley.proxy.rlwy.net",
        port=22285,
        database="railway",
        user="postgres",
        password="qUngJAyBvLWQdkmSkZEjjEoMoDVzOBnx"
    )
    
    cur = conn.cursor()
    
    try:
        print("=" * 80)
        print("CRIANDO ESTRUTURA DE LISTAGEM DE PEÇAS")
        print("=" * 80)
        
        # 1. Criar tabela parts_list
        print("\n1. Criando tabela parts_list...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS parts_list (
                id SERIAL PRIMARY KEY,
                list_number VARCHAR(20) UNIQUE NOT NULL,
                service_order_id INTEGER NOT NULL REFERENCES service_order(id) ON DELETE CASCADE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_by INTEGER NOT NULL REFERENCES "user"(id),
                status VARCHAR(20) DEFAULT 'aberta' NOT NULL,
                notes TEXT,
                total_value NUMERIC(10, 2) DEFAULT 0
            );
        """)
        print("   ✅ Tabela parts_list criada com sucesso!")
        
        # 2. Criar índices para parts_list
        print("\n2. Criando índices para parts_list...")
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_parts_list_list_number 
            ON parts_list(list_number);
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_parts_list_service_order 
            ON parts_list(service_order_id);
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_parts_list_created_by 
            ON parts_list(created_by);
        """)
        print("   ✅ Índices criados com sucesso!")
        
        # 3. Criar tabela parts_list_item
        print("\n3. Criando tabela parts_list_item...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS parts_list_item (
                id SERIAL PRIMARY KEY,
                parts_list_id INTEGER NOT NULL REFERENCES parts_list(id) ON DELETE CASCADE,
                part_id INTEGER NOT NULL REFERENCES part(id),
                quantity INTEGER NOT NULL DEFAULT 1,
                unit_price NUMERIC(10, 2) NOT NULL,
                total_price NUMERIC(10, 2) NOT NULL,
                notes TEXT
            );
        """)
        print("   ✅ Tabela parts_list_item criada com sucesso!")
        
        # 4. Criar índices para parts_list_item
        print("\n4. Criando índices para parts_list_item...")
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_parts_list_item_list 
            ON parts_list_item(parts_list_id);
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_parts_list_item_part 
            ON parts_list_item(part_id);
        """)
        print("   ✅ Índices criados com sucesso!")
        
        # 5. Adicionar coluna parts_list_number na tabela service_order
        print("\n5. Adicionando coluna parts_list_number em service_order...")
        try:
            cur.execute("""
                ALTER TABLE service_order 
                ADD COLUMN IF NOT EXISTS parts_list_number VARCHAR(20);
            """)
            print("   ✅ Coluna parts_list_number adicionada com sucesso!")
        except psycopg2.errors.DuplicateColumn:
            print("   ℹ️  Coluna parts_list_number já existe!")
            conn.rollback()
        
        # 6. Criar índice para parts_list_number
        print("\n6. Criando índice para parts_list_number...")
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_service_order_parts_list_number 
            ON service_order(parts_list_number);
        """)
        print("   ✅ Índice criado com sucesso!")
        
        # Commit das alterações
        conn.commit()
        
        print("\n" + "=" * 80)
        print("MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 80)
        print("\n📋 Tabelas criadas:")
        print("   • parts_list")
        print("   • parts_list_item")
        print("\n🔧 Coluna adicionada:")
        print("   • service_order.parts_list_number")
        print("\n✅ Sistema pronto para gerenciar Listagens de Peças!")
        
    except Exception as e:
        print(f"\n❌ ERRO durante a migração: {e}")
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    create_parts_list_tables()
