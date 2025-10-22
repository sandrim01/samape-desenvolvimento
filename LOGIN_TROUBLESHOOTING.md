# 🔐 Guia de Solução de Problemas de Login - SAMAPE

## ✅ Status do Sistema

**Banco de Dados:** ✅ Funcionando  
**Usuário Admin:** ✅ Configurado corretamente  
**Servidor Flask:** ✅ Rodando na porta 5000  
**Template de Login:** ✅ Carregando corretamente  

## 🔑 Credenciais de Acesso

```
Usuário: admin
Senha: admin123
```

## 🌐 Como Acessar o Sistema

### 1. Verificar se o servidor está rodando
O servidor deve estar rodando em: `http://localhost:5000`

### 2. Acessar a página de login
- Abra o navegador
- Digite: `http://localhost:5000`
- Você será redirecionado para a página de login

### 3. Fazer o login
- **Usuário:** `admin`
- **Senha:** `admin123`
- Clique em "Entrar"

## 🔧 Possíveis Problemas e Soluções

### Problema 1: "Página não carrega"
**Solução:**
```bash
# Verificar se o servidor está rodando
python -c "from app import app; app.run(debug=True, host='0.0.0.0', port=5000)"
```

### Problema 2: "Nome de usuário ou senha inválidos"
**Soluções:**
1. Verifique se está digitando exatamente: `admin` (minúsculo)
2. Verifique se está digitando exatamente: `admin123`
3. Execute o script de reset do usuário:
```bash
python check_admin_user.py
```

### Problema 3: "Erro 500 ou erro interno"
**Solução:**
```bash
# Verificar logs no terminal onde o Flask está rodando
# Ou executar teste da aplicação:
python test_app.py
```

### Problema 4: "Página em branco ou não responde"
**Soluções:**
1. Limpar cache do navegador (Ctrl+F5)
2. Tentar em modo privado/incógnito
3. Verificar se não há firewall bloqueando

## 🛠️ Scripts de Diagnóstico

### Script 1: Verificar usuário admin
```bash
python check_admin_user.py
```

### Script 2: Testar login completo
```bash
python test_login.py
```

### Script 3: Verificar aplicação
```bash
python test_app.py
```

### Script 4: Verificar banco de dados
```bash
python verify_database.py
```

## 📞 Checklist de Verificação

- [ ] Servidor Flask está rodando?
- [ ] Página de login carrega em `http://localhost:5000`?
- [ ] Usuário `admin` existe no banco?
- [ ] Senha `admin123` está correta?
- [ ] Usuário está ativo?
- [ ] Sem erros no console do navegador?
- [ ] Sem erros no terminal do Flask?

## 🔄 Reset Completo (Se necessário)

Se nada funcionar, execute esta sequência:

```bash
# 1. Parar o servidor Flask (Ctrl+C)

# 2. Reset do usuário admin
python check_admin_user.py

# 3. Testar login
python test_login.py

# 4. Reiniciar servidor
python -c "from app import app; app.run(debug=True, host='0.0.0.0', port=5000)"

# 5. Tentar login novamente
```

## 🎯 Informações de Debug

- **URL do sistema:** http://localhost:5000
- **Usuário:** admin
- **Senha:** admin123
- **Debug ativo:** Sim
- **Banco:** PostgreSQL (Railway)

---

## 💡 Dica Importante

Se ainda assim não conseguir fazer login, me informe:
1. O que aparece na tela quando tenta fazer login?
2. Há alguma mensagem de erro?
3. O que mostra no terminal do Flask?
4. Testou com os scripts de diagnóstico?

**O sistema está funcionando corretamente!** 🎉
