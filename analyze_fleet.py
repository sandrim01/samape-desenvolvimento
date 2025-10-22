#!/usr/bin/env python3
"""
Script para analisar o conteúdo detalhado da página de frota
"""

import os
import sys
import re
from app import app
from database import db
from models import User

def analyze_fleet_page():
    with app.app_context():
        try:
            print("=== Análise Detalhada da Página de Frota ===")
            
            with app.test_client() as client:
                # 1. Fazer login
                login_page = client.get('/login')
                csrf_match = re.search(r'<input[^>]*name="csrf_token"[^>]*value="([^"]*)"', login_page.data.decode('utf-8'))
                csrf_token = csrf_match.group(1)
                
                login_data = {
                    'username': 'teste',
                    'password': '123456',
                    'csrf_token': csrf_token
                }
                
                client.post('/login', data=login_data)
                
                # 2. Acessar frota
                fleet_response = client.get('/frota')
                fleet_content = fleet_response.data.decode('utf-8')
                
                print(f"Status da frota: {fleet_response.status_code}")
                print(f"Tamanho da resposta: {len(fleet_content)} caracteres")
                
                # 3. Procurar por elementos específicos
                print("\n=== Análise do Conteúdo ===")
                
                # Procurar por tabela de veículos
                if '<table' in fleet_content and 'vehicle-table' in fleet_content:
                    print("✓ Tabela de veículos encontrada")
                else:
                    print("✗ Tabela de veículos NÃO encontrada")
                
                # Procurar por thead
                if '<thead>' in fleet_content:
                    print("✓ Cabeçalho da tabela encontrado")
                else:
                    print("✗ Cabeçalho da tabela NÃO encontrado")
                
                # Procurar por tbody
                if '<tbody>' in fleet_content:
                    print("✓ Corpo da tabela encontrado")
                else:
                    print("✗ Corpo da tabela NÃO encontrado")
                
                # Procurar por linhas de dados (tr)
                tr_count = fleet_content.count('<tr>')
                print(f"Número de <tr> encontrados: {tr_count}")
                
                # Procurar especificamente pela placa
                if 'PQT5E89' in fleet_content:
                    print("✓ Placa PQT5E89 encontrada!")
                    # Encontrar o contexto onde aparece
                    pqt_index = fleet_content.find('PQT5E89')
                    context_start = max(0, pqt_index - 200)
                    context_end = min(len(fleet_content), pqt_index + 200)
                    context = fleet_content[context_start:context_end]
                    print(f"Contexto: ...{context}...")
                else:
                    print("✗ Placa PQT5E89 NÃO encontrada")
                
                # Procurar por outras strings relacionadas
                search_terms = ['TORO', 'VOLCANO', 'FIAT', 'vehicle', 'veículo']
                for term in search_terms:
                    count = fleet_content.lower().count(term.lower())
                    if count > 0:
                        print(f"✓ '{term}' encontrado {count} vez(es)")
                    else:
                        print(f"✗ '{term}' NÃO encontrado")
                
                # Procurar por mensagens de erro ou empty state
                if 'Nenhum veículo encontrado' in fleet_content:
                    print("✗ Mensagem 'Nenhum veículo encontrado' presente")
                else:
                    print("✓ Mensagem 'Nenhum veículo encontrado' NÃO presente")
                
                # Verificar se há JavaScript ou loading que pode estar afetando
                if 'loading' in fleet_content.lower():
                    print("⚠ Conteúdo contém indicações de loading")
                
                # Salvar conteúdo para análise manual se necessário
                if len(sys.argv) > 1 and sys.argv[1] == '--save':
                    with open('fleet_page_debug.html', 'w', encoding='utf-8') as f:
                        f.write(fleet_content)
                    print("\n✓ Conteúdo salvo em 'fleet_page_debug.html'")
                
                print(f"\n=== Primeiros 1000 caracteres da resposta ===")
                print(fleet_content[:1000])
                
        except Exception as e:
            print(f"Erro: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    analyze_fleet_page()
