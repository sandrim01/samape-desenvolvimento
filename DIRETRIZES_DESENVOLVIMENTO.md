# 📋 Diretrizes de Desenvolvimento - SAMAPE

## 🧪 Gerenciamento de Arquivos de Teste

### ❌ O que NÃO fazer:
- Criar arquivos de teste diretamente no diretório raiz
- Manter arquivos de debug/verificação após resolver o problema
- Deixar scripts de correção/fix no repositório após uso
- Criar backups manuais (`.bak`, `_backup.py`, etc.)

### ✅ O que fazer:

#### 1. **Arquivos de Teste**
- Criar testes em diretório separado: `/tests/`
- Usar nomes descritivos: `test_funcionalidade_especifica.py`
- **EXCLUIR IMEDIATAMENTE** após perder a utilidade
- Para testes permanentes, usar framework como pytest

#### 2. **Scripts de Debug**
- Criar em diretório temporário: `/debug/` (adicionar ao .gitignore)
- Nomear com prefixo: `debug_problema_especifico.py`
- **EXCLUIR** assim que o problema for resolvido
- Documentar a solução no código principal, não manter o script

#### 3. **Scripts de Migração**
- Criar em diretório específico: `/migrations/`
- Nomear com timestamp: `YYYYMMDD_descricao_migracao.py`
- **EXCLUIR** após executar com sucesso em produção
- Manter apenas scripts de migração de schema permanentes

#### 4. **Scripts de Correção/Fix**
- Usar apenas temporariamente para resolver problemas específicos
- **EXCLUIR IMEDIATAMENTE** após aplicar a correção
- Incorporar a correção no código principal

### 🗂️ Estrutura Recomendada:
```
samape-desenvolvimento/
├── app.py              # Arquivo principal
├── routes.py           # Rotas da aplicação
├── models.py           # Modelos do banco
├── forms.py            # Formulários
├── config.py           # Configurações
├── utils.py            # Utilitários
├── database.py         # Configuração do banco
├── tests/              # Testes permanentes (se necessário)
├── migrations/         # Migrações de schema permanentes
├── static/             # Arquivos estáticos
├── templates/          # Templates HTML
└── requirements.txt    # Dependências
```

### 🚮 Arquivos Excluídos na Limpeza (2025-01-31):
- `test_*.py` (22 arquivos)
- `debug_*.py` (1 arquivo)
- `check_*.py` (2 arquivos)
- `verify_*.py` (2 arquivos)
- `diagnos*.py` (2 arquivos)
- `fix_*.py` (4 arquivos)
- Scripts de migração pontuais (8 arquivos)
- Arquivos de backup (2 arquivos)
- Scripts temporários (3 arquivos)

**Total: 46 arquivos removidos**

### 📝 Regra de Ouro:
> **"Se um arquivo de teste/debug/fix não tem mais utilidade, EXCLUA IMEDIATAMENTE"**

### 🔄 Processo para Novos Arquivos de Teste:
1. Criar o arquivo de teste
2. Resolver o problema/implementar a funcionalidade
3. **EXCLUIR** o arquivo de teste
4. Documentar a solução no código principal
5. Fazer commit apenas do código final limpo

### 📚 Exceções (arquivos que podem permanecer):
- `create_test_data.py` - Para popular dados iniciais de desenvolvimento
- `insert_initial_data.py` - Para dados iniciais do sistema
- `migrate_db.py` - Para migrações de schema permanentes
- `create_tables.py` - Para criação inicial de tabelas

---
**Última atualização:** 31/01/2025
