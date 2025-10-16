# Guia de Componentes Mobile Padronizados - SAMAPE

Este guia apresenta o sistema de componentes mobile padronizados implementado para garantir uma experiência consistente e otimizada em dispositivos móveis.

## 📱 Sistema de Classes CSS

### Card Padrão Mobile
```html
<div class="mobile-standard-card">
    <!-- Conteúdo do card -->
</div>
```

### Header de Página Mobile
```html
<div class="mobile-page-header">
    <h1 class="mobile-page-title">Título da Página</h1>
    <div class="mobile-page-actions">
        <a href="#" class="mobile-action-btn-expanded">
            <i class="fas fa-plus"></i> Nova Ação
        </a>
    </div>
</div>
```

### Filtros Mobile
```html
<div class="mobile-filters-card">
    <div class="mobile-filter-row">
        <div class="mobile-filter-col">
            <input type="text" class="form-control" placeholder="Buscar...">
        </div>
        <div class="mobile-filter-col" style="flex: 0 0 auto;">
            <button class="btn btn-primary">
                <i class="fas fa-search"></i>
            </button>
        </div>
    </div>
</div>
```

## 🏗️ Estrutura de Card Completo

```html
<div class="mobile-standard-card">
    <!-- Header com título e status -->
    <div class="mobile-card-header">
        <div>
            <h5 class="mobile-card-title">Título Principal</h5>
            <p class="mobile-card-subtitle">Subtítulo ou informação secundária</p>
        </div>
        <span class="mobile-status-badge status-active">Ativo</span>
    </div>
    
    <!-- Corpo com informações -->
    <div class="mobile-card-body">
        <div class="mobile-card-row">
            <i class="mobile-card-icon fas fa-envelope"></i>
            <span class="mobile-card-label">Email</span>
            <span class="mobile-card-value">usuario@exemplo.com</span>
        </div>
        <div class="mobile-card-row">
            <i class="mobile-card-icon fas fa-phone"></i>
            <span class="mobile-card-label">Telefone</span>
            <span class="mobile-card-value">(11) 99999-9999</span>
        </div>
    </div>
    
    <!-- Ações -->
    <div class="mobile-card-actions">
        <a href="#" class="mobile-action-btn btn-view" title="Visualizar">
            <i class="fas fa-eye"></i>
        </a>
        <a href="#" class="mobile-action-btn btn-edit" title="Editar">
            <i class="fas fa-edit"></i>
        </a>
        <button class="mobile-action-btn btn-delete" title="Excluir">
            <i class="fas fa-trash"></i>
        </button>
    </div>
</div>
```

## 🎨 Status Badges Disponíveis

```css
.mobile-status-badge.status-active      /* Amarelo - Ativo/Pendente */
.mobile-status-badge.status-aberta      /* Amarelo - Aberta */
.mobile-status-badge.status-pending     /* Amarelo - Pendente */

.mobile-status-badge.status-completed   /* Verde - Concluído */
.mobile-status-badge.status-fechada     /* Verde - Fechada */
.mobile-status-badge.status-success     /* Verde - Sucesso */

.mobile-status-badge.status-cancelled   /* Vermelho - Cancelado */
.mobile-status-badge.status-cancelada   /* Vermelho - Cancelada */
.mobile-status-badge.status-danger      /* Vermelho - Perigo */

.mobile-status-badge.status-em-andamento /* Azul - Em andamento */
.mobile-status-badge.status-processing   /* Azul - Processando */
```

## 🔘 Botões de Ação Disponíveis

```css
.mobile-action-btn.btn-view      /* Azul - Visualizar */
.mobile-action-btn.btn-edit      /* Amarelo - Editar */
.mobile-action-btn.btn-delete    /* Vermelho - Excluir */
.mobile-action-btn.btn-invoice   /* Roxo - Fatura */
.mobile-action-btn.btn-download  /* Verde - Download */
```

## 📋 Tabs Mobile Padronizadas

```html
<div class="mobile-standard-tabs">
    <a href="#" class="mobile-standard-tab active">Aba 1</a>
    <a href="#" class="mobile-standard-tab">Aba 2</a>
    <a href="#" class="mobile-standard-tab">Aba 3</a>
</div>
```

## 🔧 JavaScript Builder

Para criar cards dinamicamente via JavaScript:

```javascript
// Exemplo de uso do MobileCardBuilder
const cardData = {
    title: 'João Silva',
    subtitle: '123.456.789-00',
    status: 'active',
    fields: [
        {
            icon: 'fas fa-envelope',
            label: 'Email',
            value: 'joao@email.com'
        },
        {
            icon: 'fas fa-phone',
            label: 'Telefone',
            value: '(11) 99999-9999'
        }
    ],
    actions: [
        {
            type: 'view',
            href: '/clients/1',
            icon: 'fas fa-eye',
            title: 'Visualizar'
        },
        {
            type: 'edit',
            href: '/clients/1/edit',
            icon: 'fas fa-edit',
            title: 'Editar'
        },
        {
            type: 'expanded',
            href: '/clients/new',
            icon: 'fas fa-plus',
            text: 'Novo Cliente'
        }
    ]
};

const builder = new MobileCardBuilder(cardData);
const cardHTML = builder.build();
document.getElementById('cards-container').innerHTML = cardHTML;
```

## 🎯 Padronização Automática

O sistema aplica automaticamente padronização a elementos existentes:

- **Cards existentes**: Convertidos para `.mobile-standard-card`
- **Tabs**: Convertidas para `.mobile-standard-tabs`
- **Headers**: Convertidos para `.mobile-page-header`
- **Botões**: Otimizados para touch com tamanho mínimo 44px

## 📱 Características Mobile

### Touch Optimization
- Tamanho mínimo de 44px para todos os alvos de toque
- Feedback visual em interações
- Feedback háptico sutil (quando disponível)
- Animações suaves e responsivas

### Design System
- Cores unificadas com a versão desktop
- Espaçamento consistente usando variáveis CSS
- Bordas e sombras padronizadas
- Tipografia otimizada para leitura mobile

### Responsividade
- Breakpoint principal em 768px
- Layout flexível com CSS Grid/Flexbox
- Imagens e conteúdo adaptáveis
- Navegação otimizada para mobile

## 🚀 Como Implementar em Novas Páginas

1. **Header da Página**:
   ```html
   <div class="mobile-page-header">
       <h1 class="mobile-page-title">Título</h1>
       <div class="mobile-page-actions">
           <!-- botões de ação -->
       </div>
   </div>
   ```

2. **Filtros (se necessário)**:
   ```html
   <div class="mobile-filters-card">
       <!-- formulário de filtros -->
   </div>
   ```

3. **Lista de Cards**:
   ```html
   <div class="mobile-cards-container d-md-none">
       <!-- cards mobile -->
   </div>
   ```

4. **Tabela Desktop** (manter existente):
   ```html
   <div class="table-responsive d-none d-md-block">
       <!-- tabela para desktop -->
   </div>
   ```

## 📋 Checklist de Implementação

- [ ] Header da página padronizado
- [ ] Filtros em card dedicado
- [ ] Cards mobile com estrutura padronizada
- [ ] Botões de ação otimizados para touch
- [ ] Status badges quando aplicável
- [ ] Ícones em informações dos cards
- [ ] Animações e feedback visual
- [ ] Testes em diferentes dispositivos

## 🎨 Exemplo de Página Padronizada

Veja o arquivo `templates/clients/index.html` como exemplo de implementação completa da padronização mobile.

---

**Desenvolvido por**: Sistema de Design SAMAPE  
**Versão**: 1.0  
**Data**: 2024