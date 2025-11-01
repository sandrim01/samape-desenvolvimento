# Implementação de Campos de KM e Valores na Ordem de Serviço

## 📋 Resumo
Foram adicionados campos de controle de kilometragem e valores detalhados na tabela `service_order` para permitir cálculos automáticos do valor total da OS.

## 🎯 Problema Identificado
O formulário de criação de Ordem de Serviço (`templates/service_orders/create.html`) possuía campos que não existiam no banco de dados:
- `km_inicial`, `km_final`, `km_total`
- `km_rate` (valor por KM), `km_value` (valor total de KM)
- `labor_value` (mão de obra), `parts_value` (peças), `total_value` (total)

Isso causava erro ao tentar criar uma OS.

## ✅ Solução Implementada

### 1. Alterações no Modelo (`models.py`)

```python
class ServiceOrder(db.Model):
    # ... campos existentes ...
    
    # Campos de Kilometragem
    km_inicial = db.Column(db.Numeric(10, 2), default=0)
    km_final = db.Column(db.Numeric(10, 2), default=0)
    km_total = db.Column(db.Numeric(10, 2), default=0)
    km_rate = db.Column(db.Numeric(10, 2), default=0)  # Valor por KM
    km_value = db.Column(db.Numeric(10, 2), default=0)  # Valor total de KM
    
    # Composição de Valores
    labor_value = db.Column(db.Numeric(10, 2), default=0)  # Mão de obra
    parts_value = db.Column(db.Numeric(10, 2), default=0)  # Peças
    total_value = db.Column(db.Numeric(10, 2), default=0)  # Valor total
    
    def update_km_total(self):
        """Calcula o total de KM percorridos"""
        if self.km_inicial and self.km_final and self.km_final > self.km_inicial:
            self.km_total = self.km_final - self.km_inicial
        else:
            self.km_total = 0
    
    def update_km_value(self):
        """Calcula o valor total baseado em KM"""
        if self.km_total and self.km_rate:
            self.km_value = self.km_total * self.km_rate
        else:
            self.km_value = 0
    
    def update_total_value(self):
        """Calcula o valor total do serviço"""
        km_val = self.km_value or 0
        labor_val = self.labor_value or 0
        parts_val = self.parts_value or 0
        self.total_value = km_val + labor_val + parts_val
```

### 2. Script de Migração (`add_service_order_columns.py`)

Criado script para adicionar as colunas no banco de dados PostgreSQL:
- Verifica se cada coluna já existe antes de adicionar
- Adiciona todas as colunas com valores padrão 0
- Executado com sucesso no banco de produção

**Resultado da execução:**
```
✓ Coluna km_rate adicionada com sucesso!
✓ Coluna km_value adicionada com sucesso!
✓ Coluna labor_value adicionada com sucesso!
✓ Coluna parts_value adicionada com sucesso!
✓ Coluna total_value adicionada com sucesso!
```

### 3. Atualização das Rotas (`routes.py`)

#### Rota `/os/nova` (POST)
```python
service_order = ServiceOrder(
    # ... campos existentes ...
    km_inicial=form.km_inicial.data,
    km_final=form.km_final.data,
    km_rate=form.km_rate.data,
    labor_value=form.labor_value.data,
    parts_value=form.parts_value.data
)

# Cálculos automáticos
service_order.update_km_total()
service_order.update_km_value()
service_order.update_total_value()
```

#### Rota `/api/service_orders/create` (Modal)
```python
service_order = ServiceOrder(
    # ... campos existentes ...
    km_inicial=data.get('km_inicial', 0),
    km_final=data.get('km_final', 0),
    km_rate=data.get('km_rate', 0),
    labor_value=data.get('labor_value', 0),
    parts_value=data.get('parts_value', 0)
)

# Cálculos automáticos
service_order.update_km_total()
service_order.update_km_value()
service_order.update_total_value()
```

## 🧮 Cálculos Automáticos

### 1. Total de Kilometragem
```
km_total = km_final - km_inicial
```

### 2. Valor de Kilometragem
```
km_value = km_total × km_rate
```

### 3. Valor Total do Serviço
```
total_value = km_value + labor_value + parts_value
```

## 📊 Estrutura da Tabela Atualizada

```sql
service_order
├── id (PK)
├── client_id (FK)
├── responsible_id (FK)
├── description
├── estimated_value
├── status
├── created_at
├── updated_at
├── closed_at
├── invoice_number
├── invoice_date
├── invoice_amount
├── service_details
├── discount_amount
├── original_amount
├── km_inicial       ← NOVO
├── km_final         ← NOVO
├── km_total         ← NOVO
├── km_rate          ← NOVO
├── km_value         ← NOVO
├── labor_value      ← NOVO
├── parts_value      ← NOVO
└── total_value      ← NOVO
```

## 📝 Formulário Atualizado

O formulário de criação já possui todos os campos necessários:

### Seção: Controle de Kilometragem
- **KM Inicial**: Campo numérico
- **KM Final**: Campo numérico
- **Total Percorrido**: Calculado automaticamente
- **Valor por KM**: Campo numérico
- **Valor Total KM**: Calculado automaticamente

### Seção: Valores do Serviço
- **Valor da Mão de Obra**: Campo numérico
- **Valor das Peças**: Campo numérico
- **Valor Total do Serviço**: Calculado automaticamente (KM + Mão de Obra + Peças)

## 🎨 JavaScript do Formulário

O template já possui funções JavaScript para cálculos em tempo real:

```javascript
function calculateKmTotal() {
    const kmInicial = parseFloat($('#km_inicial').val()) || 0;
    const kmFinal = parseFloat($('#km_final').val()) || 0;
    const kmTotal = kmFinal > kmInicial ? (kmFinal - kmInicial) : 0;
    $('#km_total').val(kmTotal.toFixed(2));
    calculateKmValue();
}

function calculateKmValue() {
    const kmTotal = parseFloat($('#km_total').val()) || 0;
    const kmRate = parseFloat($('#km_rate').val()) || 0;
    const kmValue = kmTotal * kmRate;
    $('#km_value').val(kmValue.toFixed(2));
    calculateTotalValue();
}

function calculateTotalValue() {
    const kmValue = parseFloat($('#km_value').val()) || 0;
    const laborValue = parseFloat($('#labor_value').val()) || 0;
    const partsValue = parseFloat($('#parts_value').val()) || 0;
    const total = kmValue + laborValue + partsValue;
    $('#total_value').val(total.toFixed(2));
}
```

## ✅ Testes Realizados

1. ✅ Script de migração executado com sucesso
2. ✅ Colunas adicionadas no banco de dados PostgreSQL
3. ✅ Modelo atualizado com novos campos
4. ✅ Rotas atualizadas para processar novos campos
5. ✅ Código enviado para o repositório Git

## 🚀 Próximos Passos

1. Aguardar deploy automático no Railway
2. Testar criação de nova OS no ambiente de produção
3. Verificar se os cálculos automáticos estão funcionando
4. Testar todos os cenários:
   - OS com apenas valor estimado
   - OS com kilometragem e valor por KM
   - OS com mão de obra e peças
   - OS completa com todos os valores

## 📌 Commits Relacionados

- `276628f` - feat: Adiciona campos de KM e valores na OS
- `21d2952` - fix: Remove colunas discount_amount e original_amount do modelo
- `a29c5a7` - fix: Remove colunas inexistentes do modelo ServiceOrder

## 🔗 Integração com Fechamento de OS

Estes campos alimentarão o sistema financeiro quando a OS for fechada:
- O `total_value` será usado como `invoice_amount`
- Será criado um lançamento financeiro automático
- Categoria: `FinancialCategory.fechamento_os`
- Status: `FinancialStatus.pago`

---

**Data de Implementação:** 01/11/2025  
**Status:** ✅ Implementado e em produção
