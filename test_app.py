"""
Script para testar a inicialização da aplicação Flask
"""
import os

# Configurar a URL do banco de dados
os.environ['DATABASE_URL'] = 'postgresql://postgres:DygkiiZpPKBMhHItUfsBVFQfpqmQvwDz@mainline.proxy.rlwy.net:55166/railway'

try:
    print("🔧 Testando inicialização da aplicação...")
    
    from app import app, db
    from models import User
    
    print("✅ App Flask inicializado com sucesso!")
    print(f"✅ Banco de dados configurado: {app.config.get('SQLALCHEMY_DATABASE_URI', 'N/A')[:50]}...")
    
    with app.app_context():
        print("✅ Contexto da aplicação funcionando")
        
        # Testar consulta ao banco
        user_count = User.query.count()
        print(f"✅ Consulta ao banco funcionando - {user_count} usuários cadastrados")
        
        print(f"\n🚀 Aplicação pronta para executar!")
        print(f"💡 Para iniciar o servidor: python -c \"from app import app; app.run(debug=True, host='0.0.0.0', port=5000)\"")
        
except Exception as e:
    print(f"❌ Erro na inicialização: {e}")
    import traceback
    traceback.print_exc()
