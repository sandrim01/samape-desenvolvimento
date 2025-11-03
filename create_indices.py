"""
Script para criar índices de performance no banco de dados
Execute: python create_performance_indices.py
"""

from app import app, db
from sqlalchemy import text

# Lista de índices para criar
INDICES = [
    # Service Order - queries mais comuns
    "CREATE INDEX IF NOT EXISTS idx_service_order_status ON service_order(status);",
    "CREATE INDEX IF NOT EXISTS idx_service_order_client_id ON service_order(client_id);",
    "CREATE INDEX IF NOT EXISTS idx_service_order_responsible_id ON service_order(responsible_id);",
    "CREATE INDEX IF NOT EXISTS idx_service_order_created_at ON service_order(created_at DESC);",
    "CREATE INDEX IF NOT EXISTS idx_service_order_closed_at ON service_order(closed_at DESC);",
    
    # Financial Entry - relatórios e filtros
    "CREATE INDEX IF NOT EXISTS idx_financial_entry_status ON financial_entry(status);",
    "CREATE INDEX IF NOT EXISTS idx_financial_entry_type ON financial_entry(type);",
    "CREATE INDEX IF NOT EXISTS idx_financial_entry_due_date ON financial_entry(due_date);",
    "CREATE INDEX IF NOT EXISTS idx_financial_entry_payment_date ON financial_entry(payment_date);",
    "CREATE INDEX IF NOT EXISTS idx_financial_entry_service_order_id ON financial_entry(service_order_id);",
    
    # Parts List - consultas de peças
    "CREATE INDEX IF NOT EXISTS idx_parts_list_service_order_id ON parts_list(service_order_id);",
    "CREATE INDEX IF NOT EXISTS idx_parts_list_status ON parts_list(status);",
    "CREATE INDEX IF NOT EXISTS idx_parts_list_created_at ON parts_list(created_at DESC);",
    
    # Client - buscas e ordenação
    "CREATE INDEX IF NOT EXISTS idx_client_name ON client(name);",
    "CREATE INDEX IF NOT EXISTS idx_client_active ON client(active);",
    
    # Equipment - filtros
    "CREATE INDEX IF NOT EXISTS idx_equipment_client_id ON equipment(client_id);",
    "CREATE INDEX IF NOT EXISTS idx_equipment_status ON equipment(status);",
    
    # User - login e consultas
    "CREATE INDEX IF NOT EXISTS idx_user_email ON user(email);",
    "CREATE INDEX IF NOT EXISTS idx_user_active ON user(active);",
    
    # Vehicle - frota
    "CREATE INDEX IF NOT EXISTS idx_vehicle_status ON vehicle(status) WHERE status IS NOT NULL;",
    "CREATE INDEX IF NOT EXISTS idx_vehicle_type ON vehicle(type) WHERE type IS NOT NULL;",
    
    # Action Log - auditoria (apenas se necessário)
    "CREATE INDEX IF NOT EXISTS idx_action_log_timestamp ON action_log(timestamp DESC);",
    "CREATE INDEX IF NOT EXISTS idx_action_log_user_id ON action_log(user_id);",
]

def create_indices():
    """Cria todos os índices no banco de dados"""
    print("🔧 Criando índices de performance...")
    print(f"📊 Total de índices a criar: {len(INDICES)}\n")
    
    with app.app_context():
        created = 0
        skipped = 0
        errors = 0
        
        for idx, sql in enumerate(INDICES, 1):
            try:
                # Extrair nome do índice para exibição
                index_name = sql.split("idx_")[1].split(" ")[0] if "idx_" in sql else f"index_{idx}"
                
                print(f"[{idx}/{len(INDICES)}] Criando índice: idx_{index_name}...", end=" ")
                
                db.session.execute(text(sql))
                db.session.commit()
                
                print("✅ Criado")
                created += 1
                
            except Exception as e:
                error_msg = str(e)
                
                # Se o índice já existe, não é erro
                if "already exists" in error_msg.lower():
                    print("⏭️  Já existe")
                    skipped += 1
                else:
                    print(f"❌ Erro: {error_msg}")
                    errors += 1
                    
                db.session.rollback()
    
    # Resumo final
    print("\n" + "="*60)
    print("📈 RESUMO DA CRIAÇÃO DE ÍNDICES")
    print("="*60)
    print(f"✅ Criados com sucesso: {created}")
    print(f"⏭️  Já existiam: {skipped}")
    print(f"❌ Erros: {errors}")
    print(f"📊 Total processados: {len(INDICES)}")
    print("="*60)
    
    if errors == 0:
        print("\n🎉 Todos os índices foram criados/verificados com sucesso!")
        print("⚡ O sistema deve estar mais rápido agora!")
    else:
        print(f"\n⚠️  Houve {errors} erro(s). Verifique os detalhes acima.")
    
    return created, skipped, errors

def analyze_indices():
    """Mostra os índices existentes (apenas PostgreSQL)"""
    print("\n🔍 Analisando índices existentes...")
    
    with app.app_context():
        try:
            # Query para listar índices no PostgreSQL
            query = text("""
                SELECT 
                    schemaname,
                    tablename,
                    indexname,
                    indexdef
                FROM pg_indexes
                WHERE schemaname = 'public'
                    AND indexname LIKE 'idx_%'
                ORDER BY tablename, indexname;
            """)
            
            result = db.session.execute(query)
            indices = result.fetchall()
            
            if indices:
                print(f"\n📋 Encontrados {len(indices)} índices customizados:\n")
                current_table = None
                
                for idx in indices:
                    table = idx[1]
                    index_name = idx[2]
                    
                    if table != current_table:
                        if current_table is not None:
                            print()
                        print(f"📁 Tabela: {table}")
                        current_table = table
                    
                    print(f"   • {index_name}")
            else:
                print("ℹ️  Nenhum índice customizado encontrado.")
                
        except Exception as e:
            print(f"⚠️  Não foi possível analisar índices: {e}")

if __name__ == "__main__":
    print("="*60)
    print("🚀 SAMAPE - Otimização de Performance do Banco de Dados")
    print("="*60)
    print()
    
    # Criar índices
    created, skipped, errors = create_indices()
    
    # Mostrar índices existentes
    if created > 0 or skipped > 0:
        analyze_indices()
    
    print("\n✅ Script concluído!")
