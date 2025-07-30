"""
Script para diagnosticar problemas com Flask-Login
"""
import os

# Configurar a URL do banco de dados
os.environ['DATABASE_URL'] = 'postgresql://postgres:DygkiiZpPKBMhHItUfsBVFQfpqmQvwDz@mainline.proxy.rlwy.net:55166/railway'

def test_flask_login():
    print("🔐 Diagnóstico Flask-Login")
    print("=" * 25)
    
    try:
        from app import app, login_manager, db
        from models import User
        from flask_login import login_user, current_user
        
        with app.app_context():
            # 1. Testar o user_loader
            print("1️⃣ Testando user_loader...")
            
            admin = User.query.filter_by(username='admin').first()
            if admin:
                print(f"✅ Admin encontrado: ID {admin.id}")
                
                # Testar se o user_loader funciona
                loaded_user = login_manager.user_loader(str(admin.id))
                if loaded_user:
                    print(f"✅ User loader funcionando: {loaded_user.username}")
                else:
                    print("❌ User loader retornando None")
                    
            # 2. Testar contexto de request
            print("\n2️⃣ Testando contexto de request...")
            with app.test_request_context():
                print(f"   • current_user.is_authenticated: {current_user.is_authenticated}")
                print(f"   • current_user.is_anonymous: {current_user.is_anonymous}")
                
                # Tentar fazer login programaticamente
                if admin:
                    result = login_user(admin)
                    print(f"   • login_user result: {result}")
                    print(f"   • current_user após login: {current_user}")
                    print(f"   • is_authenticated após login: {current_user.is_authenticated}")
                    
        # 3. Verificar configurações do Flask
        print("\n3️⃣ Verificando configurações...")
        print(f"   • SECRET_KEY definida: {'SECRET_KEY' in app.config}")
        print(f"   • SECRET_KEY: {app.config.get('SECRET_KEY', 'N/A')[:20]}...")
        print(f"   • SESSION_COOKIE_SECURE: {app.config.get('SESSION_COOKIE_SECURE', 'N/A')}")
        print(f"   • SESSION_COOKIE_HTTPONLY: {app.config.get('SESSION_COOKIE_HTTPONLY', 'N/A')}")
        
        # 4. Verificar login_manager
        print("\n4️⃣ Verificando login_manager...")
        print(f"   • login_view: {login_manager.login_view}")
        print(f"   • login_message: {login_manager.login_message}")
        print(f"   • user_loader registrado: {hasattr(login_manager, '_user_callback')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

def fix_flask_login():
    """Tenta corrigir problemas comuns do Flask-Login"""
    print("\n🔧 Tentando corrigir Flask-Login...")
    
    try:
        from app import app
        
        # Desabilitar HTTPS para desenvolvimento
        app.config['SESSION_COOKIE_SECURE'] = False
        app.config['SESSION_COOKIE_HTTPONLY'] = True
        app.config['SESSION_COOKIE_SAMESITE'] = None
        
        # Garantir que secret key está definida
        if not app.config.get('SECRET_KEY'):
            app.config['SECRET_KEY'] = 'desenvolvimento_key_temporaria'
            
        print("✅ Configurações de sessão ajustadas para desenvolvimento")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao corrigir: {e}")
        return False

if __name__ == "__main__":
    if test_flask_login():
        fix_flask_login()
        print("\n💡 Configurações ajustadas. Reinicie o servidor e tente novamente.")
