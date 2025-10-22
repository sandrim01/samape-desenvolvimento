#!/usr/bin/env python3
"""
Script para criar a tabela CompanySettings no banco de dados
"""

import sys
import os

# Adicionar o diretório pai ao Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import db
from models import CompanySettings
from app import app

def create_company_settings_table():
    """Cria a tabela CompanySettings no banco de dados"""
    try:
        with app.app_context():
            # Criar a tabela CompanySettings
            CompanySettings.__table__.create(db.engine, checkfirst=True)
            print("✅ Tabela CompanySettings criada com sucesso!")
            
            # Verificar se já existe um registro de empresa
            existing_company = CompanySettings.query.first()
            if not existing_company:
                # Criar registro inicial com dados padrão da SAMAPE
                initial_company = CompanySettings(
                    company_name="SAMAPE - Serviços Automotivos e Manutenção de Equipamentos",
                    trade_name="SAMAPE",
                    document="00.000.000/0001-00",
                    address="Rua Example, 123",
                    city="São Paulo",
                    state="SP",
                    zip_code="00000-000",
                    phone="(11) 0000-0000",
                    email="contato@samape.com.br",
                    website="https://www.samape.com.br",
                    description="Serviços automotivos especializados e manutenção de equipamentos industriais.",
                    updated_by=1  # Assumindo que existe um usuário admin com ID 1
                )
                
                db.session.add(initial_company)
                db.session.commit()
                print("✅ Dados iniciais da empresa inseridos com sucesso!")
            else:
                print("ℹ️  Dados da empresa já existem no banco de dados.")
                
    except Exception as e:
        print(f"❌ Erro ao criar tabela CompanySettings: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Criando tabela CompanySettings...")
    success = create_company_settings_table()
    
    if success:
        print("✅ Migração concluída com sucesso!")
    else:
        print("❌ Erro durante a migração!")
        sys.exit(1)