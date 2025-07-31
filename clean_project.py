#!/usr/bin/env python3
"""
Script para limpar arquivos desnecessários do projeto SAMAPE
Executa análise e remoção de arquivos temporários, testes antigos e duplicatas
"""
import os
import glob
import shutil
from pathlib import Path

def clean_project():
    print("🧹 LIMPEZA DO PROJETO SAMAPE")
    print("=" * 40)
    
    base_dir = Path(".")
    files_to_remove = []
    dirs_to_remove = []
    
    # 1. Arquivos de teste antigos/desnecessários
    test_files = [
        "test_*.py",
        "check_*.py", 
        "debug_*.py",
        "diagnose_*.py",
        "fix_*.py",
        "verify_*.py",
        "setup_*.py"
    ]
    
    print("\n📝 ARQUIVOS DE TESTE E DEBUG:")
    for pattern in test_files:
        found_files = list(base_dir.glob(pattern))
        for file in found_files:
            if file.name not in ['test_base64_images.py']:  # Manter alguns testes importantes
                files_to_remove.append(file)
                print(f"   🗑️  {file.name}")
    
    # 2. Scripts de migração/setup antigos (já executados)
    migration_scripts = [
        "create_db_tables.py",
        "create_tables.py", 
        "migrate_db.py",
        "migrate_to_railway.py",
        "migrate_images_to_base64.py",
        "insert_initial_data.py",
        "insert_equipment_models.py",
        "create_test_data.py",
        "update_db.py"
    ]
    
    print("\n📦 SCRIPTS DE MIGRAÇÃO (já executados):")
    for script in migration_scripts:
        script_path = base_dir / script
        if script_path.exists():
            files_to_remove.append(script_path)
            print(f"   🗑️  {script}")
    
    # 3. Arquivos duplicados/backup
    backup_files = [
        "routes.py.bak",
        "main.py",  # Duplicata do app.py
        "database.py",  # Funcionalidade já em models.py
        "start_server.py"  # Desnecessário
    ]
    
    print("\n📄 ARQUIVOS DUPLICADOS/BACKUP:")
    for backup in backup_files:
        backup_path = base_dir / backup
        if backup_path.exists():
            files_to_remove.append(backup_path)
            print(f"   🗑️  {backup}")
    
    # 4. Arquivos temporários e cache (mesmo com .gitignore)
    temp_patterns = [
        "*.pyc",
        "*.pyo", 
        "*.log",
        "cookies.txt",
        ".replit"
    ]
    
    print("\n🗂️  ARQUIVOS TEMPORÁRIOS:")
    for pattern in temp_patterns:
        found_files = list(base_dir.glob(pattern))
        for file in found_files:
            files_to_remove.append(file)
            print(f"   🗑️  {file.name}")
    
    # 5. Diretório __pycache__ 
    pycache_dirs = list(base_dir.glob("**/__pycache__"))
    if pycache_dirs:
        print("\n💾 CACHE PYTHON:")
        for cache_dir in pycache_dirs:
            dirs_to_remove.append(cache_dir)
            print(f"   🗑️  {cache_dir}")
    
    # 6. Arquivos de documentação temporários (manter apenas os principais)
    temp_docs = [
        "LOGIN_TROUBLESHOOTING.md",
        "DATABASE_SETUP.md",
        "SIDEBAR_PROFILE_IMPROVEMENTS.md"
    ]
    
    print("\n📋 DOCUMENTAÇÃO TEMPORÁRIA:")
    for doc in temp_docs:
        doc_path = base_dir / doc
        if doc_path.exists():
            files_to_remove.append(doc_path)
            print(f"   🗑️  {doc}")
    
    # 7. Imagens desnecessárias em attached_assets
    assets_dir = base_dir / "attached_assets"
    if assets_dir.exists():
        print("\n🖼️  ASSETS DESNECESSÁRIOS:")
        # Manter apenas logos e favicons essenciais
        keep_assets = [
            "FAVICON_SAMAPE.ico",
            "FAVICON_SAMAPE.png", 
            "logo com sombra maior.png"
        ]
        
        for asset in assets_dir.iterdir():
            if asset.is_file() and asset.name not in keep_assets:
                files_to_remove.append(asset)
                print(f"   🗑️  {asset.name}")
    
    # Contar arquivos
    total_files = len(files_to_remove)
    total_dirs = len(dirs_to_remove)
    
    print(f"\n📊 RESUMO:")
    print(f"   • Arquivos para remover: {total_files}")
    print(f"   • Diretórios para remover: {total_dirs}")
    
    if total_files == 0 and total_dirs == 0:
        print("\n✅ Projeto já está limpo!")
        return
    
    # Confirmar remoção
    print(f"\n⚠️  Deseja remover {total_files + total_dirs} itens? (s/N): ", end="")
    confirm = input().lower().strip()
    
    if confirm in ['s', 'sim', 'y', 'yes']:
        removed_count = 0
        
        # Remover arquivos
        for file_path in files_to_remove:
            try:
                file_path.unlink()
                removed_count += 1
                print(f"✅ Removido: {file_path.name}")
            except Exception as e:
                print(f"❌ Erro ao remover {file_path.name}: {e}")
        
        # Remover diretórios
        for dir_path in dirs_to_remove:
            try:
                shutil.rmtree(dir_path)
                removed_count += 1
                print(f"✅ Removido: {dir_path}")
            except Exception as e:
                print(f"❌ Erro ao remover {dir_path}: {e}")
        
        print(f"\n🎉 Limpeza concluída! {removed_count} itens removidos.")
        
        # Atualizar .gitignore se necessário
        update_gitignore()
        
    else:
        print("\n❌ Limpeza cancelada.")

def update_gitignore():
    """Atualiza .gitignore com padrões adicionais"""
    gitignore_path = Path(".gitignore")
    
    additional_patterns = [
        "\n# === SAMAPE SPECIFIC ===",
        "# Arquivos temporários de desenvolvimento",
        "test_*.py",
        "debug_*.py", 
        "check_*.py",
        "diagnose_*.py",
        "fix_*.py",
        "verify_*.py",
        "setup_*.py",
        "",
        "# Scripts de migração (uma vez executados)",
        "migrate_*.py",
        "create_*.py", 
        "insert_*.py",
        "update_db.py",
        "",
        "# Backups e duplicatas",
        "*.bak",
        "main.py",
        "start_server.py",
        "",
        "# Assets temporários",
        "attached_assets/image_*.png",
        "attached_assets/Screenshot_*.png",
        "attached_assets/Captura*.png",
        "attached_assets/Pasted-*.txt",
        "",
        "# Documentação temporária",
        "*_TROUBLESHOOTING.md",
        "*_SETUP.md",
        "*_IMPROVEMENTS.md"
    ]
    
    try:
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            current_content = f.read()
        
        if "SAMAPE SPECIFIC" not in current_content:
            with open(gitignore_path, 'a', encoding='utf-8') as f:
                f.write('\n'.join(additional_patterns))
            print("✅ .gitignore atualizado com padrões do SAMAPE")
        
    except Exception as e:
        print(f"⚠️  Erro ao atualizar .gitignore: {e}")

if __name__ == "__main__":
    clean_project()
