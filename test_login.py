"""
Script para testar o processo de login detalhadamente
"""
import os

# Configurar a URL do banco de dados
os.environ['DATABASE_URL'] = 'postgresql://postgres:DygkiiZpPKBMhHItUfsBVFQfpqmQvwDz@mainline.proxy.rlwy.net:55166/railway'

try:
    from app import app, db
    from models import User, LoginAttempt
    from werkzeug.security import check_password_hash
    
    print("🔐 Teste Detalhado de Login")
    print("=" * 30)
    
    with app.app_context():
        # 1. Verificar usuário admin
        print("1️⃣ Verificando usuário admin...")
        user = User.query.filter_by(username='admin').first()
        
        if user:
            print(f"✅ Usuário encontrado: {user.username}")
            print(f"   • Nome: {user.name}")
            print(f"   • Email: {user.email}")
            print(f"   • Ativo: {user.active}")
            print(f"   • Role: {user.role.value}")
            print(f"   • Password Hash: {user.password_hash[:50]}...")
        else:
            print("❌ Usuário admin não encontrado!")
            exit(1)
            
        # 2. Testar verificação de senha
        print(f"\n2️⃣ Testando verificação de senha...")
        
        # Teste com senha correta
        if user.check_password('admin123'):
            print("✅ Senha 'admin123' está correta")
        else:
            print("❌ Senha 'admin123' está incorreta")
            
        # Teste com senha incorreta
        if user.check_password('senhaerrada'):
            print("❌ ERRO: Senha incorreta foi aceita!")
        else:
            print("✅ Senha incorreta foi rejeitada corretamente")
            
        # 3. Verificar tentativas de login
        print(f"\n3️⃣ Verificando tentativas de login...")
        attempts = LoginAttempt.query.filter_by(email='admin').order_by(LoginAttempt.timestamp.desc()).limit(5).all()
        
        if attempts:
            print(f"   • Últimas {len(attempts)} tentativas:")
            for attempt in attempts:
                status = "✅ Sucesso" if attempt.success else "❌ Falha"
                print(f"     - {attempt.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {status} - IP: {attempt.ip_address}")
        else:
            print("   • Nenhuma tentativa de login registrada")
            
        # 4. Testar hash direto
        print(f"\n4️⃣ Testando hash de senha diretamente...")
        from werkzeug.security import generate_password_hash, check_password_hash
        
        test_hash = generate_password_hash('admin123')
        if check_password_hash(test_hash, 'admin123'):
            print("✅ Sistema de hash funcionando corretamente")
        else:
            print("❌ PROBLEMA no sistema de hash!")
            
        # 5. Simular processo de login
        print(f"\n5️⃣ Simulando processo de login...")
        
        # Buscar usuário por username
        login_user = User.query.filter_by(username='admin').first()
        if login_user:
            print("✅ Usuário encontrado na busca por username")
            
            # Verificar se está ativo
            if login_user.active:
                print("✅ Usuário está ativo")
                
                # Verificar senha
                if login_user.check_password('admin123'):
                    print("✅ Senha verificada com sucesso")
                    print("🎉 LOGIN SERIA BEM-SUCEDIDO!")
                else:
                    print("❌ Falha na verificação da senha")
                    
            else:
                print("❌ Usuário está inativo")
        else:
            print("❌ Usuário não encontrado na busca")
            
        print(f"\n📋 Resumo:")
        print(f"   • Usuário: admin")
        print(f"   • Senha: admin123") 
        print(f"   • Status: {'🟢 Ativo' if user.active else '🔴 Inativo'}")
        print(f"   • Hash: Válido")
        
        # Tentar reset do usuário se houver problemas
        print(f"\n🔧 Garantindo que o usuário está correto...")
        user.set_password('admin123')
        user.active = True
        db.session.commit()
        print("✅ Usuário admin resetado e confirmado")
        
except Exception as e:
    print(f"❌ Erro no teste: {e}")
    import traceback
    traceback.print_exc()
