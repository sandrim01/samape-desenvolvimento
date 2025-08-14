#!/usr/bin/env python3
"""
Script para testar a criação de itens de estoque
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import StockItem, StockItemType, StockItemStatus, User
from forms import StockItemForm
from flask import Flask, request
from datetime import datetime

def test_stock_creation():
    with app.app_context():
        print("=== TESTE DE CRIAÇÃO DE ITEM DE ESTOQUE ===")
        
        # Verificar se os enums estão funcionando
        print("\n1. Testando enums:")
        try:
            print(f"StockItemType.epi: {StockItemType.epi}")
            print(f"StockItemType.ferramenta: {StockItemType.ferramenta}")
            print(f"StockItemStatus.disponivel: {StockItemStatus.disponivel}")
            print("✅ Enums funcionando")
        except Exception as e:
            print(f"❌ Erro com enums: {e}")
            return
        
        # Testar formulário
        print("\n2. Testando formulário:")
        try:
            form_data = {
                'name': 'Capacete de Segurança - TESTE',
                'description': 'Capacete para teste',
                'type': 'epi',
                'quantity': 10,
                'unit': 'UN',
                'unit_cost': 25.50,
                'minimum_quantity': 5,
                'location': 'Depósito A',
                'status': 'disponivel',
                'supplier_id': 0,
                'expiry_date': '',
                'ca_number': 'CA-12345'
            }
            
            # Simular request com dados do formulário
            with app.test_request_context(method='POST', data=form_data):
                form = StockItemForm()
                form.type.choices = [(t.name, t.value) for t in StockItemType]
                form.status.choices = [(s.name, s.value) for s in StockItemStatus]
                
                print(f"Dados do form: {form_data}")
                print(f"Form válido: {form.validate()}")
                if not form.validate():
                    print(f"Erros de validação: {form.errors}")
                else:
                    print("✅ Formulário válido")
                    
        except Exception as e:
            print(f"❌ Erro ao testar formulário: {e}")
            return
        
        # Testar criação direta no banco
        print("\n3. Testando criação direta:")
        try:
            # Buscar um usuário para ser o criador
            user = User.query.first()
            if not user:
                print("❌ Nenhum usuário encontrado no banco")
                return
            
            stock_item = StockItem(
                name='Item de Teste Direto',
                description='Teste direto no banco',
                type=StockItemType.ferramenta,
                quantity=5,
                unit='UN',
                price=15.00,
                min_quantity=2,
                location='Teste',
                status=StockItemStatus.disponivel,
                created_by=user.id
            )
            
            db.session.add(stock_item)
            db.session.commit()
            
            print(f"✅ Item criado com ID: {stock_item.id}")
            
            # Limpar o teste
            db.session.delete(stock_item)
            db.session.commit()
            print("✅ Item de teste removido")
            
        except Exception as e:
            print(f"❌ Erro ao criar item diretamente: {e}")
            db.session.rollback()
        
        print("\n=== FIM DO TESTE ===")

if __name__ == '__main__':
    test_stock_creation()
