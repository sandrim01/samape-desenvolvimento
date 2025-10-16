/**
 * SAMAPE - JavaScript para Otimizações Mobile
 * Melhora a experiência do usuário em dispositivos móveis
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // ===== DETECÇÃO DE DISPOSITIVO MÓVEL =====
    const isMobile = window.innerWidth <= 768;
    const isTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    
    // ===== CONFIGURAÇÕES DE VIEWPORT =====
    function setViewportHeight() {
        // Fix para altura do viewport em mobile (considera keyboard)
        const vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);
    }
    
    // Executa no load e no resize
    setViewportHeight();
    window.addEventListener('resize', setViewportHeight);
    
    // ===== MELHORIAS DE TOUCH =====
    if (isTouch) {
        // Remove delay de 300ms no touch
        document.addEventListener('touchstart', function() {}, { passive: true });
        
        // Adiciona classe para dispositivos touch
        document.body.classList.add('touch-device');
        
        // Melhora feedback visual em botões
        const touchElements = document.querySelectorAll('.btn, .nav-item, .card, .list-group-item');
        
        touchElements.forEach(element => {
            element.addEventListener('touchstart', function() {
                this.classList.add('touching');
            }, { passive: true });
            
            element.addEventListener('touchend', function() {
                setTimeout(() => {
                    this.classList.remove('touching');
                }, 100);
            }, { passive: true });
            
            element.addEventListener('touchcancel', function() {
                this.classList.remove('touching');
            }, { passive: true });
        });
    }
    
    // ===== NAVEGAÇÃO MOBILE =====
    const bottomNav = document.querySelector('.mobile-bottom-nav');
    if (bottomNav && isMobile) {
        
        // Esconde navegação ao scroll para baixo
        let lastScrollTop = 0;
        let scrollTimer = null;
        
        window.addEventListener('scroll', function() {
            clearTimeout(scrollTimer);
            
            scrollTimer = setTimeout(() => {
                const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
                
                if (scrollTop > lastScrollTop && scrollTop > 100) {
                    // Scrolling down
                    bottomNav.style.transform = 'translateY(100%)';
                } else {
                    // Scrolling up
                    bottomNav.style.transform = 'translateY(0)';
                }
                lastScrollTop = scrollTop;
            }, 10);
        }, { passive: true });
        
        // Garante que a navegação apareça quando parar de scrollar
        let scrollTimeout;
        window.addEventListener('scroll', function() {
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(() => {
                bottomNav.style.transform = 'translateY(0)';
            }, 1000);
        }, { passive: true });
    }
    
    // ===== OTIMIZAÇÕES DE FORMULÁRIO =====
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, select, textarea');
        
        inputs.forEach(input => {
            // Melhora UX dos inputs em mobile
            if (isMobile) {
                // Adiciona autocomplete apropriado
                if (input.type === 'email' && !input.autocomplete) {
                    input.autocomplete = 'email';
                }
                if (input.type === 'tel' && !input.autocomplete) {
                    input.autocomplete = 'tel';
                }
                if (input.name && input.name.includes('name') && !input.autocomplete) {
                    input.autocomplete = 'name';
                }
                
                // Otimiza teclado virtual
                if (input.type === 'number' || input.inputmode) {
                    // Já configurado corretamente
                } else if (input.type === 'email') {
                    input.inputmode = 'email';
                } else if (input.type === 'tel') {
                    input.inputmode = 'tel';
                } else if (input.type === 'url') {
                    input.inputmode = 'url';
                }
            }
            
            // Feedback visual melhorado
            input.addEventListener('focus', function() {
                this.closest('.form-group, .mb-3')?.classList.add('focused');
            });
            
            input.addEventListener('blur', function() {
                this.closest('.form-group, .mb-3')?.classList.remove('focused');
            });
        });
    });
    
    // ===== OTIMIZAÇÕES DE TABELA =====
    const tables = document.querySelectorAll('.table:not(.table-mobile-cards)');
    
    if (isMobile) {
        tables.forEach(table => {
            // Adiciona scroll horizontal suave
            const tableContainer = table.closest('.table-responsive');
            if (tableContainer) {
                tableContainer.style.scrollBehavior = 'smooth';
                
                // Adiciona indicador de scroll
                const scrollIndicator = document.createElement('div');
                scrollIndicator.className = 'scroll-indicator';
                scrollIndicator.innerHTML = '<i class="fas fa-chevron-right"></i>';
                tableContainer.appendChild(scrollIndicator);
                
                tableContainer.addEventListener('scroll', function() {
                    if (this.scrollLeft >= (this.scrollWidth - this.clientWidth - 10)) {
                        scrollIndicator.style.opacity = '0';
                    } else {
                        scrollIndicator.style.opacity = '1';
                    }
                });
            }
        });
    }
    
    // ===== MELHORIAS DE MODAL =====
    const modals = document.querySelectorAll('.modal');
    const mobileMenuModal = document.getElementById('mobileMenuModal');
    
    modals.forEach(modal => {
        modal.addEventListener('shown.bs.modal', function() {
            // Foca no primeiro input do modal
            const firstInput = this.querySelector('input, select, textarea');
            if (firstInput && !isMobile) { // Evita abrir teclado virtual
                firstInput.focus();
            }
            
            // Previne scroll do body
            document.body.style.overflow = 'hidden';
        });
        
        modal.addEventListener('hidden.bs.modal', function() {
            // Restaura scroll do body
            document.body.style.overflow = '';
        });
    });
    
    // ===== MODAL DO MENU MOBILE =====
    if (mobileMenuModal && isMobile) {
        // Adiciona animação aos itens do grid
        const gridItems = mobileMenuModal.querySelectorAll('.menu-grid-item');
        
        mobileMenuModal.addEventListener('shown.bs.modal', function() {
            // Anima entrada dos itens com delay escalonado
            gridItems.forEach((item, index) => {
                item.style.opacity = '0';
                item.style.transform = 'translateY(20px)';
                
                setTimeout(() => {
                    item.style.transition = 'all 0.3s ease';
                    item.style.opacity = '1';
                    item.style.transform = 'translateY(0)';
                }, index * 50);
            });
        });
        
        // Fecha modal ao clicar em um item
        gridItems.forEach(item => {
            item.addEventListener('click', function() {
                // Pequeno delay para feedback visual
                setTimeout(() => {
                    bootstrap.Modal.getInstance(mobileMenuModal)?.hide();
                }, 100);
            });
        });
        
        // Haptic feedback para dispositivos que suportam
        if ('vibrate' in navigator) {
            gridItems.forEach(item => {
                item.addEventListener('touchstart', function() {
                    navigator.vibrate(10); // Vibração leve
                }, { passive: true });
            });
        }
    }
    
    // ===== LOADING STATES =====
    function showLoading(element) {
        if (element) {
            element.classList.add('loading-state');
            element.disabled = true;
        }
    }
    
    function hideLoading(element) {
        if (element) {
            element.classList.remove('loading-state');
            element.disabled = false;
        }
    }
    
    // Aplica loading em forms
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"], input[type="submit"]');
            if (submitBtn) {
                showLoading(submitBtn);
                
                // Remove loading se form tem erro
                setTimeout(() => {
                    hideLoading(submitBtn);
                }, 10000);
            }
        });
    });
    
    // ===== NOTIFICAÇÕES MOBILE =====
    function showMobileNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `mobile-notification ${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Anima entrada
        setTimeout(() => notification.classList.add('show'), 100);
        
        // Remove após 3 segundos
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }
    
    // ===== OTIMIZAÇÕES DE PERFORMANCE =====
    
    // Lazy loading para imagens
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    observer.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
    
    // Debounce para eventos de resize
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // ===== MELHORIAS DE ACESSIBILIDADE =====
    
    // Navegação por teclado melhorada
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            document.body.classList.add('keyboard-navigation');
        }
    });
    
    document.addEventListener('mousedown', function() {
        document.body.classList.remove('keyboard-navigation');
    });
    
    // ===== UTILITÁRIOS GLOBAIS =====
    
    // Expõe funções úteis globalmente
    window.SAMAPE = window.SAMAPE || {};
    window.SAMAPE.mobile = {
        isMobile,
        isTouch,
        showNotification: showMobileNotification,
        showLoading,
        hideLoading,
        debounce
    };
    
    // ===== AJUSTES ESPECÍFICOS PARA iOS =====
    if (/iPad|iPhone|iPod/.test(navigator.userAgent)) {
        document.body.classList.add('ios-device');
        
        // Fix para inputs que ficam "grudados" no topo
        const inputs = document.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                setTimeout(() => {
                    window.scrollTo(0, 0);
                }, 100);
            });
        });
    }
    
    // ===== PREVENÇÃO DE ZOOM EM INPUTS =====
    if (isMobile) {
        const metaViewport = document.querySelector('meta[name="viewport"]');
        if (metaViewport) {
            let viewportContent = metaViewport.getAttribute('content');
            
            document.addEventListener('focusin', function(e) {
                if (e.target.matches('input, select, textarea')) {
                    metaViewport.setAttribute('content', viewportContent + ', user-scalable=no');
                }
            });
            
            document.addEventListener('focusout', function(e) {
                if (e.target.matches('input, select, textarea')) {
                    metaViewport.setAttribute('content', viewportContent);
                }
            });
        }
    }
    
    console.log('🚀 SAMAPE Mobile: Otimizações carregadas com sucesso!');
});

// ===== CSS ADICIONAL VIA JAVASCRIPT =====
const mobileStyles = `
    .touching {
        opacity: 0.7 !important;
        transform: scale(0.98) !important;
    }
    
    .scroll-indicator {
        position: absolute;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
        color: var(--bs-primary);
        font-size: 1.2rem;
        pointer-events: none;
        opacity: 1;
        transition: opacity 0.3s ease;
    }
    
    .mobile-notification {
        position: fixed;
        bottom: 100px;
        left: 16px;
        right: 16px;
        padding: 12px 16px;
        background: var(--bs-primary);
        color: white;
        border-radius: 8px;
        transform: translateY(100px);
        opacity: 0;
        transition: all 0.3s ease;
        z-index: 1050;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    .mobile-notification.show {
        transform: translateY(0);
        opacity: 1;
    }
    
    .mobile-notification.success {
        background: var(--bs-success);
    }
    
    .mobile-notification.error {
        background: var(--bs-danger);
    }
    
    .mobile-notification.warning {
        background: var(--bs-warning);
        color: var(--bs-dark);
    }
    
    .focused {
        background: rgba(var(--bs-primary-rgb), 0.1);
        border-radius: 8px;
        transition: background 0.2s ease;
    }
    
    .keyboard-navigation *:focus {
        outline: 2px solid var(--bs-primary) !important;
        outline-offset: 2px !important;
    }
    
    .ios-device .form-control {
        transform: translateZ(0);
        -webkit-appearance: none;
    }
`;

// Injeta os estilos
const styleSheet = document.createElement('style');
styleSheet.textContent = mobileStyles;
document.head.appendChild(styleSheet);