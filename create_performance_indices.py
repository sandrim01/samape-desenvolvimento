"""
Script para criar índices de performance no banco de dados
Execute este script após as otimizações para acelerar consultas
"""

from database import db
from app import app
import logging

# Lista de índices para melhorar performance das consultas mais comuns
PERFORMANCE_INDICES = [
    # Índices para Service Orders (consultas mais frequentes)
    "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_service_orders_status ON service_orders(status);",
    "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_service_orders_created_at ON service_orders(created_at);",
    "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_service_orders_client_id ON service_orders(client_id);",
    "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_service_orders_equipment_id ON service_orders(equipment_id);",
    "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_service_orders_user_id ON service_orders(user_id);",
    
    # Índice composto para dashboard (status + data)
    "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_service_orders_status_date ON service_orders(status, created_at);",
    
    # Índices para Financial Entries
    "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_financial_entries_date ON financial_entries(date);",
    "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_financial_entries_type ON financial_entries(type);",
    "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_financial_entries_service_order_id ON financial_entries(service_order_id);",
    
    # Índices para Equipment
    "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_equipment_client_id ON equipment(client_id);",
    "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_equipment_brand_model ON equipment(brand, model);",
    
    # Índices para Clients
    "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_clients_name ON clients(name);",
    "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_clients_document ON clients(document);",
    
    # Índices para Parts
    "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_parts_name ON parts(name);",
    "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_parts_code ON parts(code);",
    
    # Índices para Users (login performance)
    "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_email ON users(email);",
    "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_username ON users(username);",
    
    # Índices para Action Log (se existir)
    "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_action_log_timestamp ON action_log(timestamp) WHERE timestamp IS NOT NULL;",
    "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_action_log_user_id ON action_log(user_id) WHERE user_id IS NOT NULL;",
    
    # Índices para Part Sales
    "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_part_sales_date ON part_sales(sale_date);",
    "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_part_sales_part_id ON part_sales(part_id);",
    
    # Índices para Supplier Orders
    "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_supplier_orders_date ON supplier_orders(order_date);",
    "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_supplier_orders_supplier_id ON supplier_orders(supplier_id);",
]

def create_performance_indices():
    """Criar todos os índices de performance"""
    with app.app_context():
        try:
            # Desabilitar autocommit para executar em transação
            connection = db.engine.connect()
            
            print("🚀 Criando índices de performance...")
            
            for i, index_sql in enumerate(PERFORMANCE_INDICES, 1):
                try:
                    print(f"[{i}/{len(PERFORMANCE_INDICES)}] Executando: {index_sql[:50]}...")
                    connection.execute(db.text(index_sql))
                    connection.commit()
                    print(f"✅ Índice {i} criado com sucesso")
                    
                except Exception as e:
                    error_msg = str(e).lower()
                    if 'already exists' in error_msg or 'duplicate' in error_msg:
                        print(f"⚠️  Índice {i} já existe, pulando...")
                    else:
                        print(f"❌ Erro ao criar índice {i}: {e}")
                        logging.error(f"Erro ao criar índice: {e}")
                    
                    # Rollback desta operação e continue
                    try:
                        connection.rollback()
                    except:
                        pass
            
            connection.close()
            print("\n🎉 Processo de criação de índices concluído!")
            print("💡 Os índices melhorarão a performance das consultas mais comuns.")
            
        except Exception as e:
            print(f"❌ Erro geral na criação de índices: {e}")
            logging.error(f"Erro geral na criação de índices: {e}")

def analyze_database():
    """Executar ANALYZE para atualizar estatísticas do banco"""
    with app.app_context():
        try:
            print("📊 Atualizando estatísticas do banco de dados...")
            connection = db.engine.connect()
            
            # PostgreSQL
            if 'postgresql' in str(db.engine.url):
                connection.execute(db.text("ANALYZE;"))
                print("✅ ANALYZE PostgreSQL executado")
            
            # SQLite
            elif 'sqlite' in str(db.engine.url):
                connection.execute(db.text("ANALYZE;"))
                print("✅ ANALYZE SQLite executado")
            
            connection.commit()
            connection.close()
            
        except Exception as e:
            print(f"⚠️  Erro ao executar ANALYZE: {e}")

if __name__ == "__main__":
    print("🔧 Iniciando otimização de performance do banco de dados...")
    print("=" * 60)
    
    # Criar índices
    create_performance_indices()
    
    # Atualizar estatísticas
    analyze_database()
    
    print("\n" + "=" * 60)
    print("🎯 Otimização concluída! O sistema deve estar mais rápido agora.")
    print("📈 Monitore a performance e execute novamente se necessário.")