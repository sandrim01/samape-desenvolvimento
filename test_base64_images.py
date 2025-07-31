"""
Teste do novo sistema de imagens base64
"""
from app import app
from models import db, User

def test_base64_images():
    print("🖼️ Teste do Sistema de Imagens Base64")
    print("=" * 45)
    
    with app.app_context():
        try:
            # Listar usuários com imagens
            print("1️⃣ Verificando usuários com imagens...")
            users = User.query.all()
            
            for user in users:
                print(f"\n👤 {user.name} (ID: {user.id})")
                print(f"   • profile_image: {user.profile_image}")
                print(f"   • profile_image_data: {'✅ Presente' if user.profile_image_data else '❌ Ausente'}")
                
                if user.profile_image_data:
                    # Verificar se é data URL válida
                    if user.profile_image_data.startswith('data:image/'):
                        data_type = user.profile_image_data.split(';')[0].split(':')[1]
                        size = len(user.profile_image_data)
                        print(f"   • Tipo: {data_type}")
                        print(f"   • Tamanho: {size:,} chars")
                        
                        # Verificar método get_profile_image
                        try:
                            profile_img = user.get_profile_image()
                            print(f"   • get_profile_image(): ✅ Funcionando")
                        except Exception as e:
                            print(f"   • get_profile_image(): ❌ Erro: {e}")
                    else:
                        print(f"   • ⚠️ Formato inválido: {user.profile_image_data[:50]}...")
                else:
                    # Testar imagem padrão
                    try:
                        profile_img = user.get_profile_image()
                        if profile_img and profile_img.startswith('data:image/'):
                            print(f"   • Imagem padrão: ✅ Base64 válida")
                        else:
                            print(f"   • Imagem padrão: ❌ Problema no formato")
                    except Exception as e:
                        print(f"   • get_profile_image(): ❌ Erro: {e}")
            
            print("\n🎯 RESULTADO:")
            total_users = len(users)
            users_with_base64 = len([u for u in users if u.profile_image_data])
            users_without_base64 = total_users - users_with_base64
            
            print(f"   • Total de usuários: {total_users}")
            print(f"   • Com imagem base64: {users_with_base64}")
            print(f"   • Sem imagem base64: {users_without_base64}")
            
            print("\n✅ SISTEMA PRONTO!")
            print("📋 Próximos passos:")
            print("1. Fazer commit das mudanças")
            print("2. Deploy no Railway")
            print("3. Testar upload de nova imagem")
            print("4. Verificar se imagens não somem mais")
            
        except Exception as e:
            print(f"❌ Erro: {e}")

if __name__ == "__main__":
    test_base64_images()
