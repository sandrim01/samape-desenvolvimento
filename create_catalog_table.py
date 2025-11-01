"""
Script de migração para criar a tabela de catálogo interno e modificar parts_list_item
"""
import psycopg2
import os

def migrate_catalog():
    """Cria a tabela catalog_item e modifica parts_list_item"""
    
    # Obter a DATABASE_URL do ambiente ou usar a padrão
    database_url = os.environ.get("DATABASE_URL", "postgresql+psycopg://postgres:qUngJAyBvLWQdkmSkZEjjEoMoDVzOBnx@trolley.proxy.rlwy.net:22285/railway")
    
    # Ajustar a URL para psycopg2 (remover o +psycopg se existir)
    database_url = database_url.replace("postgresql+psycopg://", "postgresql://")
    
    # Conectar ao banco
    conn = psycopg2.connect(database_url)
    
    cur = conn.cursor()
    
    try:
        print("🔄 Iniciando migração do catálogo...")
        
        # 1. Criar tabela catalog_item
        print("\n1. Criando tabela catalog_item...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS catalog_item (
                id SERIAL PRIMARY KEY,
                name VARCHAR(200) NOT NULL,
                part_number VARCHAR(100),
                description TEXT,
                last_price NUMERIC(10, 2),
                times_used INTEGER DEFAULT 1,
                first_used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("   ✅ Tabela catalog_item criada")
        
        # 2. Adicionar colunas em parts_list_item
        print("\n2. Adicionando novas colunas em parts_list_item...")
        
        # Verificar se part_name já existe
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='parts_list_item' AND column_name='part_name'
        """)
        if not cur.fetchone():
            cur.execute("ALTER TABLE parts_list_item ADD COLUMN part_name VARCHAR(200)")
            print("   ✅ Coluna part_name adicionada")
        else:
            print("   ⚠️  Coluna part_name já existe")
        
        # Verificar se part_number já existe
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='parts_list_item' AND column_name='part_number'
        """)
        if not cur.fetchone():
            cur.execute("ALTER TABLE parts_list_item ADD COLUMN part_number VARCHAR(100)")
            print("   ✅ Coluna part_number adicionada")
        else:
            print("   ⚠️  Coluna part_number já existe")
        
        # Verificar se description já existe
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='parts_list_item' AND column_name='description'
        """)
        if not cur.fetchone():
            cur.execute("ALTER TABLE parts_list_item ADD COLUMN description TEXT")
            print("   ✅ Coluna description adicionada")
        else:
            print("   ⚠️  Coluna description já existe")
        
        # Verificar se catalog_item_id já existe
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='parts_list_item' AND column_name='catalog_item_id'
        """)
        if not cur.fetchone():
            cur.execute("ALTER TABLE parts_list_item ADD COLUMN catalog_item_id INTEGER REFERENCES catalog_item(id)")
            print("   ✅ Coluna catalog_item_id adicionada")
        else:
            print("   ⚠️  Coluna catalog_item_id já existe")
        
        # 3. Modificar part_id para ser opcional (permitir NULL)
        print("\n3. Modificando coluna part_id para permitir NULL...")
        cur.execute("ALTER TABLE parts_list_item ALTER COLUMN part_id DROP NOT NULL")
        print("   ✅ Coluna part_id agora permite NULL")
        
        # 4. Migrar dados existentes (copiar nome da peça do estoque para part_name)
        print("\n4. Migrando dados existentes...")
        cur.execute("""
            UPDATE parts_list_item 
            SET part_name = (SELECT name FROM part WHERE part.id = parts_list_item.part_id)
            WHERE part_id IS NOT NULL AND part_name IS NULL
        """)
        rows_updated = cur.rowcount
        print(f"   ✅ {rows_updated} registros atualizados com part_name")
        
        # 5. Criar índices para otimização
        print("\n5. Criando índices...")
        
        indices = [
            ("idx_catalog_item_name", "catalog_item", "name"),
            ("idx_catalog_item_part_number", "catalog_item", "part_number"),
            ("idx_catalog_item_active", "catalog_item", "is_active"),
            ("idx_catalog_item_times_used", "catalog_item", "times_used"),
            ("idx_parts_list_item_catalog", "parts_list_item", "catalog_item_id"),
            ("idx_parts_list_item_name", "parts_list_item", "part_name"),
        ]
        
        for idx_name, table, column in indices:
            try:
                cur.execute(f"CREATE INDEX IF NOT EXISTS {idx_name} ON {table}({column})")
                print(f"   ✅ Índice {idx_name} criado")
            except Exception as e:
                print(f"   ⚠️  Erro ao criar índice {idx_name}: {e}")
        
        # 6. Criar constraint para garantir que part_name não seja nulo
        print("\n6. Adicionando constraint de validação...")
        try:
            cur.execute("""
                ALTER TABLE parts_list_item 
                ADD CONSTRAINT check_part_name_not_null 
                CHECK (part_name IS NOT NULL AND part_name != '')
            """)
            print("   ✅ Constraint check_part_name_not_null adicionada")
        except Exception as e:
            print(f"   ⚠️  Constraint já existe ou erro: {e}")
        
        # Commit das mudanças
        conn.commit()
        print("\n✅ Migração concluída com sucesso!")
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Erro durante a migração: {e}")
        raise
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    migrate_catalog()
