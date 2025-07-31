# 🧹 POLÍTICA DE LIMPEZA DO PROJETO SAMAPE

## 📋 OBJETIVO
Manter o repositório limpo, organizado e sem arquivos desnecessários que possam afetar o desempenho ou clareza do projeto.

## 🚀 EXECUÇÃO AUTOMÁTICA

### Antes de Cada Commit
```bash
python pre_commit_clean.py
```

### Limpeza Completa (Mensal)
```bash
python clean_project.py
```

## 📁 ARQUIVOS SEMPRE REMOVIDOS

### 🧪 Testes e Debug
- `test_*.py` (exceto testes principais)
- `debug_*.py`
- `check_*.py`
- `diagnose_*.py`
- `fix_*.py`
- `verify_*.py`
- `setup_*.py`

### 📦 Scripts de Migração (Já Executados)
- `migrate_*.py`
- `create_*.py`
- `insert_*.py`
- `update_db.py`

### 📄 Duplicatas e Backups
- `*.bak`
- `main.py` (duplicata do app.py)
- `database.py` (funcionalidade em models.py)
- `start_server.py`

### 🗂️ Temporários e Cache
- `__pycache__/` (exceto .venv)
- `*.pyc`
- `*.pyo`
- `*.log`
- `cookies.txt`
- `.DS_Store`
- `Thumbs.db`
- `.replit`

### 🖼️ Assets Desnecessários
- `image_*.png` (screenshots temporários)
- `Screenshot_*.png`
- `Captura*.png`
- `Pasted-*.txt`
- Arquivos de debug/teste em `attached_assets/`

### 📋 Documentação Temporária
- `*_TROUBLESHOOTING.md`
- `*_SETUP.md`
- `*_IMPROVEMENTS.md` (após implementação)

## ✅ ARQUIVOS PRESERVADOS

### 🔧 Core da Aplicação
- `app.py`
- `models.py`
- `routes.py`
- `forms.py`
- `config.py`
- `utils.py`
- `jinja_filters.py`

### 📦 Configuração
- `pyproject.toml`
- `uv.lock`
- `.gitignore`

### 🖼️ Assets Essenciais
- `FAVICON_SAMAPE.ico`
- `FAVICON_SAMAPE.png`
- `logo com sombra maior.png`

### 📁 Diretórios Principais
- `templates/`
- `static/`
- `db_migration/` (schemas)

### 🧪 Testes Importantes
- `test_base64_images.py` (teste do sistema principal)

### 📋 Documentação Principal
- `README.md`
- `PROBLEMA_RESOLVIDO_BASE64.md`
- `SIDEBAR_USERNAME_ROLE_UPDATE.md`

## 🔄 PROCESSO DE COMMIT

### 1. Limpeza Pré-Commit
```bash
python pre_commit_clean.py
git add .
git status  # Verificar arquivos
```

### 2. Commit
```bash
git commit -m "feat: descrição da funcionalidade

- Detalhe 1
- Detalhe 2
- Limpeza automática aplicada"
```

### 3. Push
```bash
git push
```

## 📊 .GITIGNORE ATUALIZADO

O arquivo `.gitignore` foi atualizado com padrões específicos do SAMAPE:

```gitignore
# === SAMAPE SPECIFIC ===
# Arquivos temporários de desenvolvimento
test_*.py
debug_*.py
check_*.py
diagnose_*.py
fix_*.py
verify_*.py
setup_*.py

# Scripts de migração (uma vez executados)
migrate_*.py
create_*.py
insert_*.py
update_db.py

# Backups e duplicatas
*.bak
main.py
start_server.py

# Assets temporários
attached_assets/image_*.png
attached_assets/Screenshot_*.png
attached_assets/Captura*.png
attached_assets/Pasted-*.txt

# Documentação temporária
*_TROUBLESHOOTING.md
*_SETUP.md
*_IMPROVEMENTS.md
```

## 🎯 BENEFÍCIOS

1. **⚡ Performance**: Repositório mais leve
2. **🧹 Organização**: Código limpo e claro
3. **🔍 Clareza**: Foco nos arquivos essenciais
4. **📦 Deploy**: Builds mais rápidos
5. **👥 Colaboração**: Estrutura mais compreensível

## ⚠️ IMPORTANTE

- **SEMPRE** execute `pre_commit_clean.py` antes de commits
- **NUNCA** remova arquivos essenciais listados acima
- **REVISAR** arquivos antes de confirmar remoção
- **BACKUP** de arquivos importantes antes de limpeza completa

---

**Política implementada em:** 30/07/2025  
**Última atualização:** 30/07/2025
