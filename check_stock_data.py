#!/usr/bin/env python3
"""
Script para verificar os dados da tabela stock_item
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import StockItem, StockItemType, StockItemStatus
from database import db

def check_stock_items():
    """Verifica os dados da tabela stock_item"""
    
    with app.app_context():
        try:
            print("🔍 Verificando dados da tabela stock_item...")
            print("=" * 60)
            
            # Contar total de itens
            total_items = StockItem.query.count()
            print(f"📊 Total de itens no estoque: {total_items}")
            
            if total_items == 0:
                print("❌ Nenhum item encontrado no estoque!")
                print("\n💡 Vamos criar alguns itens de teste...")
                create_test_items()
                return
            
            # Listar todos os itens
            items = StockItem.query.all()
            
            print("\n📋 Lista de itens:")
            for item in items:
                print(f"  • ID: {item.id}")
                print(f"    Nome: {item.name}")
                print(f"    Tipo: {item.type}")
                print(f"    Quantidade: {item.quantity}")
                print(f"    Unidade: {getattr(item, 'unit', 'N/A')}")
                print(f"    Status: {item.status}")
                print(f"    Localização: {item.location or 'N/A'}")
                print("-" * 40)
            
            # Verificar por tipo
            print("\n📈 Estatísticas por tipo:")
            for item_type in StockItemType:
                count = StockItem.query.filter_by(type=item_type).count()
                print(f"  • {item_type.value}: {count} itens")
                
        except Exception as e:
            print(f"❌ Erro ao verificar dados: {str(e)}")
            import traceback
            traceback.print_exc()

def create_test_items():
    """Cria alguns itens de teste"""
    try:
        # EPIs de teste
        epi_items = [
            {
                'name': 'Capacete de Segurança',
                'description': 'Capacete de segurança branco com jugular',
                'type': StockItemType.epi,
                'quantity': 50,
                'unit': 'UN',
                'price': 25.90,
                'min_quantity': 10,
                'location': 'Almoxarifado A - Prateleira 1',
                'status': StockItemStatus.disponivel
            },
            {
                'name': 'Luva de Látex',
                'description': 'Luva de látex descartável tamanho M',
                'type': StockItemType.epi,
                'quantity': 200,
                'unit': 'PAR',
                'price': 1.50,
                'min_quantity': 50,
                'location': 'Almoxarifado A - Prateleira 2',
                'status': StockItemStatus.disponivel
            },
            {
                'name': 'Óculos de Proteção',
                'description': 'Óculos de proteção transparente',
                'type': StockItemType.epi,
                'quantity': 8,
                'unit': 'UN',
                'price': 15.90,
                'min_quantity': 15,
                'location': 'Almoxarifado A - Prateleira 3',
                'status': StockItemStatus.baixo
            }
        ]
        
        # Ferramentas de teste
        tool_items = [
            {
                'name': 'Chave de Fenda Phillips',
                'description': 'Chave de fenda phillips 6mm',
                'type': StockItemType.ferramenta,
                'quantity': 25,
                'unit': 'UN',
                'price': 12.90,
                'min_quantity': 5,
                'location': 'Almoxarifado B - Gaveta 1',
                'status': StockItemStatus.disponivel
            },
            {
                'name': 'Martelo de Bola',
                'description': 'Martelo de bola 500g cabo de madeira',
                'type': StockItemType.ferramenta,
                'quantity': 15,
                'unit': 'UN',
                'price': 35.90,
                'min_quantity': 3,
                'location': 'Almoxarifado B - Gaveta 2',
                'status': StockItemStatus.disponivel
            }
        ]
        
        print("➕ Criando itens de teste...")
        
        for item_data in epi_items + tool_items:
            item = StockItem(**item_data, created_by=1)  # Assumindo admin user ID = 1
            db.session.add(item)
        
        db.session.commit()
        print("✅ Itens de teste criados com sucesso!")
        
        # Verificar novamente
        check_stock_items()
        
    except Exception as e:
        print(f"❌ Erro ao criar itens de teste: {str(e)}")
        db.session.rollback()

if __name__ == "__main__":
    print("🔍 Verificando dados de estoque")
    print("=" * 60)
    
    check_stock_items()
