"""
Script para inserir dados iniciais no banco de dados
"""
import os
from datetime import datetime

# Configurar a URL do banco de dados
os.environ['DATABASE_URL'] = 'postgresql://postgres:DygkiiZpPKBMhHItUfsBVFQfpqmQvwDz@mainline.proxy.rlwy.net:55166/railway'

try:
    from app import app, db
    from models import User, UserRole, SystemSettings, SequenceCounter
    
    print("🚀 SAMAPE - Inserção de Dados Iniciais")
    print("=" * 40)
    
    with app.app_context():
        # Verificar se já existe usuário admin
        admin_user = User.query.filter_by(username='admin').first()
        
        if not admin_user:
            print("👤 Criando usuário administrador...")
            admin_user = User(
                username='admin',
                name='Administrador do Sistema',
                email='admin@samape.com.br',
                role=UserRole.admin,
                active=True
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            print("✅ Usuário admin criado (login: admin, senha: admin123)")
        else:
            print("ℹ️  Usuário admin já existe")
            
        # Configurações do sistema
        settings_data = [
            ('empresa_nome', 'SAMAPE'),
            ('empresa_cnpj', '00.000.000/0001-00'),
            ('empresa_endereco', 'Endereço da Empresa'),
            ('empresa_telefone', '(00) 0000-0000'),
            ('empresa_email', 'contato@samape.com.br'),
            ('sistema_versao', '1.0.0'),
            ('nfe_ambiente', 'homologacao'),  # homologacao ou producao
            ('nfe_serie', '1'),
        ]
        
        print("⚙️  Criando configurações do sistema...")
        for name, value in settings_data:
            setting = SystemSettings.query.filter_by(name=name).first()
            if not setting:
                setting = SystemSettings(name=name, value=value, updated_by=admin_user.id)
                db.session.add(setting)
                print(f"   • {name}: {value}")
        
        # Contadores de sequência
        sequences_data = [
            ('ordem_servico', 'OS', 1, 6, 'Numeração de Ordens de Serviço'),
            ('nfe', 'NFE', 1, 9, 'Numeração de Notas Fiscais Eletrônicas'),
            ('orcamento', 'ORC', 1, 6, 'Numeração de Orçamentos'),
            ('pedido_compra', 'PC', 1, 6, 'Numeração de Pedidos de Compra'),
        ]
        
        print("🔢 Criando contadores de sequência...")
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
                print(f"   • {name} ({prefix}): iniciando em {current}")
        
        # Salvar todas as alterações
        db.session.commit()
        
        print("\n✅ Dados iniciais inseridos com sucesso!")
        print("\n📋 Resumo:")
        print("   • Usuário admin: admin / admin123")
        print("   • Configurações do sistema criadas")
        print("   • Contadores de sequência inicializados")
        print("\n🎉 Sistema pronto para uso!")
        
except Exception as e:
    print(f"❌ Erro ao inserir dados iniciais: {e}")
    import traceback
    traceback.print_exc()
