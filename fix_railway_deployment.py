#!/usr/bin/env python3
"""
Script para corrigir problemas de deployment no Railway
Remove vestígios do Replit e configura corretamente para Railway
"""

import os
import subprocess
import sys
from pathlib import Path

def fix_railway_deployment():
    print("🚂 CORREÇÃO DO DEPLOYMENT RAILWAY")
    print("=" * 40)
    
    # 1. Verificar se estamos no diretório correto
    if not Path("app.py").exists():
        print("❌ Execute este script na raiz do projeto SAMAPE")
        return False
    
    # 2. Remover arquivos problemáticos
    problematic_files = [
        ".replit",
        ".replit.nix", 
        "replit.nix",
        "poetry.lock",
        "Pipfile",
        "Pipfile.lock"
    ]
    
    print("\n🗑️  Removendo arquivos problemáticos...")
    for file in problematic_files:
        file_path = Path(file)
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"   ✅ Removido: {file}")
            except Exception as e:
                print(f"   ❌ Erro ao remover {file}: {e}")
    
    # 3. Verificar pyproject.toml
    print("\n📝 Verificando pyproject.toml...")
    try:
        with open("pyproject.toml", "r", encoding="utf-8") as f:
            content = f.read()
        
        if "repl-nix-workspace" in content:
            print("   ⚠️  Encontrado nome antigo do Replit")
            content = content.replace("repl-nix-workspace", "samape-desenvolvimento")
            content = content.replace("0.1.0", "1.0.0")
            content = content.replace("Add your description here", "Sistema SAMAPE - Gestão de Equipamentos e Ordens de Serviço")
            
            with open("pyproject.toml", "w", encoding="utf-8") as f:
                f.write(content)
            print("   ✅ pyproject.toml corrigido")
        else:
            print("   ✅ pyproject.toml já está correto")
    
    except Exception as e:
        print(f"   ❌ Erro ao verificar pyproject.toml: {e}")
    
    # 4. Criar/verificar Procfile para Railway
    print("\n🚀 Criando Procfile para Railway...")
    procfile_content = "web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120"
    
    try:
        with open("Procfile", "w", encoding="utf-8") as f:
            f.write(procfile_content)
        print("   ✅ Procfile criado")
    except Exception as e:
        print(f"   ❌ Erro ao criar Procfile: {e}")
    
    # 5. Criar requirements.txt alternativo para Railway
    print("\n📦 Criando requirements.txt...")
    requirements = [
        "Flask>=3.1.0",
        "Flask-SQLAlchemy>=3.1.1", 
        "Flask-Login>=0.6.3",
        "Flask-WTF>=1.2.2",
        "WTForms>=3.2.1",
        "psycopg2-binary>=2.9.10",
        "gunicorn>=23.0.0",
        "email-validator>=2.2.0",
        "Werkzeug>=3.1.3",
        "MarkupSafe>=3.0.2",
        "SQLAlchemy>=2.0.40"
    ]
    
    try:
        with open("requirements.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(requirements))
        print("   ✅ requirements.txt criado")
    except Exception as e:
        print(f"   ❌ Erro ao criar requirements.txt: {e}")
    
    # 6. Verificar app.py para problemas de PORT
    print("\n⚙️  Verificando configuração de PORT...")
    try:
        with open("app.py", "r", encoding="utf-8") as f:
            app_content = f.read()
        
        # Procurar por configuração de porta
        if "port=int(os.environ.get('PORT'" not in app_content:
            print("   ⚠️  Configuração de PORT pode estar incorreta")
            
            # Adicionar configuração correta no final do arquivo
            if "if __name__ == '__main__':" in app_content:
                # Substituir o bloco principal
                lines = app_content.split('\n')
                new_lines = []
                skip_main = False
                
                for line in lines:
                    if line.strip().startswith("if __name__ == '__main__':"):
                        new_lines.extend([
                            "",
                            "if __name__ == '__main__':",
                            "    import os",
                            "    port = int(os.environ.get('PORT', 5000))",
                            "    debug = os.environ.get('FLASK_ENV') == 'development'",
                            "    app.run(host='0.0.0.0', port=port, debug=debug)"
                        ])
                        skip_main = True
                        break
                    new_lines.append(line)
                
                if skip_main:
                    app_content = '\n'.join(new_lines)
                    
                    with open("app.py", "w", encoding="utf-8") as f:
                        f.write(app_content)
                    print("   ✅ Configuração de PORT corrigida")
            else:
                print("   ✅ Configuração de PORT já está correta")
        else:
            print("   ✅ Configuração de PORT já está correta")
            
    except Exception as e:
        print(f"   ❌ Erro ao verificar app.py: {e}")
    
    # 7. Atualizar .gitignore
    print("\n📝 Atualizando .gitignore...")
    gitignore_additions = [
        "",
        "# === RAILWAY DEPLOYMENT ===",
        "*.log",
        ".env.local",
        ".env.production",
        "",
        "# Replit vestígios (não usar)",
        ".replit*",
        "replit.nix",
        "poetry.lock",
        "Pipfile*"
    ]
    
    try:
        with open(".gitignore", "r", encoding="utf-8") as f:
            gitignore_content = f.read()
        
        if "RAILWAY DEPLOYMENT" not in gitignore_content:
            with open(".gitignore", "a", encoding="utf-8") as f:
                f.write('\n'.join(gitignore_additions))
            print("   ✅ .gitignore atualizado")
        else:
            print("   ✅ .gitignore já está atualizado")
            
    except Exception as e:
        print(f"   ❌ Erro ao atualizar .gitignore: {e}")
    
    print("\n🎯 CORREÇÃO CONCLUÍDA!")
    print("\n📋 Próximos passos:")
    print("1. git add .")
    print("2. git commit -m 'fix: Corrige deployment Railway - remove vestígios Replit'")
    print("3. git push")
    print("4. Railway vai fazer redeploy automaticamente")
    print("\n✅ O erro 'repl-nix-workspace' deve ser resolvido!")

if __name__ == "__main__":
    fix_railway_deployment()
