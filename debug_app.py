"""
Script de debug para identificar problemas na aplicação
"""
import os
import sys
import traceback

# Configurar a URL do banco de dados
os.environ['DATABASE_URL'] = 'postgresql://postgres:DygkiiZpPKBMhHItUfsBVFQfpqmQvwDz@mainline.proxy.rlwy.net:55166/railway'

print("🔍 Debug do Sistema SAMAPE")
print("=" * 30)

print(f"🐍 Python: {sys.version}")
print(f"📁 Diretório: {os.getcwd()}")

# Teste 1: Importações básicas
print("\n1️⃣ Testando importações básicas...")
try:
    from database import db
    print("✅ database.py importado")
except Exception as e:
    print(f"❌ Erro em database.py: {e}")
    traceback.print_exc()

try:
    from models import User
    print("✅ models.py importado")
except Exception as e:
    print(f"❌ Erro em models.py: {e}")
    traceback.print_exc()

# Teste 2: Aplicação Flask
print("\n2️⃣ Testando aplicação Flask...")
try:
    from app import app
    print("✅ app.py importado")
    print(f"   App: {app}")
    print(f"   Configuração: {app.config.get('SQLALCHEMY_DATABASE_URI', 'N/A')[:50]}...")
except Exception as e:
    print(f"❌ Erro em app.py: {e}")
    traceback.print_exc()

# Teste 3: Contexto da aplicação
print("\n3️⃣ Testando contexto da aplicação...")
try:
    with app.app_context():
        print("✅ Contexto da aplicação funcionando")
        user_count = User.query.count()
        print(f"✅ Consulta ao banco funcionando - {user_count} usuários")
except Exception as e:
    print(f"❌ Erro no contexto: {e}")
    traceback.print_exc()

# Teste 4: Usuário admin
print("\n4️⃣ Testando usuário admin...")
try:
    with app.app_context():
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print(f"✅ Admin encontrado: {admin.username}")
            print(f"   Email: {admin.email}")
            print(f"   Ativo: {admin.active}")
            
            # Testar senha
            if admin.check_password('admin123'):
                print("✅ Senha correta")
            else:
                print("❌ Senha incorreta")
        else:
            print("❌ Admin não encontrado")
except Exception as e:
    print(f"❌ Erro ao verificar admin: {e}")
    traceback.print_exc()

# Teste 5: Routes
print("\n5️⃣ Testando rotas...")
try:
    from routes import register_routes
    print("✅ routes.py importado")
except Exception as e:
    print(f"❌ Erro em routes.py: {e}")
    traceback.print_exc()

print("\n" + "="*50)
print("🔍 Debug concluído!")
