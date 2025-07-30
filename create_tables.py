#!/usr/bin/env python3
"""
Script para criar todas as tabelas no banco de dados PostgreSQL
Comando: python create_tables.py
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# Adiciona o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_database_tables():
    """Cria todas as tabelas no banco de dados"""
    
    # URL do banco de dados fornecida
    database_url = "postgresql://postgres:DygkiiZpPKBMhHItUfsBVFQfpqmQvwDz@mainline.proxy.rlwy.net:55166/railway"
    
    try:
        # Conectar ao banco de dados
        engine = create_engine(database_url)
        
        print("🔌 Conectando ao banco de dados...")
        with engine.connect() as conn:
            print("✅ Conexão estabelecida com sucesso!")
            
            # Testar a conexão
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"📊 Versão do PostgreSQL: {version}")
        
        # Importar os modelos e criar as tabelas
        print("📋 Importando modelos...")
        from app import app, db
        
        with app.app_context():
            print("🔨 Criando tabelas...")
            
            # Criar todas as tabelas
            db.create_all()
            
            print("✅ Todas as tabelas foram criadas com sucesso!")
            
            # Listar as tabelas criadas
            with engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    ORDER BY table_name;
                """))
                
                tables = [row[0] for row in result.fetchall()]
                print(f"📋 Tabelas criadas ({len(tables)}):")
                for table in tables:
                    print(f"   • {table}")
                    
    except ImportError as e:
        print(f"❌ Erro ao importar módulos: {e}")
        print("💡 Certifique-se de que todas as dependências estão instaladas.")
        return False
        
    except OperationalError as e:
        print(f"❌ Erro de conexão com o banco de dados: {e}")
        print("💡 Verifique se a URL do banco está correta e se o servidor está acessível.")
        return False
        
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False
    
    return True

def check_database_connection():
    """Verifica se é possível conectar ao banco de dados"""
    database_url = "postgresql://postgres:DygkiiZpPKBMhHItUfsBVFQfpqmQvwDz@mainline.proxy.rlwy.net:55166/railway"
    
    try:
        engine = create_engine(database_url)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"❌ Falha na conexão: {e}")
        return False

if __name__ == "__main__":
    print("🚀 SAMAPE - Criação de Tabelas do Banco de Dados")
    print("=" * 50)
    
    # Verificar conexão primeiro
    print("🔍 Verificando conexão com o banco de dados...")
    if not check_database_connection():
        print("❌ Não foi possível conectar ao banco de dados.")
        sys.exit(1)
    
    print("✅ Conexão verificada com sucesso!")
    print()
    
    # Criar as tabelas
    if create_database_tables():
        print()
        print("🎉 Processo concluído com sucesso!")
        print("💡 As tabelas estão prontas para uso.")
    else:
        print()
        print("❌ Processo falhou!")
        print("💡 Verifique os erros acima e tente novamente.")
        sys.exit(1)
