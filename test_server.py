#!/usr/bin/env python3
"""
Servidor de teste simples para o SAMAPE
"""

from app import create_app
import os

if __name__ == '__main__':
    app = create_app()
    
    # Configurações de debug
    app.config['DEBUG'] = True
    app.config['TESTING'] = False
    
    print("🚀 Servidor de teste SAMAPE iniciado!")
    print("📍 Acesse: http://localhost:5000")
    print("📍 Ou: http://127.0.0.1:5000")
    print("🛑 Para parar: Ctrl+C")
    
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\n👋 Servidor encerrado pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
