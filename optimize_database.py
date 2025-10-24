# OTIMIZAÇÕES DE PERFORMANCE - ÍNDICES DATABASE
# Arquivo para criação de índices que melhoram significativamente a performance

from database import db
from sqlalchemy import text

def create_performance_indexes():
    """
    Cria índices no banco de dados para melhorar a performance das consultas mais frequentes
    """
    
    try:
        # Índices para tabela service_orders (consultas mais frequentes)
        print("Criando índices para service_orders...")
        
        # Índice para filtros por status
        db.session.execute(text("""
            CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_service_orders_status 
            ON service_orders(status);
        """))
        
        # Índice para filtros por data de criação
        db.session.execute(text("""
            CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_service_orders_created_at 
            ON service_orders(created_at DESC);
        """))
        
        # Índice para filtros por cliente
        db.session.execute(text("""
            CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_service_orders_client_id 
            ON service_orders(client_id);
        """))
        
        # Índice para filtros por responsável
        db.session.execute(text("""
            CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_service_orders_responsible_id 
            ON service_orders(responsible_id);
        """))
        
        # Índice composto para consultas complexas
        db.session.execute(text("""
            CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_service_orders_client_status 
            ON service_orders(client_id, status);
        """))
        
        print("Criando índices para action_logs...")
        
        # Índice para logs de ação (dashboard)
        db.session.execute(text("""
            CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_action_logs_timestamp 
            ON action_logs(timestamp DESC);
        """))
        
        print("Criando índices para equipment...")
        
        # Índice para equipamentos por cliente
        db.session.execute(text("""
            CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_equipment_client_id 
            ON equipment(client_id);
        """))
        
        print("Criando índices para financial_entries...")
        
        # Índice para entradas financeiras por data
        db.session.execute(text("""
            CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_financial_entries_date 
            ON financial_entries(date DESC);
        """))
        
        # Índice para entradas financeiras por tipo
        db.session.execute(text("""
            CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_financial_entries_type 
            ON financial_entries(type);
        """))
        
        print("Criando índices para users...")
        
        # Índice para usuários ativos
        db.session.execute(text("""
            CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_active 
            ON users(active) WHERE active = true;
        """))
        
        db.session.commit()
        print("✅ Todos os índices de performance foram criados com sucesso!")
        
        # Estatísticas dos índices
        result = db.session.execute(text("""
            SELECT schemaname, tablename, indexname, indexdef 
            FROM pg_indexes 
            WHERE indexname LIKE 'idx_%' 
            ORDER BY tablename, indexname;
        """))
        
        print("\n📊 Índices criados:")
        for row in result:
            print(f"  • {row.tablename}.{row.indexname}")
            
    except Exception as e:
        print(f"❌ Erro ao criar índices: {str(e)}")
        db.session.rollback()

def analyze_database_performance():
    """
    Analisa o desempenho do banco de dados e sugere otimizações
    """
    try:
        print("\n🔍 Analisando performance do banco...")
        
        # Verificar consultas lentas
        result = db.session.execute(text("""
            SELECT query, calls, total_time, mean_time, rows
            FROM pg_stat_statements 
            WHERE mean_time > 100 
            ORDER BY mean_time DESC 
            LIMIT 10;
        """))
        
        print("\n⚠️  Consultas mais lentas (>100ms):")
        for row in result:
            print(f"  • {row.mean_time:.2f}ms - {row.query[:100]}...")
        
        # Verificar tamanho das tabelas
        result = db.session.execute(text("""
            SELECT 
                schemaname,
                tablename,
                pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
                pg_total_relation_size(schemaname||'.'||tablename) as bytes
            FROM pg_tables 
            WHERE schemaname = 'public'
            ORDER BY bytes DESC;
        """))
        
        print("\n📏 Tamanho das tabelas:")
        for row in result:
            print(f"  • {row.tablename}: {row.size}")
            
    except Exception as e:
        print(f"❌ Erro na análise: {str(e)}")
        print("  Nota: pg_stat_statements pode não estar habilitado")

if __name__ == "__main__":
    from app import app
    with app.app_context():
        create_performance_indexes()
        analyze_database_performance()