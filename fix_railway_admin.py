"""
Script para atualizar senha do usuário admin no Railway
"""
import os

def fix_railway_admin():
    """Corrige a senha do usuário admin no Railway"""
    
    # URL do banco Railway
    railway_db_url = "postgresql://postgres:qUngJAyBvLWQdkmSkZEjjEoMoDVzOBnx@trolley.proxy.rlwy.net:22285/railway"
    os.environ['DATABASE_URL'] = railway_db_url
    
    print("🔧 Correção do Admin Railway")
    print("=" * 28)
    
    try:
        from app import app, db
        from models import User, UserRole
        
        with app.app_context():
            print("🔍 Procurando usuários existentes...")
            
            # Listar todos os usuários
            users = User.query.all()
            print(f"   Encontrados {len(users)} usuários:")
            
            for user in users:
                print(f"   • ID {user.id}: {user.username} - {user.name} ({user.role.value}) {'🟢' if user.active else '🔴'}")
            
            # Procurar usuário admin
            admin = User.query.filter_by(username='admin').first()
            
            if admin:
                print(f"\n✅ Admin encontrado: {admin.username}")
                print(f"   • Nome: {admin.name}")
                print(f"   • Email: {admin.email}")
                print(f"   • Ativo: {admin.active}")
                
                # Atualizar senha
                print(f"\n🔑 Atualizando senha para 'admin123'...")
                admin.set_password('admin123')
                admin.active = True  # Garantir que está ativo
                
                db.session.commit()
                
                # Testar senha
                if admin.check_password('admin123'):
                    print("✅ Senha atualizada e testada com sucesso!")
                    
                    print(f"\n🎉 ADMIN RAILWAY CORRIGIDO!")
                    print(f"🔑 Credenciais:")
                    print(f"   • Usuário: {admin.username}")
                    print(f"   • Senha: admin123")
                    print(f"   • URL: https://samape-py-desenvolvimento.up.railway.app")
                    
                    return True
                else:
                    print("❌ Falha no teste da senha")
                    return False
            else:
                print("\n❌ Usuário admin não encontrado")
                
                # Tentar encontrar outros usuários admin
                admin_users = User.query.filter_by(role=UserRole.admin).all()
                if admin_users:
                    print(f"   Encontrados {len(admin_users)} usuários admin:")
                    for user in admin_users:
                        print(f"   • {user.username} - {user.name}")
                        
                        # Atualizar o primeiro admin encontrado
                        if user == admin_users[0]:
                            print(f"\n🔧 Atualizando usuário: {user.username}")
                            user.set_password('admin123')
                            user.active = True
                            db.session.commit()
                            
                            print(f"✅ Senha atualizada para: {user.username}")
                            print(f"🔑 Use: {user.username} / admin123")
                            return True
                else:
                    print("   Nenhum usuário admin encontrado")
                    return False
                    
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if fix_railway_admin():
        print("\n💡 Agora teste o login no Railway!")
        print("https://samape-py-desenvolvimento.up.railway.app/login")
    else:
        print("\n❌ Não foi possível corrigir o admin.")
