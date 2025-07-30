"""
Script para iniciar o servidor Flask com debug detalhado
"""
import os

# Configurar a URL do banco de dados
os.environ['DATABASE_URL'] = 'postgresql://postgres:DygkiiZpPKBMhHItUfsBVFQfpqmQvwDz@mainline.proxy.rlwy.net:55166/railway'

print("🚀 Iniciando Servidor SAMAPE")
print("=" * 30)

try:
    from app import app
    
    print("✅ Aplicação carregada com sucesso")
    print(f"📋 Configurações:")
    print(f"   • Debug: {app.debug}")
    print(f"   • Host: 0.0.0.0")
    print(f"   • Porta: 5000")
    print(f"   • URL: http://localhost:5000")
    
    print(f"\n🔑 Credenciais de acesso:")
    print(f"   • Usuário: admin")
    print(f"   • Senha: admin123")
    
    print(f"\n📡 Iniciando servidor...")
    print(f"   (Pressione Ctrl+C para parar)")
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        use_reloader=False  # Evitar problemas de reload
    )
    
except KeyboardInterrupt:
    print("\n✅ Servidor parado pelo usuário")
except Exception as e:
    print(f"❌ Erro ao iniciar servidor: {e}")
    import traceback
    traceback.print_exc()
