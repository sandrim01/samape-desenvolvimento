"""
Script para verificar o status do banco de dados
"""
import os

# Configurar a URL do banco de dados
os.environ['DATABASE_URL'] = 'postgresql://postgres:DygkiiZpPKBMhHItUfsBVFQfpqmQvwDz@mainline.proxy.rlwy.net:55166/railway'

try:
    from app import app, db
    from models import User, Client, Equipment, ServiceOrder, Supplier, Part, Vehicle
    from sqlalchemy import text
    
    print("🔍 SAMAPE - Verificação do Banco de Dados")
    print("=" * 45)
    
    with app.app_context():
        # Verificar conexão
        print("🔌 Testando conexão...")
        result = db.session.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        print(f"✅ PostgreSQL: {version.split(',')[0]}")
        
        # Listar todas as tabelas
        print("\n📋 Tabelas no banco de dados:")
        result = db.session.execute(text("""
            SELECT table_name, 
                   (SELECT COUNT(*) FROM information_schema.columns 
                    WHERE table_name = t.table_name AND table_schema = 'public') as column_count
            FROM information_schema.tables t
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """))
        
        tables = result.fetchall()
        for table_name, column_count in tables:
            print(f"   • {table_name:25} ({column_count} colunas)")
        
        # Verificar dados nas principais tabelas
        print(f"\n📊 Resumo dos dados:")
        
        counts = [
            ("Usuários", User.query.count()),
            ("Clientes", Client.query.count()),
            ("Equipamentos", Equipment.query.count()),
            ("Ordens de Serviço", ServiceOrder.query.count()),
            ("Fornecedores", Supplier.query.count()),
            ("Peças/Produtos", Part.query.count()),
            ("Veículos", Vehicle.query.count()),
        ]
        
        for entity, count in counts:
            print(f"   • {entity:20}: {count:>5} registros")
            
        # Verificar usuário admin
        print(f"\n👤 Usuários cadastrados:")
        users = User.query.all()
        for user in users:
            print(f"   • {user.username:15} - {user.name:25} ({user.role.value})")
            
        print(f"\n✅ Banco de dados está funcionando corretamente!")
        print(f"📝 Total de tabelas: {len(tables)}")
        
except Exception as e:
    print(f"❌ Erro ao verificar banco: {e}")
    import traceback
    traceback.print_exc()
