"""
Script de migração para adicionar campos de fabricante e modelo nas tabelas catalog_item e parts_list_item
"""
import psycopg2
import os

def add_manufacturer_model_fields():
    """Adiciona colunas manufacturer e equipment_model"""
    
    # Obter a DATABASE_URL do ambiente ou usar a padrão
    database_url = os.environ.get("DATABASE_URL", "postgresql+psycopg://postgres:qUngJAyBvLWQdkmSkZEjjEoMoDVzOBnx@trolley.proxy.rlwy.net:22285/railway")
    
    # Ajustar a URL para psycopg2
    database_url = database_url.replace("postgresql+psycopg://", "postgresql://")
    
    # Conectar ao banco
    conn = psycopg2.connect(database_url)
    cur = conn.cursor()
    
    try:
        print("🔄 Iniciando migração para adicionar fabricante e modelo...")
        
        # 1. Adicionar colunas em catalog_item
        print("\n1. Adicionando colunas em catalog_item...")
        
        # Verificar se manufacturer já existe
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='catalog_item' AND column_name='manufacturer'
        """)
        if not cur.fetchone():
            cur.execute("ALTER TABLE catalog_item ADD COLUMN manufacturer VARCHAR(100)")
            print("   ✅ Coluna manufacturer adicionada em catalog_item")
        else:
            print("   ⚠️  Coluna manufacturer já existe em catalog_item")
        
        # Verificar se equipment_model já existe
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='catalog_item' AND column_name='equipment_model'
        """)
        if not cur.fetchone():
            cur.execute("ALTER TABLE catalog_item ADD COLUMN equipment_model VARCHAR(150)")
            print("   ✅ Coluna equipment_model adicionada em catalog_item")
        else:
            print("   ⚠️  Coluna equipment_model já existe em catalog_item")
        
        # 2. Adicionar colunas em parts_list_item
        print("\n2. Adicionando colunas em parts_list_item...")
        
        # Verificar se manufacturer já existe
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='parts_list_item' AND column_name='manufacturer'
        """)
        if not cur.fetchone():
            cur.execute("ALTER TABLE parts_list_item ADD COLUMN manufacturer VARCHAR(100)")
            print("   ✅ Coluna manufacturer adicionada em parts_list_item")
        else:
            print("   ⚠️  Coluna manufacturer já existe em parts_list_item")
        
        # Verificar se equipment_model já existe
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='parts_list_item' AND column_name='equipment_model'
        """)
        if not cur.fetchone():
            cur.execute("ALTER TABLE parts_list_item ADD COLUMN equipment_model VARCHAR(150)")
            print("   ✅ Coluna equipment_model adicionada em parts_list_item")
        else:
            print("   ⚠️  Coluna equipment_model já existe em parts_list_item")
        
        # 3. Criar índices para otimização
        print("\n3. Criando índices...")
        
        indices = [
            ("idx_catalog_item_manufacturer", "catalog_item", "manufacturer"),
            ("idx_catalog_item_equipment_model", "catalog_item", "equipment_model"),
            ("idx_parts_list_item_manufacturer", "parts_list_item", "manufacturer"),
            ("idx_parts_list_item_equipment_model", "parts_list_item", "equipment_model"),
        ]
        
        for idx_name, table, column in indices:
            try:
                cur.execute(f"CREATE INDEX IF NOT EXISTS {idx_name} ON {table}({column})")
                print(f"   ✅ Índice {idx_name} criado")
            except Exception as e:
                print(f"   ⚠️  Erro ao criar índice {idx_name}: {e}")
        
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
    add_manufacturer_model_fields()
