"""
Script simples para testar login via HTTP (sem BeautifulSoup)
"""
import os
import requests
import re

BASE_URL = 'http://localhost:5000'

def test_simple_login():
    print("🔐 Teste Simples de Login")
    print("=" * 25)
    
    session = requests.Session()
    
    try:
        # 1. Acessar página de login
        print("1️⃣ Carregando página de login...")
        login_url = f"{BASE_URL}/login"
        response = session.get(login_url)
        
        if response.status_code != 200:
            print(f"❌ Erro ao carregar login: {response.status_code}")
            return False
            
        print("✅ Página de login carregada")
        
        # 2. Extrair CSRF token usando regex
        print("2️⃣ Procurando CSRF token...")
        csrf_pattern = r'name="csrf_token"[^>]*value="([^"]*)"'
        csrf_match = re.search(csrf_pattern, response.text)
        
        csrf_token = None
        if csrf_match:
            csrf_token = csrf_match.group(1)
            print(f"✅ CSRF token encontrado: {csrf_token[:20]}...")
        else:
            print("⚠️ CSRF token não encontrado, tentando sem...")
        
        # 3. Tentar login
        print("3️⃣ Enviando credenciais...")
        login_data = {
            'username': 'admin',
            'password': 'admin123'
        }
        
        if csrf_token:
            login_data['csrf_token'] = csrf_token
            
        response = session.post(login_url, data=login_data, allow_redirects=False)
        
        print(f"   Status da resposta: {response.status_code}")
        
        if response.status_code == 302:
            redirect_to = response.headers.get('Location', '')
            print(f"✅ Login bem-sucedido! Redirecionando para: {redirect_to}")
            return True
        elif response.status_code == 200:
            print("❌ Login falhou - retornou para página de login")
            
            # Verificar se há mensagens de erro na resposta
            if 'inválidos' in response.text.lower():
                print("   • Erro: Credenciais inválidas")
            elif 'csrf' in response.text.lower():
                print("   • Erro: Problema com CSRF token")
            elif 'tentativas' in response.text.lower():
                print("   • Erro: Muitas tentativas de login")
            else:
                print("   • Erro não identificado")
                
            return False
        else:
            print(f"❌ Erro inesperado: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão - servidor não responde")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def check_login_page_content():
    """Verifica o conteúdo da página de login"""
    try:
        response = requests.get(f"{BASE_URL}/login")
        if response.status_code == 200:
            content = response.text
            
            print("📄 Análise da página de login:")
            print(f"   • Tamanho: {len(content)} bytes")
            print(f"   • Contém 'username': {'username' in content}")
            print(f"   • Contém 'password': {'password' in content}")
            print(f"   • Contém 'csrf_token': {'csrf_token' in content}")
            print(f"   • Contém formulário: {'<form' in content}")
            print(f"   • Contém botão submit: {'submit' in content}")
            
            return True
        else:
            print(f"❌ Erro ao acessar login: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Teste de Login - SAMAPE")
    print("=" * 30)
    
    # Verificar servidor
    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code in [200, 302]:
            print("✅ Servidor está rodando")
            
            # Analisar página de login
            if check_login_page_content():
                print()
                # Tentar login
                if test_simple_login():
                    print("\n🎉 SUCESSO! Login funcionando!")
                else:
                    print("\n❌ FALHA no login")
            
        else:
            print(f"⚠️ Servidor responde mas com erro: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Servidor não está rodando")
        print("💡 Execute: python start_server.py")
    except Exception as e:
        print(f"❌ Erro: {e}")
