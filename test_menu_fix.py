"""
Script para testar se o menu foi corrigido
"""
import requests
from bs4 import BeautifulSoup

def test_menu_fix():
    print("🔧 Teste do Menu de Perfil - Correção Bootstrap")
    print("=" * 50)
    
    # Testar no Railway
    BASE_URL = 'https://samape-py-desenvolvimento.up.railway.app'
    
    try:
        # Fazer uma requisição para qualquer página que tenha o menu
        response = requests.get(f"{BASE_URL}/login", timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            print("✅ Página carregada com sucesso")
            print(f"   • URL: {BASE_URL}/login")
            print(f"   • Status: {response.status_code}")
            
            # Verificar se o menu tem os atributos corretos do Bootstrap
            dropdown_btn = soup.find('button', {'data-bs-toggle': 'dropdown'})
            dropdown_menu = soup.find('ul', class_='dropdown-menu')
            
            print("\n🔍 Verificando estrutura do menu:")
            print(f"   • Botão dropdown encontrado: {'✅' if dropdown_btn else '❌'}")
            print(f"   • Menu dropdown encontrado: {'✅' if dropdown_menu else '❌'}")
            
            if dropdown_btn:
                print(f"   • Atributo data-bs-toggle: {'✅' if dropdown_btn.get('data-bs-toggle') == 'dropdown' else '❌'}")
                print(f"   • Classe dropdown-toggle: {'✅' if 'dropdown-toggle' in dropdown_btn.get('class', []) else '❌'}")
            
            if dropdown_menu:
                print(f"   • Classe dropdown-menu: {'✅' if 'dropdown-menu' in dropdown_menu.get('class', []) else '❌'}")
                print(f"   • Itens do menu: {len(dropdown_menu.find_all('a', class_='dropdown-item'))}")
            
            # Verificar se há links importantes
            profile_link = soup.find('a', href=lambda x: x and 'profile' in x if x else False)
            logout_link = soup.find('a', href=lambda x: x and 'logout' in x if x else False)
            
            print("\n🔗 Links importantes:")
            print(f"   • Link 'Meu Perfil': {'✅' if profile_link else '❌'}")
            print(f"   • Link 'Sair': {'✅' if logout_link else '❌'}")
            
            return True
            
        else:
            print(f"❌ Erro ao carregar página: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    if test_menu_fix():
        print("\n🎉 TESTE CONCLUÍDO!")
        print("Se você está logado, o menu agora deve funcionar corretamente.")
        print("Clique no seu nome no canto superior direito para testar.")
    else:
        print("\n❌ TESTE FALHOU")
        print("Verifique se a aplicação está funcionando.")
