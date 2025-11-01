# 📋 Guia de Preenchimento - Formulário de Ordem de Serviço

## ✅ Campos Implementados e Funcionais

### 🚗 **Seção 1: Controle de Kilometragem**

#### Campos de Entrada (preencher manualmente):
1. **Kilometragem Inicial** (`km_inicial`)
   - Campo numérico com 2 casas decimais
   - Exemplo: `12345.50`
   - Uso: KM no início do serviço

2. **Kilometragem Final** (`km_final`)
   - Campo numérico com 2 casas decimais
   - Exemplo: `12450.75`
   - Uso: KM no final do serviço
   - ⚠️ Validação: Deve ser maior que KM inicial

3. **Valor por KM** (`km_rate`)
   - Campo numérico com 2 casas decimais
   - Exemplo: `2.50`
   - Uso: Taxa cobrada por quilômetro rodado

#### Campos Calculados Automaticamente:
- **Total Percorrido (KM)** (`km_total`)
  - 📊 Fórmula: `km_final - km_inicial`
  - Exemplo: `12450.75 - 12345.50 = 105.25 km`
  - ✏️ Campo somente leitura (readonly)

- **Valor Total KM** (`km_value`)
  - 📊 Fórmula: `km_total × km_rate`
  - Exemplo: `105.25 × 2.50 = R$ 263.13`
  - ✏️ Campo somente leitura (readonly)

---

### 💰 **Seção 2: Valores do Serviço**

#### Campos de Entrada (preencher manualmente):
1. **Valor da Mão de Obra** (`labor_value`)
   - Campo numérico com 2 casas decimais
   - Exemplo: `150.00`
   - Uso: Custo do trabalho realizado

2. **Valor das Peças** (`parts_value`)
   - Campo numérico com 2 casas decimais
   - Exemplo: `200.00`
   - Uso: Custo das peças utilizadas

#### Campo Calculado Automaticamente:
- **Valor Total do Serviço** (`total_value`)
  - 📊 Fórmula: `km_value + labor_value + parts_value`
  - Exemplo: `263.13 + 150.00 + 200.00 = R$ 613.13`
  - ✏️ Campo somente leitura (readonly)

---

## 🎯 Fluxo de Preenchimento Recomendado

### Passo 1: Informações Básicas
```
1. Selecione o Cliente
2. Selecione o Responsável (opcional)
3. Selecione os Equipamentos relacionados
4. Preencha a Descrição do Serviço
5. Defina o Status inicial
```

### Passo 2: Kilometragem (se aplicável)
```
1. Digite a Kilometragem Inicial
2. Digite a Kilometragem Final
   ➡️ Total Percorrido é calculado automaticamente
3. Digite o Valor por KM
   ➡️ Valor Total KM é calculado automaticamente
```

### Passo 3: Valores do Serviço
```
1. Digite o Valor da Mão de Obra
2. Digite o Valor das Peças
   ➡️ Valor Total do Serviço é calculado automaticamente
```

### Passo 4: Anexos (opcional)
```
1. Selecione imagens (máx. 500KB cada)
2. Adicione descrições (separadas por ponto e vírgula)
```

---

## 🧮 Exemplos de Cálculo

### Exemplo 1: Serviço com Deslocamento
```
📍 Kilometragem Inicial: 10.000,00 km
📍 Kilometragem Final:   10.050,00 km
📍 Total Percorrido:        50,00 km (calculado)

💵 Valor por KM:          R$ 3,00
💵 Valor Total KM:      R$ 150,00 (calculado)

🔧 Mão de Obra:         R$ 250,00
🔩 Peças:               R$ 180,00

💰 TOTAL:              R$ 580,00 (calculado)
```

### Exemplo 2: Serviço sem Deslocamento
```
📍 Campos de KM: deixar em branco

🔧 Mão de Obra:         R$ 120,00
🔩 Peças:               R$  85,00

💰 TOTAL:              R$ 205,00 (calculado)
```

### Exemplo 3: Apenas Deslocamento
```
📍 Kilometragem Inicial: 5.000,00 km
📍 Kilometragem Final:   5.100,00 km
📍 Total Percorrido:       100,00 km (calculado)

💵 Valor por KM:          R$ 2,50
💵 Valor Total KM:      R$ 250,00 (calculado)

🔧 Mão de Obra:         R$   0,00
🔩 Peças:               R$   0,00

💰 TOTAL:              R$ 250,00 (calculado)
```

---

## ⚡ Funcionalidades Automáticas

### ✨ Cálculos em Tempo Real
- Todos os valores são recalculados automaticamente ao digitar
- Não é necessário clicar em nenhum botão "Calcular"
- Os campos calculados são atualizados instantaneamente

### ✅ Validações
- **KM Final > KM Inicial**: Sistema valida automaticamente
- **Valores numéricos**: Aceita apenas números e decimais
- **Campos obrigatórios**: Cliente e Descrição são obrigatórios

### 💾 Salvamento no Banco de Dados
Todos os campos são salvos na tabela `service_order`:
```sql
- km_inicial (NUMERIC 10,2)
- km_final (NUMERIC 10,2)
- km_total (NUMERIC 10,2)
- km_rate (NUMERIC 10,2)
- km_value (NUMERIC 10,2)
- labor_value (NUMERIC 10,2)
- parts_value (NUMERIC 10,2)
- total_value (NUMERIC 10,2)
```

---

## 🎨 Interface Visual

### Seção de Kilometragem (Card Azul)
```
┌─────────────────────────────────────────────┐
│ 🚗 Controle de Kilometragem                 │
├─────────────────────────────────────────────┤
│ [ KM Inicial ]  [ KM Final ]  [ Total ✓ ]  │
│ [ R$/KM ]                     [ Total R$ ✓ ]│
└─────────────────────────────────────────────┘
```

### Seção de Valores (Card Verde)
```
┌─────────────────────────────────────────────┐
│ 💰 Valores do Serviço                       │
├─────────────────────────────────────────────┤
│ [ Mão de Obra ]  [ Peças ]                  │
│ [ VALOR TOTAL ✓ ]                           │
└─────────────────────────────────────────────┘
```

---

## 🐛 Resolução de Problemas

### Problema: Campo calculado não atualiza
**Solução**: 
- Verifique se preencheu todos os campos necessários
- Campos calculados dependem dos campos de entrada
- Aguarde 1 segundo após digitar

### Problema: Erro ao salvar
**Solução**:
- Verifique se Cliente e Descrição estão preenchidos
- Verifique se KM Final é maior que KM Inicial
- Verifique se os valores são números válidos

### Problema: Total não considera kilometragem
**Solução**:
- Preencha todos os 3 campos: KM Inicial, KM Final e Valor/KM
- O cálculo só é feito quando todos estão preenchidos

---

## 📊 Status da Implementação

| Item | Status |
|------|--------|
| ✅ Campos no formulário | Implementado |
| ✅ Colunas no banco de dados | Implementado |
| ✅ JavaScript de cálculo | Implementado |
| ✅ Validações | Implementado |
| ✅ Salvamento em rotas | Implementado |
| ✅ Modelo atualizado | Implementado |
| ✅ Métodos de cálculo | Implementado |

---

## 🚀 Testando a Funcionalidade

### Teste 1: Criar OS Simples
1. Acesse: `/os/nova`
2. Selecione um cliente
3. Preencha descrição
4. Digite valores de mão de obra e peças
5. Clique em "Salvar"
6. ✅ Verifique se o total foi calculado

### Teste 2: Criar OS com KM
1. Acesse: `/os/nova`
2. Selecione um cliente
3. Preencha todos os campos de KM
4. Verifique se Total Percorrido é calculado
5. Verifique se Valor Total KM é calculado
6. Clique em "Salvar"
7. ✅ Verifique se todos os valores foram salvos

### Teste 3: Validação de KM
1. Digite KM Final menor que KM Inicial
2. ⚠️ Deve mostrar erro de validação
3. Corrija os valores
4. ✅ Erro deve desaparecer

---

## 📚 Referências Técnicas

- **Formulário**: `templates/service_orders/create.html`
- **Modelo**: `models.py` → `ServiceOrder`
- **Rota**: `routes.py` → `new_service_order()`
- **JavaScript**: Dentro do template create.html
- **Validação**: `forms.py` → `ServiceOrderForm`

---

**Última atualização**: 16/01/2025  
**Versão**: 2.0 - Campos KM e Valores Completos
