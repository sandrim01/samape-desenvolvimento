/* SAMAPE - JavaScript Consolidado e Otimizado */
/* Versão: 1.0 - Performance otimizada */

(function() {
    'use strict';
    
    // === CONFIGURAÇÃO INICIAL === //
    function initializeApp() {
        // Force dark theme
        document.documentElement.setAttribute('data-bs-theme', 'dark');
        
        // Remove loading state
        document.body.classList.remove('loading-initial');
        document.body.classList.add('loaded');
        
        // Initialize components
        initializeBootstrapComponents();
        initializeMobileCardTables();
        
        // Setup event listeners
        setupEventListeners();
    }
    
    // === BOOTSTRAP COMPONENTS === //
    function initializeBootstrapComponents() {
        // Initialize dropdowns
        const dropdowns = document.querySelectorAll('[data-bs-toggle="dropdown"]');
        dropdowns.forEach(dropdown => {
            try {
                new bootstrap.Dropdown(dropdown);
            } catch (e) {
                console.warn('Erro ao inicializar dropdown:', e);
            }
        });
        
        // Initialize sidebar dropdown specifically
        const sidebarDropdown = document.getElementById('sidebarProfileDropdown');
        if (sidebarDropdown) {
            try {
                new bootstrap.Dropdown(sidebarDropdown);
            } catch (e) {
                console.warn('Erro ao inicializar dropdown da sidebar:', e);
            }
        }
    }
    
    // === LAZY LOADING DE RECURSOS === //
    function loadLazyResources() {
        // Load jQuery only if needed
        if (typeof jQuery === 'undefined' && document.querySelector('.requires-jquery')) {
            loadScript('https://code.jquery.com/jquery-3.6.0.min.js');
        }
        
        // Load Fancybox only if needed
        if (document.querySelector('[data-fancybox]')) {
            loadScript('https://cdn.jsdelivr.net/npm/@fancyapps/ui@5.0/dist/fancybox/fancybox.umd.js', 
                function() {
                    if (typeof Fancybox !== 'undefined') {
                        Fancybox.bind("[data-fancybox]", {
                            Toolbar: {
                                display: [
                                    { id: "prev", position: "center" },
                                    { id: "counter", position: "center" },
                                    { id: "next", position: "center" },
                                    { id: "zoom", position: "right" },
                                    { id: "close", position: "right" },
                                ],
                            },
                            Thumbs: { autoStart: false },
                            Image: { zoom: true },
                            on: {
                                initLayout: (fancybox) => {
                                    const $container = fancybox.$container;
                                    if ($container) {
                                        $container.style.setProperty("--f-bg-color", "rgba(33, 37, 41, 0.95)");
                                        $container.style.setProperty("--f-button-color", "#fff");
                                    }
                                }
                            }
                        });
                    }
                }
            );
        }
        
        // Load Chart.js only if needed
        if (document.querySelector('canvas[data-chart]')) {
            loadScript('https://cdn.jsdelivr.net/npm/chart.js');
        }
    }
    
    // === HELPER FUNCTIONS === //
    function loadScript(src, callback) {
        const script = document.createElement('script');
        script.src = src;
        script.async = true;
        if (callback) script.onload = callback;
        document.head.appendChild(script);
    }
    
    // === NOTIFICAÇÕES === //
    window.showSnack = function(message, duration = 3000) {
        const snack = document.getElementById('snackNotification');
        const text = document.getElementById('snackText');
        
        if (snack && text) {
            text.textContent = message;
            snack.classList.add('show');
            
            setTimeout(() => {
                snack.classList.remove('show');
            }, duration);
        }
    };
    
    // === MOBILE CARD TABLES === //
    function initializeMobileCardTables() {
        document.querySelectorAll('.mobile-card-table').forEach(container => {
            const table = container.querySelector('table');
            if (!table) return;
            
            const headerRow = table.querySelector('thead tr');
            if (!headerRow) return;
            
            const headings = Array.from(headerRow.querySelectorAll('th')).map(th => th.textContent.trim());
            const rows = Array.from(table.querySelectorAll('tbody tr'));
            
            rows.forEach(row => {
                const values = Array.from(row.querySelectorAll('td')).map(td => td.innerHTML);
                
                // Create mobile card
                const card = document.createElement('div');
                card.className = 'mobile-card-row d-lg-none';
                
                // Card header (first element)
                const header = document.createElement('div');
                header.className = 'row-header';
                
                const title = document.createElement('div');
                title.className = 'title';
                title.innerHTML = values[0];
                
                // Status badge in header if exists
                const statusIndex = values.findIndex(v => v.includes('badge') || v.includes('status'));
                
                if (statusIndex !== -1) {
                    const status = document.createElement('div');
                    status.className = 'status';
                    status.innerHTML = values[statusIndex];
                    
                    header.appendChild(title);
                    header.appendChild(status);
                } else {
                    header.appendChild(title);
                }
                
                card.appendChild(header);
                
                // Card content (except first element and possible status)
                for (let i = 1; i < values.length; i++) {
                    if (i === statusIndex) continue;
                    
                    // Skip empty cells
                    if (!values[i] || values[i].trim() === '') continue;
                    
                    // Actions section
                    if (values[i].includes('btn') || values[i].includes('fa-')) {
                        const actions = document.createElement('div');
                        actions.className = 'row-actions';
                        actions.innerHTML = values[i];
                        card.appendChild(actions);
                        continue;
                    }
                    
                    const item = document.createElement('div');
                    item.className = 'row-item';
                    
                    const label = document.createElement('div');
                    label.className = 'item-label';
                    label.textContent = headings[i];
                    
                    const value = document.createElement('div');
                    value.className = 'item-value';
                    value.innerHTML = values[i];
                    
                    item.appendChild(label);
                    item.appendChild(value);
                    card.appendChild(item);
                }
                
                container.appendChild(card);
            });
        });
    }
    
    // === EVENT LISTENERS === //
    function setupEventListeners() {
        // Mobile menu toggle
        const menuToggle = document.querySelector('[data-bs-toggle="sidebar"]');
        const sidebar = document.querySelector('.sidebar');
        
        if (menuToggle && sidebar) {
            menuToggle.addEventListener('click', function() {
                sidebar.classList.toggle('show');
            });
        }
        
        // Close sidebar on mobile when clicking outside
        document.addEventListener('click', function(e) {
            if (window.innerWidth <= 768) {
                const sidebar = document.querySelector('.sidebar');
                const menuToggle = document.querySelector('[data-bs-toggle="sidebar"]');
                
                if (sidebar && sidebar.classList.contains('show') && 
                    !sidebar.contains(e.target) && 
                    !menuToggle.contains(e.target)) {
                    sidebar.classList.remove('show');
                }
            }
        });
        
        // Form validation improvements
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', function(e) {
                if (!form.checkValidity()) {
                    e.preventDefault();
                    e.stopPropagation();
                }
                form.classList.add('was-validated');
            });
        });
    }
    
    // === PERFORMANCE OPTIMIZATIONS === //
    function optimizePerformance() {
        // Lazy load images
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        imageObserver.unobserve(img);
                    }
                });
            });
            
            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
        
        // Debounce resize events
        let resizeTimer;
        window.addEventListener('resize', function() {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(function() {
                // Handle resize events
                initializeMobileCardTables();
            }, 250);
        });
    }
    
    // === INITIALIZATION === //
    // Initialize immediately for critical components
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeApp);
    } else {
        initializeApp();
    }
    
    // Load non-critical resources after page load
    window.addEventListener('load', function() {
        setTimeout(loadLazyResources, 1000);
        optimizePerformance();
    });
    
})();