"""
Script para criar usuário admin no banco da aplicação Railway
"""
import os
import requests

# URL da aplicação Railway
RAILWAY_URL = 'https://samape-py-desenvolvimento.up.railway.app'

def create_admin_user_via_api():
    """Tenta criar usuário admin via requisições HTTP"""
    print("👤 Criando usuário admin na aplicação Railway...")
    
    try:
        # Verificar se existe uma rota para criar usuário admin
        test_urls = [
            f"{RAILWAY_URL}/setup",
            f"{RAILWAY_URL}/install",
            f"{RAILWAY_URL}/admin/setup",
            f"{RAILWAY_URL}/create-admin"
        ]
        
        session = requests.Session()
        
        for url in test_urls:
            try:
                response = session.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"✅ Encontrado endpoint de setup: {url}")
                    return url
            except:
                continue
                
        print("❌ Nenhum endpoint de setup encontrado")
        return None
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

def test_common_credentials():
    """Testa credenciais comuns que podem existir"""
    print("🔑 Testando credenciais comuns...")
    
    common_creds = [
        ('admin', 'admin'),
        ('admin', 'admin123'),
        ('admin', 'password'),
        ('admin', '123456'),
        ('administrator', 'admin'),
        ('root', 'root'),
        ('samape', 'samape'),
        ('demo', 'demo')
    ]
    
    session = requests.Session()
    login_url = f"{RAILWAY_URL}/login"
    
    for username, password in common_creds:
        try:
            print(f"   Testando: {username} / {password}")
            
            # Obter página de login
            response = session.get(login_url)
            if response.status_code != 200:
                continue
                
            # Tentar login
            login_data = {
                'username': username,
                'password': password
            }
            
            response = session.post(login_url, data=login_data, allow_redirects=False)
            
            if response.status_code == 302:
                print(f"✅ SUCESSO! Credenciais funcionando: {username} / {password}")
                return username, password
                
        except Exception as e:
            print(f"      Erro: {e}")
            continue
    
    print("❌ Nenhuma credencial comum funcionou")
    return None, None

def check_database_status():
    """Verifica informações sobre o banco de dados"""
    print("🗃️ Verificando status do banco...")
    
    try:
        # Tentar acessar rotas que podem dar informações
        test_urls = [
            f"{RAILWAY_URL}/health",
            f"{RAILWAY_URL}/status",
            f"{RAILWAY_URL}/info",
            f"{RAILWAY_URL}/debug"
        ]
        
        for url in test_urls:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"✅ Informações disponíveis em: {url}")
                    if 'database' in response.text.lower() or 'user' in response.text.lower():
                        print(f"   Contém informações relevantes")
            except:
                continue
                
    except Exception as e:
        print(f"❌ Erro: {e}")

def suggest_solutions():
    """Sugere soluções para o problema"""
    print("\n💡 Possíveis soluções:")
    print()
    print("1️⃣ **Banco de dados vazio:**")
    print("   • O banco Railway pode não ter sido inicializado")
    print("   • Necessário executar migration/setup")
    print()
    print("2️⃣ **Credenciais diferentes:**")
    print("   • O usuário admin pode ter senha diferente")
    print("   • Pode haver outro usuário padrão")
    print()
    print("3️⃣ **Configuração diferente:**")
    print("   • A aplicação Railway pode estar usando configurações diferentes")
    print("   • Variáveis de ambiente podem estar diferentes")
    print()
    print("🔧 **Ações recomendadas:**")
    print("   • Verificar logs da aplicação Railway")
    print("   • Executar script de inicialização no Railway")
    print("   • Verificar variáveis de ambiente do Railway")
    print("   • Acessar diretamente o banco de dados Railway")

if __name__ == "__main__":
    print("🚂 SAMAPE Railway - Diagnóstico de Login")
    print("=" * 45)
    print(f"🌐 URL: {RAILWAY_URL}")
    print()
    
    # Testar se aplicação está funcionando
    try:
        response = requests.get(RAILWAY_URL, timeout=10)
        if response.status_code in [200, 302]:
            print("✅ Aplicação Railway está funcionando")
            print()
            
            # Verificar banco
            check_database_status()
            print()
            
            # Testar credenciais
            username, password = test_common_credentials()
            print()
            
            if username and password:
                print(f"🎉 Login funcionando com: {username} / {password}")
            else:
                # Procurar endpoints de setup
                setup_url = create_admin_user_via_api()
                print()
                suggest_solutions()
                
        else:
            print(f"❌ Aplicação Railway com problemas: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro ao acessar Railway: {e}")
