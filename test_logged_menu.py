"""
Script para testar e corrigir menu de perfil
"""
import requests
from bs4 import BeautifulSoup

def test_logged_menu():
    print("🔧 Teste do Menu Logado - Railway")
    print("=" * 40)
    
    BASE_URL = 'https://samape-py-desenvolvimento.up.railway.app'
    
    session = requests.Session()
    
    try:
        # 1. Fazer login primeiro
        print("1️⃣ Fazendo login...")
        login_url = f"{BASE_URL}/login"
        login_response = session.get(login_url, timeout=10)
        
        if login_response.status_code != 200:
            print(f"❌ Erro ao carregar login: {login_response.status_code}")
            return False
        
        # Extrair CSRF token
        soup = BeautifulSoup(login_response.text, 'html.parser')
        csrf_input = soup.find('input', {'name': 'csrf_token'})
        csrf_token = csrf_input['value'] if csrf_input else None
        
        # Dados de login
        login_data = {
            'username': 'Samuel',
            'password': 'admin123'
        }
        
        if csrf_token:
            login_data['csrf_token'] = csrf_token
        
        # Fazer login
        login_post = session.post(login_url, data=login_data, allow_redirects=True, timeout=10)
        
        if 'dashboard' in login_post.url or login_post.status_code == 200:
            print("✅ Login realizado com sucesso")
            
            # 2. Verificar o menu na página logada
            print("\n2️⃣ Analisando menu na página logada...")
            soup = BeautifulSoup(login_post.text, 'html.parser')
            
            # Procurar pelo botão do menu
            dropdown_btn = soup.find('button', {'data-bs-toggle': 'dropdown'})
            dropdown_menu = soup.find('ul', class_='dropdown-menu')
            
            print(f"   • Botão dropdown encontrado: {'✅' if dropdown_btn else '❌'}")
            print(f"   • Menu dropdown encontrado: {'✅' if dropdown_menu else '❌'}")
            
            # Verificar Bootstrap JS
            bootstrap_js = soup.find('script', src=lambda x: x and 'bootstrap' in x if x else False)
            print(f"   • Bootstrap JS carregado: {'✅' if bootstrap_js else '❌'}")
            
            # Verificar inicialização de dropdowns
            init_script = soup.find('script', string=lambda x: x and 'bootstrap.Dropdown' in x if x else False)
            print(f"   • Dropdown inicializado: {'✅' if init_script else '❌'}")
            
            if dropdown_btn:
                print(f"\n🔍 Detalhes do botão:")
                print(f"   • Classes: {dropdown_btn.get('class', [])}")
                print(f"   • Atributos: {dict(dropdown_btn.attrs)}")
            
            if dropdown_menu:
                print(f"\n🔍 Detalhes do menu:")
                print(f"   • Classes: {dropdown_menu.get('class', [])}")
                items = dropdown_menu.find_all('a', class_='dropdown-item')
                print(f"   • Itens do menu: {len(items)}")
                for item in items:
                    print(f"     - {item.get_text(strip=True)}")
            
            return True
        else:
            print("❌ Login falhou")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    test_logged_menu()
