"""
Script para migrar sistema de upload de fotos para base64
- Resolve problema de imagens perdidas no Railway
- Armazena imagens diretamente no banco de dados
"""
from app import app
from models import db, User
import base64
import os
from sqlalchemy import text

def migrate_profile_images_to_base64():
    """Migra sistema de fotos para base64"""
    print("🔄 Migração de Imagens de Perfil para Base64")
    print("=" * 50)
    
    with app.app_context():
        try:
            # 1. Verificar se coluna profile_image_data existe
            print("1️⃣ Verificando estrutura do banco...")
            result = db.session.execute(text(
                "SELECT column_name FROM information_schema.columns WHERE table_name='user' AND column_name='profile_image_data'"
            ))
            
            if not result.fetchone():
                print("   • Adicionando coluna profile_image_data...")
                db.session.execute(text(
                    "ALTER TABLE \"user\" ADD COLUMN profile_image_data TEXT"
                ))
                db.session.commit()
                print("   ✅ Coluna profile_image_data adicionada")
            else:
                print("   ✅ Coluna profile_image_data já existe")
            
            # 2. Converter imagens existentes
            print("\n2️⃣ Convertendo imagens existentes...")
            users_with_images = User.query.filter(
                User.profile_image.isnot(None),
                User.profile_image != 'default_profile.svg'
            ).all()
            
            converted_count = 0
            for user in users_with_images:
                image_path = os.path.join('static/images/profiles', user.profile_image)
                if os.path.exists(image_path):
                    try:
                        with open(image_path, 'rb') as img_file:
                            img_data = img_file.read()
                            img_base64 = base64.b64encode(img_data).decode('utf-8')
                            
                            # Detectar tipo de arquivo
                            if user.profile_image.lower().endswith(('.jpg', '.jpeg')):
                                img_type = 'jpeg'
                            elif user.profile_image.lower().endswith('.png'):
                                img_type = 'png'
                            elif user.profile_image.lower().endswith('.gif'):
                                img_type = 'gif'
                            else:
                                img_type = 'jpeg'  # padrão
                            
                            # Salvar no formato data URL
                            data_url = f"data:image/{img_type};base64,{img_base64}"
                            
                            # Atualizar banco usando SQL direto
                            db.session.execute(text(
                                "UPDATE \"user\" SET profile_image_data = :data WHERE id = :user_id"
                            ), {'data': data_url, 'user_id': user.id})
                            
                            converted_count += 1
                            print(f"   ✅ {user.name}: {user.profile_image} → base64")
                            
                    except Exception as e:
                        print(f"   ❌ Erro ao converter {user.name}: {e}")
                else:
                    print(f"   ⚠️ Arquivo não encontrado: {user.profile_image}")
            
            db.session.commit()
            print(f"\n✅ {converted_count} imagens convertidas com sucesso!")
            
            # 3. Criar imagem padrão base64
            print("\n3️⃣ Criando imagem padrão base64...")
            default_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="45" fill="#2D8BF7" stroke="#ffffff" stroke-width="3"/>
                <circle cx="50" cy="35" r="15" fill="#ffffff"/>
                <path d="M 25 75 Q 25 65 35 65 L 65 65 Q 75 65 75 75 L 75 85 Q 75 90 70 90 L 30 90 Q 25 90 25 85 Z" fill="#ffffff"/>
            </svg>'''
            
            default_base64 = base64.b64encode(default_svg.encode('utf-8')).decode('utf-8')
            default_data_url = f"data:image/svg+xml;base64,{default_base64}"
            
            # Salvar como constante para usar no código
            with open('default_profile_base64.py', 'w', encoding='utf-8') as f:
                f.write(f'DEFAULT_PROFILE_IMAGE_BASE64 = """{default_data_url}"""\n')
            
            print("   ✅ Imagem padrão base64 criada")
            print(f"   📁 Arquivo: default_profile_base64.py")
            
            print("\n🎉 MIGRAÇÃO CONCLUÍDA!")
            print("📋 Próximos passos:")
            print("1. Atualizar código de upload para usar base64")
            print("2. Atualizar templates para usar profile_image_data")
            print("3. Testar upload e visualização")
            
        except Exception as e:
            print(f"❌ Erro na migração: {e}")
            db.session.rollback()

if __name__ == "__main__":
    migrate_profile_images_to_base64()
