#!/usr/bin/env python3
"""
POLÍTICA DE LIMPEZA AUTOMÁTICA - SAMAPE
Executa limpeza rápida antes de cada commit
"""
import os
import shutil
from pathlib import Path

def quick_clean():
    """Limpeza rápida para execução antes de commits"""
    print("🧹 Limpeza Rápida - Pré-Commit")
    print("=" * 35)
    
    base_dir = Path(".")
    removed_count = 0
    
    # 1. Cache Python
    pycache_dirs = list(base_dir.glob("**/__pycache__"))
    if pycache_dirs:
        print("💾 Removendo cache Python...")
        for cache_dir in pycache_dirs:
            if not str(cache_dir).startswith(".venv"):  # Preservar venv
                try:
                    shutil.rmtree(cache_dir)
                    removed_count += 1
                    print(f"   ✅ {cache_dir}")
                except:
                    pass
    
    # 2. Arquivos temporários
    temp_patterns = ["*.pyc", "*.pyo", "*.log", "cookies.txt", ".DS_Store", "Thumbs.db"]
    print("🗂️  Removendo arquivos temporários...")
    for pattern in temp_patterns:
        found_files = list(base_dir.glob(pattern))
        for file in found_files:
            try:
                file.unlink()
                removed_count += 1
                print(f"   ✅ {file.name}")
            except:
                pass
    
    # 3. Verificar arquivos de teste órfãos
    test_files = list(base_dir.glob("test_*.py"))
    orphan_tests = [f for f in test_files if "temp" in f.name or "old" in f.name]
    if orphan_tests:
        print("🧪 Removendo testes órfãos...")
        for test in orphan_tests:
            try:
                test.unlink()
                removed_count += 1
                print(f"   ✅ {test.name}")
            except:
                pass
    
    if removed_count > 0:
        print(f"\n✅ {removed_count} itens removidos")
    else:
        print("\n✅ Projeto já está limpo")
    
    return removed_count

if __name__ == "__main__":
    quick_clean()
