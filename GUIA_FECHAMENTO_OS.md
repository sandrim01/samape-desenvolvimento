# 🚀 GUIA RÁPIDO: Sistema de Fechamento de OS

## Para Começar

### 1️⃣ Executar a Migração do Banco de Dados

Antes de usar o novo sistema, execute a migração:

```powershell
python migrate_fechamento_os.py
```

Digite **sim** quando solicitado.

---

## 📖 Como Usar

### ✅ Fechar uma Ordem de Serviço

1. Acesse **Ordens de Serviço** no menu
2. Clique na OS que deseja fechar
3. Clique no botão **"Fechar OS"**
4. Preencha:
   - **Valor Total**: O valor final cobrado
   - **Detalhes do Serviço**: Descrição do que foi realizado
5. Clique em **"Confirmar Fechamento"**

**O que acontece automaticamente:**
- ✅ OS marcada como "Fechada"
- ✅ Data/hora de fechamento registrada
- ✅ Lançamento financeiro criado automaticamente
- ✅ Valor alimenta o sistema financeiro

---

### 📊 Visualizar Fechamentos de OS

1. Acesse **"Fechamento de OS"** no menu lateral
2. Você verá todas as OS fechadas com:
   - Número da OS
   - Data e hora do fechamento
   - Cliente
   - Responsável
   - Valor

**Filtros disponíveis:**
- Por cliente
- Por número de OS
- Por período (data inicial e final)

---

### 💰 Verificar no Sistema Financeiro

1. Acesse **"Financeiro"** no menu
2. Os fechamentos de OS aparecem como:
   - **Tipo**: Entrada
   - **Categoria**: Fechamento de OS
   - **Status**: Pago
   - **Descrição**: "Fechamento de OS #[número] - [nome do cliente]"

---

## 🔍 Diferenças da Versão Anterior

| Antes (Notas Fiscais) | Agora (Fechamento de OS) |
|------------------------|--------------------------|
| Foco em NF-e | Foco no fechamento da OS |
| Sem categoria específica | Categoria "Fechamento de OS" |
| Lançamento manual possível | Lançamento 100% automático |
| Rota: `/notas-fiscais` | Rota: `/fechamento-os` |

---

## ⚠️ Importante

- **Toda OS fechada gera lançamento financeiro automaticamente**
- **Não é possível fechar OS sem informar o valor**
- **O lançamento é marcado como "Pago" automaticamente**
- **Não é necessário criar lançamento manualmente**

---

## 📱 Acesso Rápido

```
Menu Principal → Fechamento de OS
```

ou navegue para:

```
http://seu-servidor/fechamento-os
```

---

## 💡 Dicas

1. **Sempre preencha os detalhes do serviço** ao fechar a OS
2. **Verifique o valor** antes de confirmar
3. **Use os filtros** para encontrar fechamentos específicos
4. **Acompanhe pelo sistema financeiro** para análises

---

## 🆘 Solução de Problemas

### Problema: Não consigo fechar uma OS
**Solução**: Verifique se a OS não está já fechada

### Problema: Lançamento não aparece no financeiro
**Solução**: 
1. Verifique se executou a migração
2. Reinicie o servidor
3. Verifique os logs da aplicação

### Problema: Erro ao executar migração
**Solução**: Certifique-se de que o banco de dados está acessível

---

## 📞 Suporte

Consulte a documentação completa em:
- `FECHAMENTO_OS_IMPLEMENTACAO.md`

---

**Versão**: 1.0  
**Última atualização**: 31/10/2025
