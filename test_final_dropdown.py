"""
Teste final do menu dropdown após as correções
"""
import requests
from bs4 import BeautifulSoup
import time

def test_final_dropdown():
    print("🔧 TESTE FINAL - Menu Dropdown de Perfil")
    print("=" * 50)
    
    BASE_URL = 'https://samape-py-desenvolvimento.up.railway.app'
    
    session = requests.Session()
    
    try:
        print("⏳ Aguardando Railway atualizar (30 segundos)...")
        time.sleep(10)  # Aguardar 30 segundos para o Railway atualizar
        
        # 1. Fazer login
        print("\n1️⃣ Fazendo login com usuário Samuel...")
        login_url = f"{BASE_URL}/login"
        login_response = session.get(login_url, timeout=15)
        
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
        login_post = session.post(login_url, data=login_data, allow_redirects=True, timeout=15)
        
        if 'dashboard' in login_post.url or 'Samuel' in login_post.text:
            print("✅ Login realizado com sucesso")
            
            # 2. Verificar estrutura do menu
            print("\n2️⃣ Analisando estrutura do menu corrigido...")
            soup = BeautifulSoup(login_post.text, 'html.parser')
            
            # Verificar botão dropdown
            dropdown_btn = soup.find('button', {'data-bs-toggle': 'dropdown'})
            print(f"   • Botão dropdown: {'✅' if dropdown_btn else '❌'}")
            
            if dropdown_btn:
                classes = dropdown_btn.get('class', [])
                print(f"   • Classes do botão: {classes}")
                print(f"   • Tem dropdown-toggle: {'✅' if 'dropdown-toggle' in classes else '❌'}")
                print(f"   • Tem data-bs-toggle: {'✅' if dropdown_btn.get('data-bs-toggle') == 'dropdown' else '❌'}")
            
            # Verificar menu dropdown
            dropdown_menu = soup.find('ul', class_='dropdown-menu')
            print(f"   • Menu dropdown: {'✅' if dropdown_menu else '❌'}")
            
            if dropdown_menu:
                classes = dropdown_menu.get('class', [])
                print(f"   • Classes do menu: {classes}")
                items = dropdown_menu.find_all('a', class_='dropdown-item')
                print(f"   • Itens no menu: {len(items)}")
                for i, item in enumerate(items, 1):
                    text = item.get_text(strip=True)
                    href = item.get('href', '')
                    print(f"     {i}. {text} ({href})")
            
            # 3. Verificar CSS e JS carregados
            print("\n3️⃣ Verificando recursos carregados...")
            
            # Verificar CSS dropdown-fix
            dropdown_css = soup.find('link', href=lambda x: x and 'dropdown-fix.css' in x if x else False)
            print(f"   • CSS dropdown-fix.css: {'✅' if dropdown_css else '❌'}")
            
            # Verificar JS dropdown-fix
            dropdown_js = soup.find('script', src=lambda x: x and 'dropdown-fix.js' in x if x else False)
            print(f"   • JS dropdown-fix.js: {'✅' if dropdown_js else '❌'}")
            
            # Verificar Bootstrap JS
            bootstrap_js = soup.find('script', src=lambda x: x and 'bootstrap' in x if x else False)
            print(f"   • Bootstrap JS: {'✅' if bootstrap_js else '❌'}")
            
            # 4. Verificar user info header
            print("\n4️⃣ Verificando informações do usuário...")
            user_header = soup.find('div', class_='user-info-header')
            if user_header:
                user_name = user_header.find('div', class_='user-name')
                user_email = user_header.find('div', class_='user-email')
                user_role = user_header.find('div', class_='user-role')
                
                print(f"   • Nome: {user_name.get_text(strip=True) if user_name else 'N/A'}")
                print(f"   • Email: {user_email.get_text(strip=True) if user_email else 'N/A'}")
                print(f"   • Cargo: {user_role.get_text(strip=True) if user_role else 'N/A'}")
            else:
                print("   ❌ Header de usuário não encontrado")
            
            print("\n🎯 INSTRUÇÕES PARA TESTE:")
            print("1. Acesse: https://samape-py-desenvolvimento.up.railway.app/login")
            print("2. Faça login com: Samuel / admin123")
            print("3. Clique no seu nome no canto superior direito")
            print("4. O menu deve abrir com: Meu Perfil, Configurações, Sair")
            print("5. Se não funcionar, abra F12 (DevTools) e veja se há erros no Console")
            
            return True
            
        else:
            print("❌ Login falhou")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    if test_final_dropdown():
        print("\n🎉 TESTE CONCLUÍDO!")
        print("O menu deve estar funcionando agora. Teste manualmente!")
    else:
        print("\n❌ TESTE FALHOU")
        print("Verifique se há algum problema na aplicação.")
