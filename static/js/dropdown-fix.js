// Correção específica para o menu dropdown de perfil
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 Dropdown Fix - Iniciando correções...');
    
    // Aguardar um pequeno delay para garantir que o Bootstrap esteja carregado
    setTimeout(function() {
        // Encontrar todos os botões dropdown na navbar
        const dropdownButtons = document.querySelectorAll('.navbar .dropdown-toggle');
        
        dropdownButtons.forEach(function(button) {
            console.log('📍 Dropdown button encontrado:', button);
            
            // Garantir que o Bootstrap dropdown seja inicializado
            if (typeof bootstrap !== 'undefined' && bootstrap.Dropdown) {
                try {
                    // Remover instância existente se houver
                    const existingDropdown = bootstrap.Dropdown.getInstance(button);
                    if (existingDropdown) {
                        existingDropdown.dispose();
                    }
                    
                    // Criar nova instância
                    const dropdown = new bootstrap.Dropdown(button);
                    console.log('✅ Bootstrap Dropdown inicializado:', dropdown);
                    
                    // Adicionar eventos personalizados como fallback
                    button.addEventListener('click', function(e) {
                        e.preventDefault();
                        e.stopPropagation();
                        
                        console.log('🖱️ Clique no dropdown detectado');
                        
                        const menu = button.nextElementSibling;
                        if (menu && menu.classList.contains('dropdown-menu')) {
                            const isShown = menu.classList.contains('show');
                            
                            // Fechar todos os outros dropdowns
                            document.querySelectorAll('.dropdown-menu.show').forEach(function(openMenu) {
                                openMenu.classList.remove('show');
                                openMenu.setAttribute('aria-expanded', 'false');
                            });
                            
                            if (!isShown) {
                                menu.classList.add('show');
                                button.setAttribute('aria-expanded', 'true');
                                console.log('✅ Menu aberto');
                            } else {
                                menu.classList.remove('show');
                                button.setAttribute('aria-expanded', 'false');
                                console.log('✅ Menu fechado');
                            }
                        }
                    });
                    
                } catch (error) {
                    console.error('❌ Erro ao inicializar Bootstrap Dropdown:', error);
                    
                    // Fallback: implementação manual
                    button.addEventListener('click', function(e) {
                        e.preventDefault();
                        e.stopPropagation();
                        
                        console.log('🔧 Usando fallback manual');
                        
                        const menu = button.nextElementSibling;
                        if (menu && menu.classList.contains('dropdown-menu')) {
                            menu.classList.toggle('show');
                            const isShown = menu.classList.contains('show');
                            button.setAttribute('aria-expanded', isShown.toString());
                        }
                    });
                }
            } else {
                console.warn('⚠️ Bootstrap não disponível, usando implementação manual');
                
                // Implementação manual se Bootstrap não estiver disponível
                button.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    const menu = button.nextElementSibling;
                    if (menu && menu.classList.contains('dropdown-menu')) {
                        // Fechar outros menus
                        document.querySelectorAll('.dropdown-menu.show').forEach(function(openMenu) {
                            if (openMenu !== menu) {
                                openMenu.classList.remove('show');
                            }
                        });
                        
                        menu.classList.toggle('show');
                        const isShown = menu.classList.contains('show');
                        button.setAttribute('aria-expanded', isShown.toString());
                        
                        console.log('✅ Menu toggled (manual):', isShown);
                    }
                });
            }
        });
        
        // Fechar dropdown ao clicar fora
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.dropdown')) {
                document.querySelectorAll('.dropdown-menu.show').forEach(function(menu) {
                    menu.classList.remove('show');
                    const button = menu.previousElementSibling;
                    if (button) {
                        button.setAttribute('aria-expanded', 'false');
                    }
                });
            }
        });
        
        // Fechar dropdown ao pressionar ESC
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                document.querySelectorAll('.dropdown-menu.show').forEach(function(menu) {
                    menu.classList.remove('show');
                    const button = menu.previousElementSibling;
                    if (button) {
                        button.setAttribute('aria-expanded', 'false');
                        button.focus(); // Retornar foco ao botão
                    }
                });
            }
        });
        
        console.log('✅ Dropdown Fix - Correções aplicadas com sucesso!');
        
    }, 500); // Aguardar 500ms para garantir que tudo esteja carregado
});
