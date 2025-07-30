"""
Script para verificar e corrigir o usuário admin
"""
import os

# Configurar a URL do banco de dados
os.environ['DATABASE_URL'] = 'postgresql://postgres:DygkiiZpPKBMhHItUfsBVFQfpqmQvwDz@mainline.proxy.rlwy.net:55166/railway'

try:
    from app import app, db
    from models import User, UserRole
    
    print("🔍 Verificando usuário admin...")
    
    with app.app_context():
        # Verificar se existe usuário admin
        admin_user = User.query.filter_by(username='admin').first()
        
        if admin_user:
            print(f"✅ Usuário admin encontrado:")
            print(f"   • ID: {admin_user.id}")
            print(f"   • Username: {admin_user.username}")
            print(f"   • Nome: {admin_user.name}")
            print(f"   • Email: {admin_user.email}")
            print(f"   • Role: {admin_user.role.value}")
            print(f"   • Ativo: {admin_user.active}")
            
            # Testar a senha
            print(f"\n🔑 Testando senha 'admin123'...")
            if admin_user.check_password('admin123'):
                print("✅ Senha está correta!")
            else:
                print("❌ Senha está incorreta. Redefinindo...")
                admin_user.set_password('admin123')
                db.session.commit()
                print("✅ Senha redefinida para 'admin123'")
                
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
            db.session.commit()
            print("✅ Usuário admin criado com sucesso!")
            
        # Listar todos os usuários
        print(f"\n👥 Todos os usuários no sistema:")
        users = User.query.all()
        for user in users:
            status = "🟢 Ativo" if user.active else "🔴 Inativo"
            print(f"   • {user.username:15} - {user.name:25} ({user.role.value}) {status}")
            
        print(f"\n✅ Verificação concluída!")
        print(f"💡 Credenciais de acesso:")
        print(f"   • Usuário: admin")
        print(f"   • Senha: admin123")
        
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
