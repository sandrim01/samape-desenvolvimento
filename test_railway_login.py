"""
Script para testar login na aplicação Railway
"""
import requests
import re

BASE_URL = 'https://samape-py-desenvolvimento.up.railway.app'

def test_railway_login():
    print("🚂 Teste de Login - Railway App")
    print("=" * 35)
    
    session = requests.Session()
    
    try:
        # 1. Acessar página de login
        print("1️⃣ Carregando página de login...")
        login_url = f"{BASE_URL}/login"
        response = session.get(login_url, timeout=10)
        
        if response.status_code != 200:
            print(f"❌ Erro ao carregar login: {response.status_code}")
            if response.status_code == 502:
                print("   • Erro 502: Aplicação pode estar com problemas")
            elif response.status_code == 503:
                print("   • Erro 503: Serviço indisponível")
            return False
            
        print(f"✅ Página de login carregada")
        print(f"   • Status: {response.status_code}")
        print(f"   • Tamanho: {len(response.text)} bytes")
        
        # 2. Analisar página
        print("\n2️⃣ Analisando página de login...")
        content = response.text
        
        has_form = '<form' in content
        has_username = 'username' in content or 'name="username"' in content
        has_password = 'password' in content or 'name="password"' in content
        has_csrf = 'csrf_token' in content
        
        print(f"   • Contém formulário: {has_form}")
        print(f"   • Campo username: {has_username}")
        print(f"   • Campo password: {has_password}")
        print(f"   • CSRF token: {has_csrf}")
        
        if not (has_form and has_username and has_password):
            print("❌ Página de login não contém os elementos necessários")
            return False
        
        # 3. Extrair CSRF token
        print("\n3️⃣ Extraindo CSRF token...")
        csrf_token = None
        csrf_pattern = r'name="csrf_token"[^>]*value="([^"]*)"'
        csrf_match = re.search(csrf_pattern, content)
        
        if csrf_match:
            csrf_token = csrf_match.group(1)
            print(f"✅ CSRF token encontrado: {csrf_token[:20]}...")
        else:
            print("⚠️ CSRF token não encontrado, tentando sem...")
        
        # 4. Tentar login
        print("\n4️⃣ Tentando fazer login...")
        print("   • Usuário: admin")
        print("   • Senha: admin123")
        
        login_data = {
            'username': 'admin',
            'password': 'admin123'
        }
        
        if csrf_token:
            login_data['csrf_token'] = csrf_token
            
        response = session.post(login_url, data=login_data, allow_redirects=False, timeout=10)
        
        print(f"   • Status da resposta: {response.status_code}")
        
        if response.status_code == 302:
            redirect_to = response.headers.get('Location', '')
            print(f"✅ Login bem-sucedido!")
            print(f"   • Redirecionando para: {redirect_to}")
            
            # Tentar acessar o dashboard
            if redirect_to:
                if redirect_to.startswith('/'):
                    dashboard_url = f"{BASE_URL}{redirect_to}"
                else:
                    dashboard_url = redirect_to
                    
                print(f"\n5️⃣ Acessando dashboard...")
                dashboard_response = session.get(dashboard_url, timeout=10)
                
                if dashboard_response.status_code == 200:
                    print(f"✅ Dashboard carregado com sucesso!")
                    print(f"   • URL: {dashboard_url}")
                    return True
                elif dashboard_response.status_code == 302:
                    print(f"⚠️ Dashboard redirecionou novamente")
                    new_redirect = dashboard_response.headers.get('Location', '')
                    print(f"   • Nova localização: {new_redirect}")
                else:
                    print(f"❌ Erro ao carregar dashboard: {dashboard_response.status_code}")
            
        elif response.status_code == 200:
            print("❌ Login falhou - retornou para página de login")
            
            # Verificar se há mensagens de erro
            if 'inválidos' in response.text.lower() or 'invalid' in response.text.lower():
                print("   • Erro: Credenciais inválidas")
            elif 'csrf' in response.text.lower():
                print("   • Erro: Problema com CSRF token")
            elif 'tentativas' in response.text.lower() or 'attempts' in response.text.lower():
                print("   • Erro: Muitas tentativas de login")
            else:
                print("   • Erro não identificado na resposta")
                
        else:
            print(f"❌ Erro inesperado: {response.status_code}")
            
        return False
        
    except requests.exceptions.Timeout:
        print("❌ Timeout - aplicação não respondeu a tempo")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão - não foi possível conectar")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def check_railway_app_status():
    """Verifica o status da aplicação Railway"""
    print("🔍 Verificando status da aplicação...")
    
    try:
        response = requests.get(BASE_URL, timeout=10)
        
        print(f"   • Status: {response.status_code}")
        print(f"   • Tamanho: {len(response.text)} bytes")
        
        if response.status_code == 200:
            print("✅ Aplicação está funcionando")
            return True
        elif response.status_code == 302:
            redirect = response.headers.get('Location', '')
            print(f"✅ Aplicação redirecionando para: {redirect}")
            return True
        else:
            print(f"⚠️ Aplicação respondeu com status: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout - aplicação não responde")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Aplicação não está acessível")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    print("🚂 SAMAPE Railway - Teste de Login")
    print("=" * 40)
    print(f"🌐 URL: {BASE_URL}")
    print()
    
    if check_railway_app_status():
        print()
        if test_railway_login():
            print("\n🎉 SUCESSO! Login funcionando no Railway!")
        else:
            print("\n❌ FALHA no login do Railway")
    else:
        print("\n❌ Aplicação Railway não está acessível")
