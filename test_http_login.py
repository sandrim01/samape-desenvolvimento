"""
Script para testar o login simulando exatamente o que acontece no navegador
"""
import os
import requests
from urllib.parse import urljoin

# Configurar a URL do banco de dados
os.environ['DATABASE_URL'] = 'postgresql://postgres:DygkiiZpPKBMhHItUfsBVFQfpqmQvwDz@mainline.proxy.rlwy.net:55166/railway'

BASE_URL = 'http://localhost:5000'

def test_login():
    print("🔐 Teste de Login via HTTP")
    print("=" * 30)
    
    session = requests.Session()
    
    try:
        # 1. Acessar página de login para obter CSRF token
        print("1️⃣ Acessando página de login...")
        login_url = urljoin(BASE_URL, '/login')
        response = session.get(login_url)
        
        if response.status_code == 200:
            print(f"✅ Página de login carregada (200)")
            print(f"   URL: {login_url}")
            print(f"   Tamanho: {len(response.text)} bytes")
        else:
            print(f"❌ Erro ao carregar login: {response.status_code}")
            return False
            
        # 2. Extrair CSRF token
        print("\n2️⃣ Extraindo CSRF token...")
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_token = None
        
        # Procurar pelo campo hidden do CSRF
        csrf_input = soup.find('input', {'name': 'csrf_token'})
        if csrf_input:
            csrf_token = csrf_input.get('value')
            print(f"✅ CSRF token encontrado: {csrf_token[:20]}...")
        else:
            print("❌ CSRF token não encontrado")
            # Tentar procurar de outras formas
            meta_csrf = soup.find('meta', {'name': 'csrf-token'})
            if meta_csrf:
                csrf_token = meta_csrf.get('content')
                print(f"✅ CSRF token em meta: {csrf_token[:20]}...")
            else:
                print("⚠️ Tentando login sem CSRF token...")
        
        # 3. Fazer o login
        print("\n3️⃣ Tentando fazer login...")
        login_data = {
            'username': 'admin',
            'password': 'admin123',
            'remember_me': False
        }
        
        if csrf_token:
            login_data['csrf_token'] = csrf_token
            
        response = session.post(login_url, data=login_data, allow_redirects=False)
        
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        
        if response.status_code == 302:  # Redirect = login bem-sucedido
            redirect_location = response.headers.get('Location', '')
            print(f"✅ Login bem-sucedido! Redirecionando para: {redirect_location}")
            
            # Seguir o redirect
            if redirect_location:
                if redirect_location.startswith('/'):
                    redirect_url = urljoin(BASE_URL, redirect_location)
                else:
                    redirect_url = redirect_location
                    
                dashboard_response = session.get(redirect_url)
                if dashboard_response.status_code == 200:
                    print(f"✅ Dashboard carregado com sucesso!")
                    return True
                else:
                    print(f"❌ Erro ao carregar dashboard: {dashboard_response.status_code}")
                    
        elif response.status_code == 200:
            print("❌ Login falhou - voltou para a página de login")
            # Verificar se há mensagens de erro
            soup = BeautifulSoup(response.text, 'html.parser')
            alerts = soup.find_all('div', {'class': 'alert'})
            for alert in alerts:
                print(f"   Erro: {alert.get_text().strip()}")
        else:
            print(f"❌ Erro inesperado: {response.status_code}")
            
        return False
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão - servidor não está rodando?")
        print("💡 Certifique-se de que o servidor está rodando em http://localhost:5000")
        return False
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_server_status():
    """Testa se o servidor está respondendo"""
    try:
        response = requests.get(BASE_URL, timeout=5)
        return response.status_code == 200 or response.status_code == 302
    except:
        return False

if __name__ == "__main__":
    # Verificar se servidor está rodando
    print("🔍 Verificando se servidor está rodando...")
    if test_server_status():
        print("✅ Servidor está respondendo")
        test_login()
    else:
        print("❌ Servidor não está respondendo")
        print("💡 Execute: python start_server.py")
