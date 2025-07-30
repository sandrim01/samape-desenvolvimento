"""
Script automatizado para resolver problemas de login
"""
import os

# Configurar a URL do banco de dados
os.environ['DATABASE_URL'] = 'postgresql://postgres:DygkiiZpPKBMhHItUfsBVFQfpqmQvwDz@mainline.proxy.rlwy.net:55166/railway'

def fix_login_issues():
    try:
        from app import app, db
        from models import User, UserRole
        
        print("🔧 SAMAPE - Correção Automática de Login")
        print("=" * 40)
        
        with app.app_context():
            # 1. Verificar/Criar usuário admin
            print("1️⃣ Verificando usuário admin...")
            
            admin_user = User.query.filter_by(username='admin').first()
            
            if admin_user:
                print("✅ Usuário admin encontrado")
                # Garantir que está configurado corretamente
                admin_user.username = 'admin'
                admin_user.name = 'Administrador do Sistema'
                admin_user.email = 'admin@samape.com.br'
                admin_user.role = UserRole.admin
                admin_user.active = True
                admin_user.set_password('admin123')
                
                print("🔄 Configurações do admin atualizadas")
            else:
                print("❌ Usuário admin não encontrado. Criando...")
                admin_user = User(
                    username='admin',
                    name='Administrador do Sistema',
                    email='admin@samape.com.br',
                    role=UserRole.admin,
                    active=True
                )
                admin_user.set_password('admin123')
                db.session.add(admin_user)
                print("✅ Usuário admin criado")
            
            db.session.commit()
            
            # 2. Testar senha
            print("\n2️⃣ Testando senha...")
            if admin_user.check_password('admin123'):
                print("✅ Senha funcionando corretamente")
            else:
                print("❌ Problema com senha. Redefinindo...")
                admin_user.set_password('admin123')
                db.session.commit()
                print("✅ Senha redefinida")
            
            # 3. Verificar se usuário está ativo
            print("\n3️⃣ Verificando status do usuário...")
            if admin_user.active:
                print("✅ Usuário está ativo")
            else:
                print("❌ Usuário inativo. Ativando...")
                admin_user.active = True
                db.session.commit()
                print("✅ Usuário ativado")
            
            # 4. Limpar tentativas de login falhas
            print("\n4️⃣ Limpando tentativas de login...")
            from models import LoginAttempt
            LoginAttempt.query.filter_by(email='admin', success=False).delete()
            db.session.commit()
            print("✅ Tentativas de login limpas")
            
            # 5. Teste final
            print("\n5️⃣ Teste final...")
            test_user = User.query.filter_by(username='admin').first()
            
            if (test_user and 
                test_user.active and 
                test_user.check_password('admin123') and
                test_user.role == UserRole.admin):
                
                print("🎉 SUCESSO! Login configurado corretamente")
                print("\n📋 Credenciais de acesso:")
                print("   • Usuário: admin")
                print("   • Senha: admin123")
                print("   • URL: http://localhost:5000")
                
                return True
            else:
                print("❌ Ainda há problemas. Verifique manualmente.")
                return False
                
    except Exception as e:
        print(f"❌ Erro durante a correção: {e}")
        import traceback
        traceback.print_exc()
        return False

def start_server():
    """Inicia o servidor Flask"""
    try:
        from app import app
        print("\n🚀 Iniciando servidor Flask...")
        print("   • URL: http://localhost:5000")
        print("   • Pressione Ctrl+C para parar")
        print("   • Use as credenciais: admin / admin123")
        
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except KeyboardInterrupt:
        print("\n✅ Servidor parado pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")

if __name__ == "__main__":
    # Corrigir problemas de login
    if fix_login_issues():
        print("\n" + "="*50)
        print("✅ Correções aplicadas com sucesso!")
        print("💡 Agora você pode tentar fazer login novamente.")
        print("="*50)
        
        # Perguntar se quer iniciar o servidor
        try:
            resposta = input("\n🔍 Deseja iniciar o servidor agora? (s/n): ").lower().strip()
            if resposta in ['s', 'sim', 'y', 'yes']:
                start_server()
            else:
                print("\n💡 Para iniciar o servidor manualmente:")
                print("   python -c \"from app import app; app.run(debug=True, host='0.0.0.0', port=5000)\"")
        except KeyboardInterrupt:
            print("\n👋 Até logo!")
    else:
        print("\n❌ Não foi possível corrigir automaticamente.")
        print("💡 Execute os scripts de diagnóstico individuais para mais detalhes.")
