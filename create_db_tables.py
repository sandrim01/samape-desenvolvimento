"""
Script simples para criar as tabelas no banco de dados
"""
import os
import sys

# Configurar a URL do banco de dados
os.environ['DATABASE_URL'] = 'postgresql://postgres:DygkiiZpPKBMhHItUfsBVFQfpqmQvwDz@mainline.proxy.rlwy.net:55166/railway'

try:
    # Importar a aplicação
    from app import app, db
    
    print("🚀 SAMAPE - Criação de Tabelas do Banco de Dados")
    print("=" * 50)
    
    # Criar as tabelas dentro do contexto da aplicação
    with app.app_context():
        print("🔨 Criando todas as tabelas...")
        
        # Criar todas as tabelas definidas nos modelos
        db.create_all()
        
        print("✅ Todas as tabelas foram criadas com sucesso!")
        
        # Verificar as tabelas criadas
        from sqlalchemy import text
        result = db.session.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """))
        
        tables = [row[0] for row in result.fetchall()]
        print(f"\n📋 Tabelas criadas ({len(tables)}):")
        for table in tables:
            print(f"   • {table}")
            
        print("\n🎉 Processo concluído com sucesso!")
        print("💡 O banco de dados está pronto para uso.")

except Exception as e:
    print(f"❌ Erro ao criar tabelas: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
