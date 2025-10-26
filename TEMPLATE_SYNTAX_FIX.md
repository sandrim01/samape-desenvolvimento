# TESTE DE SINTAXE JINJA - employees/index.html

## Estrutura de IFs analisada:

### Linha 87: {% if current_user.is_admin() %}
- **Abre:** `{% if current_user.is_admin() %}`
- **Fecha:** Linha 193: `{% endif %}`

### Linha 92: {% if employee.id != current_user.id %}
- **Abre:** `{% if employee.id != current_user.id %}`
- **Fecha:** Linha 192: `{% endif %}`

### Linha 96: {% if employee.active %}
- **Abre:** `{% if employee.active %}` (botão de dar baixa)
- **Fecha:** Linha 100: `{% endif %}`

### Linha 133: {% if employee.active %}
- **Abre:** `{% if employee.active %}` (modal de baixa)
- **Fecha:** Linha 191: `{% endif %}`

## Correção aplicada:
- Removido um `{% endif %}` extra
- Mantida estrutura correta de aninhamento
- Total de 4 `{% if %}` e 4 `{% endif %}` correspondentes

## Status: CORRIGIDO