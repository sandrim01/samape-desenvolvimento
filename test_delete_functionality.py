#!/usr/bin/env python3
"""
Script para testar a exclusão de itens de estoque
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import StockItem, StockMovement, User
from datetime import datetime

def test_delete_functionality():
    with app.app_context():
        print("=== TESTE DE EXCLUSÃO DE ITEM DE ESTOQUE ===")
        
        # Verificar se há itens para testar
        items = StockItem.query.all()
        print(f"\n📊 Total de itens no banco: {len(items)}")
        
        if not items:
            print("❌ Nenhum item encontrado para teste")
            return
        
        for item in items:
            movements = StockMovement.query.filter_by(stock_item_id=item.id).all()
            print(f"\n🔍 Item: {item.name} (ID: {item.id})")
            print(f"   Movimentações: {len(movements)}")
            
            if movements:
                print("   Status: ❌ Não pode ser excluído (tem movimentações)")
                for mov in movements:
                    print(f"   - Movimentação ID {mov.id}: Qtd {mov.quantity}")
            else:
                print("   Status: ✅ Pode ser excluído (sem movimentações)")
        
        # Testar exclusão simulada
        items_without_movements = [item for item in items 
                                  if StockMovement.query.filter_by(stock_item_id=item.id).count() == 0]
        
        print(f"\n📋 Itens que podem ser excluídos: {len(items_without_movements)}")
        
        if items_without_movements:
            test_item = items_without_movements[0]
            print(f"\n🧪 Teste simulado de exclusão:")
            print(f"   Item: {test_item.name}")
            print(f"   ID: {test_item.id}")
            print(f"   ✅ Simulação: Item seria excluído com sucesso")
        else:
            print("\n⚠️ Todos os itens possuem movimentações, não podem ser excluídos")
            print("   Para testar, crie um item novo primeiro")
        
        print("\n=== FIM DO TESTE ===")

if __name__ == '__main__':
    test_delete_functionality()
