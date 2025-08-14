#!/usr/bin/env python3
"""
Script de diagnóstico para identificar problemas no sistema SAMAPE
"""

import requests
import sys
from urllib.parse import urljoin

def test_server_endpoints():
    """Testa os principais endpoints do servidor"""
    
    base_url = "http://127.0.0.1:5000"
    
    # Lista de endpoints para testar
    endpoints = [
        "/",           # Página inicial
        "/login",      # Login
        "/stock",      # Estoque
        "/dashboard",  # Dashboard
    ]
    
    print("🔍 DIAGNÓSTICO DO SISTEMA SAMAPE")
    print("=" * 50)
    
    server_running = False
    
    for endpoint in endpoints:
        url = urljoin(base_url, endpoint)
        try:
            print(f"📍 Testando: {url}")
            response = requests.get(url, timeout=5, allow_redirects=True)
            
            if response.status_code == 200:
                print(f"✅ OK - Status: {response.status_code}")
                server_running = True
            elif response.status_code in [302, 301]:
                print(f"🔄 Redirect - Status: {response.status_code} -> {response.headers.get('Location', 'N/A')}")
                server_running = True
            else:
                print(f"⚠️ Aviso - Status: {response.status_code}")
                server_running = True
                
        except requests.exceptions.ConnectionError:
            print(f"❌ ERRO - Servidor não responde em {url}")
        except requests.exceptions.Timeout:
            print(f"⏱️ TIMEOUT - {url} demorou para responder")
        except Exception as e:
            print(f"❌ ERRO - {url}: {str(e)}")
    
    print("\n" + "=" * 50)
    
    if server_running:
        print("✅ SERVIDOR FUNCIONANDO CORRETAMENTE")
        print(f"🌐 Acesse: {base_url}")
        return True
    else:
        print("❌ PROBLEMAS DETECTADOS NO SERVIDOR")
        print("💡 Verifique se o servidor está rodando:")
        print("   python main.py")
        return False

def check_database_connection():
    """Verifica conexão com banco de dados"""
    try:
        import os
        from sqlalchemy import create_engine, text
        
        print("\n🗄️ TESTANDO CONEXÃO COM BANCO DE DADOS")
        print("-" * 40)
        
        db_url = os.environ.get("DATABASE_URL", "postgresql://postgres:qUngJAyBvLWQdkmSkZEjjEoMoDVzOBnx@trolley.proxy.rlwy.net:22285/railway")
        
        engine = create_engine(db_url)
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Conexão com banco de dados: OK")
            return True
            
    except Exception as e:
        print(f"❌ Erro na conexão com banco: {str(e)}")
        return False

def check_recent_logs():
    """Verifica logs recentes se existirem"""
    print("\n📋 VERIFICANDO LOGS RECENTES")
    print("-" * 40)
    
    try:
        # Verificar se há arquivos de log
        import os
        import glob
        
        log_patterns = ["*.log", "app.log", "error.log", "flask.log"]
        logs_found = []
        
        for pattern in log_patterns:
            logs_found.extend(glob.glob(pattern))
            
        if logs_found:
            print(f"📄 Logs encontrados: {', '.join(logs_found)}")
            
            # Mostrar últimas linhas do primeiro log
            with open(logs_found[0], 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                if lines:
                    print("\n📄 Últimas linhas do log:")
                    for line in lines[-5:]:
                        print(f"   {line.strip()}")
        else:
            print("ℹ️ Nenhum arquivo de log encontrado")
            
    except Exception as e:
        print(f"⚠️ Erro ao verificar logs: {str(e)}")

if __name__ == "__main__":
    print("🚀 Iniciando diagnóstico completo...\n")
    
    # Testes principais
    server_ok = test_server_endpoints()
    db_ok = check_database_connection()
    check_recent_logs()
    
    print("\n" + "=" * 50)
    print("📊 RESUMO DO DIAGNÓSTICO")
    print("=" * 50)
    
    if server_ok and db_ok:
        print("✅ SISTEMA FUNCIONANDO NORMALMENTE")
        print("🎉 Todos os componentes principais estão operacionais")
        print("\n🔗 Links úteis:")
        print("   • Sistema: http://127.0.0.1:5000")
        print("   • Estoque: http://127.0.0.1:5000/stock")
        print("   • Login: http://127.0.0.1:5000/login")
    else:
        print("⚠️ PROBLEMAS IDENTIFICADOS")
        if not server_ok:
            print("   • Servidor Flask não está respondendo")
        if not db_ok:
            print("   • Problemas na conexão com banco de dados")
        
        print("\n💡 SOLUÇÕES SUGERIDAS:")
        print("   1. Verifique se o servidor está rodando: python main.py")
        print("   2. Verifique variáveis de ambiente do banco de dados")
        print("   3. Confirme se as dependências estão instaladas")
        
    print("\n🔧 Para mais detalhes, verifique os logs do sistema.")
