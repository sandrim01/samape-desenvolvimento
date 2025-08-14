#!/usr/bin/env python3
"""
Migração para adicionar coluna 'unit' à tabela stock_item
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from database import db
from sqlalchemy import text

def add_unit_column():
    """Adiciona a coluna 'unit' à tabela stock_item"""
    
    with app.app_context():
        try:
            print("🔧 Iniciando migração da coluna 'unit'...")
            
            # Verificar se a coluna já existe
            check_query = """
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'stock_item' AND column_name = 'unit'
            """
            
            result = db.session.execute(text(check_query)).fetchone()
            
            if result:
                print("✅ Coluna 'unit' já existe na tabela stock_item")
                return
            
            print("➕ Adicionando coluna 'unit' à tabela stock_item...")
            
            # Adicionar a coluna unit com valor padrão 'UN'
            alter_query = """
            ALTER TABLE stock_item 
            ADD COLUMN unit VARCHAR(20) DEFAULT 'UN'
            """
            
            db.session.execute(text(alter_query))
            
            # Atualizar registros existentes com valor padrão
            update_query = """
            UPDATE stock_item 
            SET unit = 'UN' 
            WHERE unit IS NULL
            """
            
            db.session.execute(text(update_query))
            db.session.commit()
            
            print("✅ Coluna 'unit' adicionada com sucesso!")
            print("✅ Registros existentes atualizados com valor padrão 'UN'")
            
        except Exception as e:
            print(f"❌ Erro durante a migração: {str(e)}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    print("🚀 Executando migração da coluna 'unit'")
    print("=" * 50)
    
    add_unit_column()
    
    print("=" * 50)
    print("✅ Migração concluída!")
