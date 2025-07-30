"""
Script para inicializar o banco de dados Railway
"""
import os

def setup_railway_database():
    """Configura o banco de dados Railway com tabelas e usuário admin"""
    
    # URL do banco Railway (do config.py)
    railway_db_url = "postgresql://postgres:qUngJAyBvLWQdkmSkZEjjEoMoDVzOBnx@trolley.proxy.rlwy.net:22285/railway"
    
    # Configurar variável de ambiente
    os.environ['DATABASE_URL'] = railway_db_url
    
    print("🚂 Configuração do Banco Railway")
    print("=" * 35)
    print(f"🗃️ Banco: trolley.proxy.rlwy.net:22285")
    
    try:
        # Importar aplicação com a nova URL
        from app import app, db
        from models import User, UserRole, SystemSettings, SequenceCounter
        
        print("✅ Conectado ao banco Railway")
        
        with app.app_context():
            print("\n1️⃣ Criando todas as tabelas...")
            
            # Criar todas as tabelas
            db.create_all()
            print("✅ Tabelas criadas com sucesso")
            
            print("\n2️⃣ Verificando usuário admin...")
            
            # Verificar se já existe admin
            admin_user = User.query.filter_by(username='admin').first()
            
            if admin_user:
                print("ℹ️  Usuário admin já existe")
                # Garantir que a senha está correta
                admin_user.set_password('admin123')
                admin_user.active = True
                print("✅ Senha do admin atualizada")
            else:
                print("👤 Criando usuário admin...")
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
            
            print("\n3️⃣ Configurando sistema...")
            
            # Configurações básicas
            settings_data = [
                ('empresa_nome', 'SAMAPE'),
                ('empresa_cnpj', '00.000.000/0001-00'),
                ('empresa_endereco', 'Endereço da Empresa'),
                ('empresa_telefone', '(00) 0000-0000'),
                ('empresa_email', 'contato@samape.com.br'),
                ('sistema_versao', '1.0.0'),
            ]
            
            for name, value in settings_data:
                setting = SystemSettings.query.filter_by(name=name).first()
                if not setting:
                    setting = SystemSettings(name=name, value=value, updated_by=admin_user.id)
                    db.session.add(setting)
            
            # Contadores de sequência
            sequences_data = [
                ('ordem_servico', 'OS', 1, 6, 'Numeração de Ordens de Serviço'),
                ('nfe', 'NFE', 1, 9, 'Numeração de Notas Fiscais Eletrônicas'),
                ('orcamento', 'ORC', 1, 6, 'Numeração de Orçamentos'),
            ]
            
            for name, prefix, current, padding, description in sequences_data:
                counter = SequenceCounter.query.filter_by(name=name).first()
                if not counter:
                    counter = SequenceCounter(
                        name=name,
                        prefix=prefix,
                        current_value=current,
                        padding=padding,
                        description=description
                    )
                    db.session.add(counter)
            
            # Salvar tudo
            db.session.commit()
            
            print("✅ Configurações criadas")
            
            print("\n4️⃣ Testando configuração...")
            
            # Teste final
            test_user = User.query.filter_by(username='admin').first()
            if test_user and test_user.check_password('admin123'):
                print("✅ Login testado com sucesso")
                
                print("\n🎉 BANCO RAILWAY CONFIGURADO!")
                print("=" * 35)
                print("🔑 Credenciais de acesso:")
                print("   • Usuário: admin")
                print("   • Senha: admin123")
                print("   • URL: https://samape-py-desenvolvimento.up.railway.app")
                
                return True
            else:
                print("❌ Falha no teste de login")
                return False
                
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if setup_railway_database():
        print("\n💡 Agora você pode fazer login na aplicação Railway!")
        print("   https://samape-py-desenvolvimento.up.railway.app/login")
    else:
        print("\n❌ Configuração falhou. Verifique os erros acima.")
