// ============================================
// DIAGNÃ“STICO: Verificar ambiente
// ============================================
console.log('=== DIAGNÃ“STICO DE AMBIENTE ===');
console.log('jQuery carregado:', typeof $ !== 'undefined');
console.log('Bootstrap carregado:', typeof bootstrap !== 'undefined');

// Verificar CSRF
const csrfMeta = document.querySelector('meta[name="csrf-token"]');
console.log('Meta CSRF encontrado:', csrfMeta !== null);
if (csrfMeta) {
    console.log('CSRF token value:', csrfMeta.getAttribute('content'));
}

// Testar click em botÃ£o
window.testButton = function() {
    console.log('Teste de botÃ£o funcionando!');
    alert('JavaScript estÃ¡ funcionando!');
};

let currentOrderId = null;

// Verificar se deve abrir o modal de criaÃ§Ã£o automaticamente
$(document).ready(function() {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('action') === 'create') {
        const preselectedClientId = urlParams.get('client_id');
        
        // Remover os parÃ¢metros da URL sem recarregar a pÃ¡gina
        const newUrl = window.location.protocol + "//" + window.location.host + window.location.pathname;
        window.history.replaceState({path:newUrl}, '', newUrl);
        
        // Abrir o modal de criaÃ§Ã£o com cliente prÃ©-selecionado
        setTimeout(function() {
            openCreateModal(preselectedClientId);
        }, 500);
    }
});

// Aguardar o carregamento do jQuery antes de executar
function initializeModal() {
    if (typeof $ === 'undefined') {
        setTimeout(initializeModal, 100);
        return;
    }
    
    $(document).ready(function() {
        // Auto-submit form when filters change
        $('#status, #client, #responsive, #date_from, #date_to').change(function() {
            $('#searchForm').submit();
        });
        
        console.log('jQuery carregado e modal inicializado');
    });
}

// Inicializar quando o DOM estiver pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeModal);
} else {
    initializeModal();
}

// FunÃ§Ã£o para visualizar ordem de serviÃ§o em modal
function viewServiceOrder(orderId) {
    console.log('viewServiceOrder chamado com ID:', orderId);
    
    // Verificar se jQuery estÃ¡ disponÃ­vel
    if (typeof $ === 'undefined') {
        console.error('jQuery nÃ£o estÃ¡ carregado');
        return;
    }
    currentOrderId = orderId;
    
    // Abrir modal
    const modal = new bootstrap.Modal(document.getElementById('viewServiceOrderModal'));
    modal.show();
    
    // Resetar conteÃºdo do modal
    $('#modalBodyContent').html(`
        <div class="text-center py-3">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Carregando...</span>
            </div>
        </div>
    `);
    
    // Buscar dados da OS via AJAX
    console.log('Fazendo requisiÃ§Ã£o AJAX para:', '/os/' + orderId + '/modal');
    $.ajax({
        url: '/os/' + orderId + '/modal',
        method: 'GET',
        dataType: 'json',
        timeout: 10000,
        success: function(data) {
            console.log('Dados recebidos da API:', data);
            renderOrderModal(data);
            // Configurar botÃµes do modal
            $('#editOrderBtn').show();
            $('#fullViewBtn').attr('href', '/os/' + orderId).show();
            
            // Configurar botÃ£o WhatsApp com dados da OS
            const pdfBtn = $('#pdfWhatsAppBtn');
            pdfBtn.attr('href', '/os/' + orderId + '/pdf');
            pdfBtn.attr('data-order-id', orderId);
            pdfBtn.attr('data-client-name', data.client.name || 'Cliente');
            pdfBtn.attr('data-client-phone', data.client.phone || '');
            pdfBtn.attr('data-description', (data.description || data.service_details || 'Ordem de ServiÃ§o').substring(0, 50));
            pdfBtn.show();
        },
        error: function(xhr, status, error) {
            console.error('Erro na requisiÃ§Ã£o AJAX:', {
                status: xhr.status,
                statusText: xhr.statusText,
                responseText: xhr.responseText,
                error: error
            });
            $('#modalBodyContent').html(`
                <div class="alert alert-danger" role="alert">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    <strong>Erro ao carregar a ordem de serviÃ§o:</strong><br>
                    Status: ${xhr.status}<br>
                    Erro: ${error}<br>
                    Resposta: ${xhr.responseText || 'Nenhuma resposta'}
                </div>
            `);
            $('#editOrderBtn').hide();
            $('#fullViewBtn').hide();
        }
    });
}

// FunÃ§Ã£o para renderizar os dados da OS no modal
function renderOrderModal(order) {
    console.log('renderOrderModal chamado com dados:', order);
    
    if (!order) {
        console.error('Dados da ordem nÃ£o fornecidos');
        return;
    }
    
    const statusClass = {
        'aberta': 'warning',
        'em_andamento': 'info', 
        'fechada': 'success'
    }[order.status] || 'secondary';
    
    const modalContent = `
        <div class="row">
            <!-- InformaÃ§Ãµes BÃ¡sicas -->
            <div class="col-md-6">
                <div class="card mb-3">
                    <div class="card-header">
                        <h6 class="mb-0"><i class="fas fa-info-circle me-2"></i>InformaÃ§Ãµes BÃ¡sicas</h6>
                    </div>
                    <div class="card-body">
                        <p><strong>OS #:</strong> ${order.id}</p>
                        <p><strong>Status:</strong> <span class="badge bg-${statusClass}">${order.status_label}</span></p>
                        <p><strong>Criada em:</strong> ${order.created_at}</p>
                        <p><strong>Atualizada em:</strong> ${order.updated_at}</p>
                        <p><strong>ResponsÃ¡vel:</strong> ${order.responsible.name}</p>
                    </div>
                </div>
            </div>
            
            <!-- Cliente -->
            <div class="col-md-6">
                <div class="card mb-3">
                    <div class="card-header">
                        <h6 class="mb-0"><i class="fas fa-user me-2"></i>Cliente</h6>
                    </div>
                    <div class="card-body">
                        <p><strong>Nome:</strong> ${order.client.name}</p>
                        <p><strong>Telefone:</strong> ${order.client.phone}</p>
                        <p><strong>E-mail:</strong> ${order.client.email}</p>
                    </div>
                </div>
            </div>
            
            <!-- Equipamentos -->
            <div class="col-md-6">
                <div class="card mb-3">
                    <div class="card-header">
                        <h6 class="mb-0"><i class="fas fa-cogs me-2"></i>Equipamento(s)</h6>
                    </div>
                    <div class="card-body">
                        ${order.equipment_list && order.equipment_list.length > 0 ? 
                            order.equipment_list.map((equipment, index) => `
                                ${index > 0 ? '<hr class="my-2">' : ''}
                                <p><strong>Modelo:</strong> ${equipment.model}</p>
                                <p><strong>Marca:</strong> ${equipment.brand}</p>
                                <p><strong>NÂº SÃ©rie:</strong> ${equipment.serial_number}</p>
                                <p class="mb-0"><strong>Ano:</strong> ${equipment.year}</p>
                            `).join('') 
                            : '<p class="text-muted mb-0">Nenhum equipamento associado</p>'
                        }
                    </div>
                </div>
            </div>
            
            <!-- Valores e Kilometragem -->
            <div class="col-md-6">
                <div class="card mb-3">
                    <div class="card-header">
                        <h6 class="mb-0"><i class="fas fa-dollar-sign me-2"></i>Valores e Kilometragem</h6>
                    </div>
                    <div class="card-body">
                        ${(order.km_inicial !== 'NÃ£o informado' || order.km_final !== 'NÃ£o informado') ? `
                            <h6 class="text-primary mb-2"><i class="fas fa-tachometer-alt me-1"></i> Kilometragem</h6>
                            ${order.km_inicial !== 'NÃ£o informado' ? `<p class="mb-1"><strong>KM Inicial:</strong> ${order.km_inicial}</p>` : ''}
                            ${order.km_final !== 'NÃ£o informado' ? `<p class="mb-1"><strong>KM Final:</strong> ${order.km_final}</p>` : ''}
                            ${order.km_total && order.km_total !== 'NÃ£o informado' ? 
                                `<p class="mb-1"><strong>KM Total:</strong> ${order.km_total}</p>` : ''
                            }
                            ${order.km_rate && order.km_rate !== 'NÃ£o informado' ? 
                                `<p class="mb-1"><strong>Taxa por KM:</strong> R$ ${order.km_rate}</p>` : ''
                            }
                            ${order.km_value && order.km_value !== 'NÃ£o informado' ? 
                                `<p class="mb-2"><strong>Valor KM:</strong> <span class="text-success">R$ ${order.km_value}</span></p>` : ''
                            }
                            <hr class="my-2">
                        ` : ''}
                        
                        <h6 class="text-success mb-2"><i class="fas fa-calculator me-1"></i> Valores</h6>
                        ${order.estimated_value !== 'NÃ£o informado' ? 
                            `<p class="mb-1"><strong>Valor Estimado:</strong> ${order.estimated_value}</p>` : ''
                        }
                        ${order.labor_value && order.labor_value !== 'NÃ£o informado' ? 
                            `<p class="mb-1"><strong>MÃ£o de Obra:</strong> R$ ${order.labor_value}</p>` : ''
                        }
                        ${order.parts_value && order.parts_value !== 'NÃ£o informado' ? 
                            `<p class="mb-1"><strong>PeÃ§as:</strong> R$ ${order.parts_value}</p>` : ''
                        }
                        ${order.total_value && order.total_value !== 'NÃ£o informado' ? 
                            `<p class="mb-2"><strong>TOTAL CALCULADO:</strong> <span class="text-primary fw-bold">R$ ${order.total_value}</span></p>` : ''
                        }
                        ${(order.labor_value && order.labor_value !== 'NÃ£o informado') || 
                          (order.parts_value && order.parts_value !== 'NÃ£o informado') || 
                          (order.km_value && order.km_value !== 'NÃ£o informado') ? 
                            `<hr class="my-2">` : ''
                        }
                        ${order.invoice_amount !== 'NÃ£o informado' ? 
                            `<p class="mb-0"><strong>Valor da Nota:</strong> ${order.invoice_amount}</p>` : ''
                        }
                    </div>
                </div>
            </div>
            
            <!-- DescriÃ§Ã£o do ServiÃ§o -->
            <div class="col-12">
                <div class="card mb-3">
                    <div class="card-header">
                        <h6 class="mb-0"><i class="fas fa-clipboard-list me-2"></i>DescriÃ§Ã£o do ServiÃ§o</h6>
                    </div>
                    <div class="card-body">
                        <p class="mb-0">${order.description || 'Nenhuma descriÃ§Ã£o informada'}</p>
                    </div>
                </div>
            </div>
            
            <!-- Listagem de PeÃ§as (se houver) -->
            ${order.parts_list_number ? `
            <div class="col-12">
                <div class="card mb-3">
                    <div class="card-header">
                        <h6 class="mb-0"><i class="fas fa-list-alt me-2"></i>Listagem de PeÃ§as</h6>
                    </div>
                    <div class="card-body">
                        <p class="mb-2">
                            <span class="badge bg-info">${order.parts_list_number}</span>
                        </p>
                        <div class="d-flex gap-2">
                            ${order.parts_list_id ? `
                                <a href="/lista-pecas/${order.parts_list_id}" target="_blank" class="btn btn-sm btn-outline-primary">
                                    <i class="fas fa-eye"></i> Ver Listagem
                                </a>
                                <a href="/lista-pecas/${order.parts_list_id}/pdf" class="btn btn-sm btn-success" onclick="openWhatsAppAfterDownload(event)">
                                    <i class="fab fa-whatsapp"></i> Baixar PDF
                                </a>
                            ` : ''}
                        </div>
                    </div>
                </div>
            </div>
            ` : ''}
            
            <!-- Detalhes do ServiÃ§o -->
            ${order.service_details && order.service_details !== 'Nenhum detalhe informado' ? `
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h6 class="mb-0"><i class="fas fa-sticky-note me-2"></i>Detalhes do ServiÃ§o</h6>
                    </div>
                    <div class="card-body">
                        <p class="mb-0">${order.service_details}</p>
                    </div>
                </div>
            </div>
            ` : ''}
            
            <!-- InformaÃ§Ãµes da Nota Fiscal (se houver) -->
            ${order.invoice_number && order.invoice_number !== 'NÃ£o informado' ? `
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h6 class="mb-0"><i class="fas fa-file-invoice me-2"></i>Nota Fiscal</h6>
                    </div>
                    <div class="card-body">
                        <p class="mb-0"><strong>NÃºmero da Nota:</strong> ${order.invoice_number}</p>
                        <p class="mb-0"><strong>Valor:</strong> ${order.invoice_amount}</p>
                    </div>
                </div>
            </div>
            ` : ''}
        </div>
        
        ${order.financial_entries_count > 0 ? `
        <div class="alert alert-info mt-3" role="alert">
            <i class="fas fa-info-circle me-2"></i>
            Esta OS possui ${order.financial_entries_count} entrada(s) financeira(s) associada(s).
        </div>
        ` : ''}
    `;
    
    $('#modalBodyContent').html(modalContent);
}

// FunÃ§Ã£o para editar a OS atual
function editCurrentOrder() {
    if (currentOrderId) {
        openEditModal(currentOrderId);
    }
}

// FunÃ§Ã£o para abrir WhatsApp apÃ³s download do PDF
function openWhatsAppAfterDownload(event) {
    // NÃ£o prevenir o comportamento padrÃ£o - deixar o download acontecer
    
    // Aguardar 1 segundo para o download iniciar
    setTimeout(function() {
        // Abre WhatsApp Web diretamente (evita bloqueio do protocolo whatsapp://)
        window.open('https://web.whatsapp.com/', '_blank');
    }, 1000);
}

// FunÃ§Ã£o para abrir o WhatsApp apÃ³s baixar o PDF da OS
function openWhatsAppAfterOSDownload(event, buttonElement) {
    console.log('openWhatsAppAfterOSDownload chamada no modal');
    
    // Pega os dados do botÃ£o
    const orderId = buttonElement.dataset.orderId || buttonElement.getAttribute('data-order-id');
    const clientName = buttonElement.dataset.clientName || buttonElement.getAttribute('data-client-name') || 'Cliente';
    const clientPhone = buttonElement.dataset.clientPhone || buttonElement.getAttribute('data-client-phone') || '';
    const description = buttonElement.dataset.description || buttonElement.getAttribute('data-description') || '';
    const pdfUrl = buttonElement.getAttribute('href');
    
    console.log('Dados modal:', { orderId, clientName, clientPhone, pdfUrl });
    
    // IMPORTANTE: NÃ£o Ã© possÃ­vel enviar arquivo automaticamente via WhatsApp Web
    // por limitaÃ§Ãµes de seguranÃ§a do navegador e da API do WhatsApp.
    // A melhor soluÃ§Ã£o Ã© abrir o PDF e instruir o usuÃ¡rio.
    
    // Abre o PDF em nova aba para o usuÃ¡rio baixar
    if (pdfUrl && pdfUrl !== '#') {
        try {
            window.open(pdfUrl, '_blank');
            console.log('PDF aberto em nova aba (modal)');
        } catch (e) {
            console.error('Erro ao abrir PDF no modal:', e);
        }
    } else {
        console.error('URL do PDF invÃ¡lida:', pdfUrl);
    }
    
    // Cria mensagem CLARA explicando que o anexo precisa ser manual
    const fileName = `OS_${orderId}_${clientName.replace(/\s+/g, '_')}.pdf`;
    let whatsappMessage = `ðŸ“‹ *Ordem de ServiÃ§o #${orderId}*`;
    
    if (clientName && clientName !== 'Cliente') {
        whatsappMessage += `\nðŸ‘¤ Cliente: ${clientName}`;
    }
    
    if (description) {
        whatsappMessage += `\nðŸ“ ${description}`;
    }
    
    whatsappMessage += `\n\nâš ï¸ *IMPORTANTE:*`;
    whatsappMessage += `\n\n1ï¸âƒ£ O PDF foi aberto em outra aba do navegador`;
    whatsappMessage += `\n2ï¸âƒ£ Clique em "Baixar" (Ã­cone de download) no PDF`;
    whatsappMessage += `\n3ï¸âƒ£ Volte aqui e clique no Ã­cone ðŸ“Ž (anexo)`;
    whatsappMessage += `\n4ï¸âƒ£ Selecione o arquivo: *${fileName}*`;
    whatsappMessage += `\n\n_Obs: Por seguranÃ§a, o WhatsApp nÃ£o permite envio automÃ¡tico de arquivos via navegador._`;
    whatsappMessage += `\n\nâœ… SAMAPE`;
    
    // Codifica a mensagem para URL
    const encodedMessage = encodeURIComponent(whatsappMessage);
        whatsappMessage += `\nðŸ‘¤ Cliente: ${clientName}`;
    }
    
    if (description) {
        whatsappMessage += `\nðŸ“ ${description}`;
    }
    
    whatsappMessage += `\n\nðŸ“Ž *O PDF estÃ¡ sendo baixado agora!*`;
    whatsappMessage += `\n\n_Basta clicar no Ã­cone de anexo (ï¿½) aqui no WhatsApp e selecionar o arquivo "${fileName}" que acabou de ser baixado._`;
    whatsappMessage += `\n\nâœ… SAMAPE - Sistema de Gerenciamento`;
    
    // Codifica a mensagem para URL
    const encodedMessage = encodeURIComponent(whatsappMessage);
    
    // Aguarda 500ms e abre o WhatsApp Web
    setTimeout(function() {
        let whatsappUrl;
        
        try {
            // Se tem telefone do cliente, valida e abre direto para ele no WhatsApp Web
            if (clientPhone && clientPhone.trim() !== '') {
                // Remove caracteres nÃ£o numÃ©ricos do telefone
                let phoneNumber = clientPhone.replace(/\D/g, '');
                
                console.log('Telefone original (modal):', clientPhone);
                console.log('Telefone limpo (modal):', phoneNumber);
                
                // Valida se o nÃºmero tem pelo menos 10 dÃ­gitos (DDD + nÃºmero)
                if (phoneNumber.length >= 10 && phoneNumber.length <= 13) {
                    // Remove 55 do inÃ­cio se jÃ¡ existir (evita duplicaÃ§Ã£o)
                    if (phoneNumber.startsWith('55')) {
                        phoneNumber = phoneNumber.substring(2);
                    }
                    
                    // Adiciona cÃ³digo do Brasil (55)
                    phoneNumber = '55' + phoneNumber;
                    
                    // Abre WhatsApp Web com nÃºmero e mensagem
                    whatsappUrl = `https://web.whatsapp.com/send?phone=${phoneNumber}&text=${encodedMessage}`;
                    console.log('Abrindo WhatsApp modal com telefone validado:', phoneNumber);
                    window.open(whatsappUrl, '_blank');
                } else {
                    // NÃºmero invÃ¡lido, abre sem nÃºmero especÃ­fico
                    console.warn('NÃºmero de telefone invÃ¡lido (modal - tamanho:', phoneNumber.length, '):', phoneNumber);
                    whatsappUrl = `https://web.whatsapp.com/send?text=${encodedMessage}`;
                    console.log('Abrindo WhatsApp modal sem telefone (nÃºmero invÃ¡lido)');
                    window.open(whatsappUrl, '_blank');
                }
            } else {
                // Se nÃ£o tem telefone, abre WhatsApp Web para escolher contato
                whatsappUrl = `https://web.whatsapp.com/send?text=${encodedMessage}`;
                console.log('Abrindo WhatsApp modal sem telefone (campo vazio)');
                window.open(whatsappUrl, '_blank');
            }
        } catch (e) {
            console.error('Erro ao abrir WhatsApp no modal:', e);
            alert('Erro ao abrir WhatsApp. Verifique o console para mais detalhes.');
        }
    }, 500);
}

// FunÃ§Ã£o para abrir modal de ediÃ§Ã£o
function openEditModal(orderId) {
    console.log('openEditModal chamado com ID:', orderId);
    
    // Verificar se jQuery estÃ¡ disponÃ­vel
    if (typeof $ === 'undefined') {
        console.error('jQuery nÃ£o estÃ¡ carregado');
        return;
    }
    
    currentOrderId = orderId;
    
    // Fechar modal de visualizaÃ§Ã£o se estiver aberto
    $('#viewServiceOrderModal').modal('hide');
    
    // Abrir modal de ediÃ§Ã£o
    const editModal = new bootstrap.Modal(document.getElementById('editServiceOrderModal'));
    editModal.show();
    
    // Resetar conteÃºdo do modal
    $('#editModalBodyContent').html(`
        <div class="text-center py-3">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Carregando...</span>
            </div>
        </div>
    `);
    
    // Buscar dados da OS para ediÃ§Ã£o via AJAX
    console.log('Fazendo requisiÃ§Ã£o AJAX para:', '/os/' + orderId + '/edit-modal');
    $.ajax({
        url: '/os/' + orderId + '/edit-modal',
        method: 'GET',
        dataType: 'json',
        timeout: 10000,
        success: function(data) {
            console.log('Dados recebidos para ediÃ§Ã£o:', data);
            renderEditModal(data);
        },
        error: function(xhr, status, error) {
            console.error('Erro na requisiÃ§Ã£o AJAX:', {
                status: xhr.status,
                statusText: xhr.statusText,
                responseText: xhr.responseText,
                error: error
            });
            $('#editModalBodyContent').html(`
                <div class="alert alert-danger" role="alert">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    <strong>Erro ao carregar formulÃ¡rio de ediÃ§Ã£o:</strong><br>
                    Status: ${xhr.status}<br>
                    Erro: ${error}<br>
                    Resposta: ${xhr.responseText || 'Nenhuma resposta'}
                </div>
            `);
        }
    });
}

// FunÃ§Ã£o para renderizar formulÃ¡rio de ediÃ§Ã£o
function renderEditModal(data) {
    console.log('renderEditModal chamado com dados:', data);
    
    if (!data) {
        console.error('Dados da ordem nÃ£o fornecidos para ediÃ§Ã£o');
        return;
    }
    
    // Gerar opÃ§Ãµes para clientes
    const clientOptions = data.clients.map(client => 
        `<option value="${client.id}" ${client.id === data.client_id ? 'selected' : ''}>${client.name}</option>`
    ).join('');
    
    // Gerar opÃ§Ãµes para responsÃ¡veis
    const userOptions = '<option value="0" ' + (data.responsible_id === 0 ? 'selected' : '') + '>A ser definido</option>' +
        data.users.map(user => 
            `<option value="${user.id}" ${user.id === data.responsible_id ? 'selected' : ''}>${user.name}</option>`
        ).join('');
    
    // Gerar checkboxes para equipamentos
    const equipmentCheckboxes = data.equipment.map(equipment => `
        <div class="form-check">
            <input class="form-check-input" type="checkbox" value="${equipment.id}" id="equipment_${equipment.id}"
                   ${data.equipment_ids.includes(equipment.id) ? 'checked' : ''}>
            <label class="form-check-label" for="equipment_${equipment.id}">
                ${equipment.model} - ${equipment.brand}
            </label>
        </div>
    `).join('');
    
    const editFormContent = `
        <form id="editServiceOrderForm">
            <div class="row">
                <div class="col-md-6">
                    <div class="mb-3">
                        <label for="edit_client_id" class="form-label">Cliente *</label>
                        <select class="form-select" id="edit_client_id" required>
                            <option value="">Selecione um cliente</option>
                            ${clientOptions}
                        </select>
                    </div>
                </div>
                
                <div class="col-md-6">
                    <div class="mb-3">
                        <label for="edit_responsible_id" class="form-label">ResponsÃ¡vel</label>
                        <select class="form-select" id="edit_responsible_id">
                            ${userOptions}
                        </select>
                    </div>
                </div>
                
                <div class="col-12">
                    <div class="mb-3">
                        <label for="edit_description" class="form-label">DescriÃ§Ã£o *</label>
                        <textarea class="form-control" id="edit_description" rows="3" required>${data.description}</textarea>
                    </div>
                </div>
                
                <!-- Listagem de PeÃ§as (se houver) -->
                ${data.parts_list_number ? `
                <div class="col-12">
                    <div class="alert alert-info" role="alert">
                        <h6 class="alert-heading mb-2"><i class="fas fa-list-alt me-2"></i>Listagem de PeÃ§as Vinculada</h6>
                        <p class="mb-2">
                            <span class="badge bg-info">${data.parts_list_number}</span>
                        </p>
                        ${data.parts_list_id ? `
                            <a href="/lista-pecas/${data.parts_list_id}" target="_blank" class="btn btn-sm btn-outline-primary">
                                <i class="fas fa-external-link-alt"></i> Abrir em Nova Aba
                            </a>
                        ` : ''}
                    </div>
                </div>
                ` : ''}
                
                <div class="col-md-4">
                    <div class="mb-3">
                        <label for="edit_estimated_value" class="form-label">Valor Estimado</label>
                        <input type="number" class="form-control" id="edit_estimated_value" step="0.01" value="${data.estimated_value}">
                    </div>
                </div>
                
                <div class="col-md-4">
                    <div class="mb-3">
                        <label for="edit_status" class="form-label">Status</label>
                        <select class="form-select" id="edit_status">
                            <option value="aberta" ${data.status === 'aberta' ? 'selected' : ''}>Aberta</option>
                            <option value="em_andamento" ${data.status === 'em_andamento' ? 'selected' : ''}>Em Andamento</option>
                            <option value="fechada" ${data.status === 'fechada' ? 'selected' : ''}>Fechada</option>
                        </select>
                    </div>
                </div>
                
                <!-- Card de Kilometragem -->
                <div class="col-12">
                    <div class="card mb-3">
                        <div class="card-header bg-primary text-white">
                            <h6 class="mb-0"><i class="fas fa-tachometer-alt me-2"></i>Kilometragem</h6>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-3">
                                    <div class="mb-3">
                                        <label for="edit_km_inicial" class="form-label">KM Inicial</label>
                                        <input type="number" class="form-control" id="edit_km_inicial" step="0.01" value="${data.km_inicial}" onchange="calculateEditKmTotal()">
                                    </div>
                                </div>
                                
                                <div class="col-md-3">
                                    <div class="mb-3">
                                        <label for="edit_km_final" class="form-label">KM Final</label>
                                        <input type="number" class="form-control" id="edit_km_final" step="0.01" value="${data.km_final}" onchange="calculateEditKmTotal()">
                                    </div>
                                </div>
                                
                                <div class="col-md-3">
                                    <div class="mb-3">
                                        <label for="edit_km_total" class="form-label">KM Total</label>
                                        <input type="number" class="form-control" id="edit_km_total" step="0.01" value="${data.km_total}" readonly>
                                    </div>
                                </div>
                                
                                <div class="col-md-3">
                                    <div class="mb-3">
                                        <label for="edit_km_rate" class="form-label">Valor por KM (R$)</label>
                                        <input type="number" class="form-control" id="edit_km_rate" step="0.01" value="${data.km_rate}" onchange="calculateEditKmValue()">
                                    </div>
                                </div>
                                
                                <div class="col-md-12">
                                    <div class="mb-0">
                                        <label for="edit_km_value" class="form-label">Valor Total KM (R$)</label>
                                        <input type="number" class="form-control" id="edit_km_value" step="0.01" value="${data.km_value}" readonly>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Card de Valores -->
                <div class="col-12">
                    <div class="card mb-3">
                        <div class="card-header bg-success text-white">
                            <h6 class="mb-0"><i class="fas fa-dollar-sign me-2"></i>Valores</h6>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-4">
                                    <div class="mb-3">
                                        <label for="edit_labor_value" class="form-label">MÃ£o de Obra (R$)</label>
                                        <input type="number" class="form-control" id="edit_labor_value" step="0.01" value="${data.labor_value}" onchange="calculateEditTotalValue()">
                                    </div>
                                </div>
                                
                                <div class="col-md-4">
                                    <div class="mb-3">
                                        <label for="edit_parts_value" class="form-label">PeÃ§as (R$)</label>
                                        <input type="number" class="form-control" id="edit_parts_value" step="0.01" value="${data.parts_value}" onchange="calculateEditTotalValue()">
                                    </div>
                                </div>
                                
                                <div class="col-md-4">
                                    <div class="mb-0">
                                        <label for="edit_total_value" class="form-label">Valor Total (R$)</label>
                                        <input type="number" class="form-control bg-light fw-bold" id="edit_total_value" step="0.01" value="${data.total_value}" readonly>
                                        <small class="text-muted">Calculado: KM + MÃ£o de Obra + PeÃ§as</small>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="col-12">
                    <div class="mb-3">
                        <label for="edit_service_details" class="form-label">Detalhes do ServiÃ§o</label>
                        <textarea class="form-control" id="edit_service_details" rows="3">${data.service_details}</textarea>
                    </div>
                </div>
                
                <div class="col-12">
                    <div class="mb-3">
                        <label class="form-label">Equipamentos</label>
                        <div class="equipment-checkboxes" style="max-height: 200px; overflow-y: auto;">
                            ${equipmentCheckboxes}
                        </div>
                    </div>
                </div>
            </div>
        </form>
    `;
    
    $('#editModalBodyContent').html(editFormContent);
}

// FunÃ§Ã£o para salvar alteraÃ§Ãµes da OS
function saveServiceOrder() {
    console.log('saveServiceOrder chamado');
    
    if (!currentOrderId) {
        console.error('ID da ordem nÃ£o definido');
        return;
    }
    
    // Coletar dados do formulÃ¡rio
    const clientIdValue = $('#edit_client_id').val();
    const responsibleIdValue = $('#edit_responsible_id').val();
    const descriptionValue = $('#edit_description').val();
    const estimatedValue = $('#edit_estimated_value').val();
    const kmInicialValue = $('#edit_km_inicial').val();
    const kmFinalValue = $('#edit_km_final').val();
    const kmTotalValue = $('#edit_km_total').val();
    const kmRateValue = $('#edit_km_rate').val();
    const kmValueField = $('#edit_km_value').val();
    const laborValueField = $('#edit_labor_value').val();
    const partsValueField = $('#edit_parts_value').val();
    const totalValueField = $('#edit_total_value').val();
    const statusValue = $('#edit_status').val();
    const serviceDetailsValue = $('#edit_service_details').val();
    
    console.log('Valores coletados do formulÃ¡rio:', {
        clientIdValue,
        responsibleIdValue,
        descriptionValue,
        estimatedValue,
        kmInicialValue,
        kmFinalValue,
        kmTotalValue,
        kmRateValue,
        kmValueField,
        laborValueField,
        partsValueField,
        totalValueField,
        statusValue,
        serviceDetailsValue
    });
    
    const formData = {
        client_id: clientIdValue ? parseInt(clientIdValue) : null,
        responsible_id: responsibleIdValue ? parseInt(responsibleIdValue) : 0,
        description: descriptionValue || '',
        estimated_value: estimatedValue ? parseFloat(estimatedValue) : null,
        km_inicial: kmInicialValue ? parseFloat(kmInicialValue) : 0,
        km_final: kmFinalValue ? parseFloat(kmFinalValue) : 0,
        km_total: kmTotalValue ? parseFloat(kmTotalValue) : 0,
        km_rate: kmRateValue ? parseFloat(kmRateValue) : 0,
        km_value: kmValueField ? parseFloat(kmValueField) : 0,
        labor_value: laborValueField ? parseFloat(laborValueField) : 0,
        parts_value: partsValueField ? parseFloat(partsValueField) : 0,
        total_value: totalValueField ? parseFloat(totalValueField) : 0,
        status: statusValue || 'aberta',
        service_details: serviceDetailsValue || '',
        equipment_ids: []
    };
    
    // Coletar equipamentos selecionados
    $('.equipment-checkboxes input[type="checkbox"]:checked').each(function() {
        formData.equipment_ids.push(parseInt($(this).val()));
    });
    
    console.log('Dados finais para salvar:', formData);
    
    // ValidaÃ§Ãµes bÃ¡sicas
    if (!formData.client_id || isNaN(formData.client_id)) {
        alert('Por favor, selecione um cliente vÃ¡lido.');
        return;
    }
    
    if (!formData.description || !formData.description.trim()) {
        alert('Por favor, informe uma descriÃ§Ã£o.');
        return;
    }
    
    // Desabilitar botÃ£o de salvar
    $('#saveOrderBtn').prop('disabled', true).html('<i class="fas fa-spinner fa-spin me-1"></i>Salvando...');
    
    // Enviar dados via AJAX
    $.ajax({
        url: '/os/' + currentOrderId + '/update-ajax',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(formData),
        success: function(response) {
            console.log('Resposta da atualizaÃ§Ã£o:', response);
            
            if (response.success) {
                // Fechar modal
                $('#editServiceOrderModal').modal('hide');
                
                // Mostrar mensagem de sucesso
                alert(response.message || 'Ordem de serviÃ§o atualizada com sucesso!');
                
                // Recarregar pÃ¡gina para mostrar alteraÃ§Ãµes
                window.location.reload();
            } else {
                alert('Erro: ' + (response.error || 'Erro desconhecido'));
            }
        },
        error: function(xhr, status, error) {
            console.error('Erro ao salvar:', {
                status: xhr.status,
                statusText: xhr.statusText,
                responseText: xhr.responseText,
                error: error
            });
            
            let errorMessage = 'Erro ao salvar alteraÃ§Ãµes.';
            if (xhr.responseJSON && xhr.responseJSON.error) {
                errorMessage = xhr.responseJSON.error;
            }
            
            alert(errorMessage);
        },
        complete: function() {
            // Reabilitar botÃ£o
            $('#saveOrderBtn').prop('disabled', false).html('<i class="fas fa-save me-1"></i>Salvar AlteraÃ§Ãµes');
        }
    });
}

// ============================================
// FunÃ§Ãµes de CÃ¡lculo AutomÃ¡tico do Modal
// ============================================

function calculateModalKmTotal() {
    const kmInicial = $('#create_km_inicial').val();
    const kmFinal = $('#create_km_final').val();
    const kmTotalField = $('#create_km_total');
    
    if (kmInicial && kmFinal) {
        const inicial = parseFloat(kmInicial);
        const final = parseFloat(kmFinal);
        
        if (final > inicial) {
            const total = (final - inicial).toFixed(2);
            kmTotalField.val(total);
            kmTotalField.removeClass('is-invalid').addClass('is-valid');
            calculateModalKmValue();
        } else if (final < inicial) {
            kmTotalField.val('');
            kmTotalField.removeClass('is-valid').addClass('is-invalid');
        } else {
            kmTotalField.val('0.00');
            kmTotalField.removeClass('is-invalid is-valid');
            calculateModalKmValue();
        }
    } else {
        kmTotalField.val('');
        kmTotalField.removeClass('is-invalid is-valid');
        calculateModalKmValue();
    }
}

function calculateModalKmValue() {
    const kmTotal = $('#create_km_total').val();
    const kmRate = $('#create_km_rate').val();
    const kmValueField = $('#create_km_value');
    
    if (kmTotal && kmRate) {
        const total = parseFloat(kmTotal);
        const rate = parseFloat(kmRate);
        const value = (total * rate).toFixed(2);
        kmValueField.val(value);
    } else {
        kmValueField.val('');
    }
    
    calculateModalTotalValue();
}

function calculateModalTotalValue() {
    const kmValue = $('#create_km_value').val();
    const laborValue = $('#create_labor_value').val();
    const partsValue = $('#create_parts_value').val();
    const totalValueField = $('#create_total_value');
    
    let total = 0.0;
    
    if (kmValue) total += parseFloat(kmValue);
    if (laborValue) total += parseFloat(laborValue);
    if (partsValue) total += parseFloat(partsValue);
    
    if (total > 0) {
        totalValueField.val(total.toFixed(2));
    } else {
        totalValueField.val('');
    }
}

// ============================================
// FunÃ§Ãµes de CÃ¡lculo AutomÃ¡tico do Modal de EDIÃ‡ÃƒO
// ============================================

function calculateEditKmTotal() {
    const kmInicial = $('#edit_km_inicial').val();
    const kmFinal = $('#edit_km_final').val();
    const kmTotalField = $('#edit_km_total');
    
    if (kmInicial && kmFinal) {
        const inicial = parseFloat(kmInicial);
        const final = parseFloat(kmFinal);
        
        if (final > inicial) {
            const total = (final - inicial).toFixed(2);
            kmTotalField.val(total);
            calculateEditKmValue();
        } else if (final < inicial) {
            kmTotalField.val('');
        } else {
            kmTotalField.val('0.00');
            calculateEditKmValue();
        }
    } else {
        kmTotalField.val('');
        calculateEditKmValue();
    }
}

function calculateEditKmValue() {
    const kmTotal = $('#edit_km_total').val();
    const kmRate = $('#edit_km_rate').val();
    const kmValueField = $('#edit_km_value');
    
    if (kmTotal && kmRate) {
        const total = parseFloat(kmTotal);
        const rate = parseFloat(kmRate);
        const value = (total * rate).toFixed(2);
        kmValueField.val(value);
    } else {
        kmValueField.val('');
    }
    
    calculateEditTotalValue();
}

function calculateEditTotalValue() {
    const kmValue = $('#edit_km_value').val();
    const laborValue = $('#edit_labor_value').val();
    const partsValue = $('#edit_parts_value').val();
    const totalValueField = $('#edit_total_value');
    
    let total = 0.0;
    
    if (kmValue) total += parseFloat(kmValue);
    if (laborValue) total += parseFloat(laborValue);
    if (partsValue) total += parseFloat(partsValue);
    
    if (total > 0) {
        totalValueField.val(total.toFixed(2));
    } else {
        totalValueField.val('');
    }
}

// ============================================
// FunÃ§Ã£o para abrir modal de criaÃ§Ã£o
// ============================================

function openCreateModal(preselectedClientId = null) {
    console.log('openCreateModal chamado com cliente:', preselectedClientId);
    
    // Verificar se jQuery estÃ¡ disponÃ­vel
    if (typeof $ === 'undefined') {
        console.error('jQuery nÃ£o estÃ¡ carregado');
        return;
    }
    
    // Abrir modal de criaÃ§Ã£o
    const createModal = new bootstrap.Modal(document.getElementById('createServiceOrderModal'));
    createModal.show();
    
    // Resetar conteÃºdo do modal
    $('#createModalBodyContent').html(`
        <div class="text-center py-3">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Carregando...</span>
            </div>
        </div>
    `);
    
    // Buscar dados para criaÃ§Ã£o via AJAX
    console.log('Fazendo requisiÃ§Ã£o AJAX para:', '/os/new-modal');
    $.ajax({
        url: '/os/new-modal',
        method: 'GET',
        dataType: 'json',
        timeout: 10000,
        success: function(data) {
            console.log('Dados recebidos para criaÃ§Ã£o:', data);
            renderCreateModal(data, preselectedClientId);
        },
        error: function(xhr, status, error) {
            console.error('Erro na requisiÃ§Ã£o AJAX:', {
                status: xhr.status,
                statusText: xhr.statusText,
                responseText: xhr.responseText,
                error: error
            });
            $('#createModalBodyContent').html(`
                <div class="alert alert-danger" role="alert">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    <strong>Erro ao carregar formulÃ¡rio de criaÃ§Ã£o:</strong><br>
                    Status: ${xhr.status}<br>
                    Erro: ${error}<br>
                    Resposta: ${xhr.responseText || 'Nenhuma resposta'}
                </div>
            `);
        }
    });
}

// FunÃ§Ã£o para renderizar formulÃ¡rio de criaÃ§Ã£o
function renderCreateModal(data, preselectedClientId = null) {
    console.log('renderCreateModal chamado com dados:', data, 'Cliente prÃ©-selecionado:', preselectedClientId);
    
    if (!data) {
        console.error('Dados nÃ£o fornecidos para criaÃ§Ã£o');
        return;
    }
    
    // Gerar opÃ§Ãµes para clientes
    const clientOptions = data.clients.map(client => 
        `<option value="${client.id}" ${preselectedClientId && client.id == preselectedClientId ? 'selected' : ''}>${client.name}</option>`
    ).join('');
    
    // Gerar opÃ§Ãµes para responsÃ¡veis
    const userOptions = '<option value="0" selected>A ser definido</option>' +
        data.users.map(user => 
            `<option value="${user.id}">${user.name}</option>`
        ).join('');
    
    const createFormContent = `
        <form id="createServiceOrderForm">
            <div class="row">
                <div class="col-md-6">
                    <div class="mb-3">
                        <label for="create_client_id" class="form-label">Cliente *</label>
                        <select class="form-select" id="create_client_id" required onchange="loadClientEquipment(this.value)">
                            <option value="">Selecione um cliente</option>
                            ${clientOptions}
                        </select>
                    </div>
                </div>
                
                <div class="col-md-6">
                    <div class="mb-3">
                        <label for="create_responsible_id" class="form-label">ResponsÃ¡vel</label>
                        <select class="form-select" id="create_responsible_id">
                            ${userOptions}
                        </select>
                    </div>
                </div>
                
                <div class="col-12">
                    <div class="mb-3">
                        <label for="create_description" class="form-label">DescriÃ§Ã£o *</label>
                        <textarea class="form-control" id="create_description" rows="3" required></textarea>
                    </div>
                </div>
                
                <div class="col-12">
                    <div class="mb-3">
                        <label class="form-label">Equipamentos</label>
                        <div class="equipment-checkboxes-create" style="max-height: 200px; overflow-y: auto;">
                            <p class="text-muted">Selecione um cliente para ver os equipamentos disponÃ­veis.</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- SeÃ§Ã£o de Kilometragem -->
            <div class="card mb-3">
                <div class="card-header bg-primary text-white">
                    <h6 class="mb-0"><i class="fas fa-tachometer-alt me-1"></i> Controle de Kilometragem</h6>
                </div>
                <div class="card-body">
                    <div class="row mb-3">
                        <div class="col-md-4">
                            <label for="create_km_inicial" class="form-label">Kilometragem Inicial</label>
                            <input type="number" class="form-control" id="create_km_inicial" step="0.01" 
                                   placeholder="Ex: 12345.50" onchange="calculateModalKmTotal()">
                        </div>
                        <div class="col-md-4">
                            <label for="create_km_final" class="form-label">Kilometragem Final</label>
                            <input type="number" class="form-control" id="create_km_final" step="0.01" 
                                   placeholder="Ex: 12450.75" onchange="calculateModalKmTotal()">
                        </div>
                        <div class="col-md-4">
                            <label for="create_km_total" class="form-label">Total Percorrido (KM)</label>
                            <input type="number" class="form-control bg-light" id="create_km_total" step="0.01" readonly>
                            <small class="form-text text-muted">Calculado automaticamente</small>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-6">
                            <label for="create_km_rate" class="form-label">Valor por KM (R$)</label>
                            <input type="number" class="form-control" id="create_km_rate" step="0.01" 
                                   placeholder="Ex: 2.50" onchange="calculateModalKmValue()">
                        </div>
                        <div class="col-md-6">
                            <label for="create_km_value" class="form-label">Valor Total KM (R$)</label>
                            <input type="number" class="form-control bg-light" id="create_km_value" step="0.01" readonly>
                            <small class="form-text text-muted">Calculado automaticamente</small>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- SeÃ§Ã£o de Valores do ServiÃ§o -->
            <div class="card mb-3">
                <div class="card-header bg-success text-white">
                    <h6 class="mb-0"><i class="fas fa-dollar-sign me-1"></i> Valores do ServiÃ§o</h6>
                </div>
                <div class="card-body">
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label for="create_labor_value" class="form-label">Valor da MÃ£o de Obra (R$)</label>
                            <input type="number" class="form-control" id="create_labor_value" step="0.01" 
                                   placeholder="Ex: 150.00" onchange="calculateModalTotalValue()">
                        </div>
                        <div class="col-md-6">
                            <label for="create_parts_value" class="form-label">Valor das PeÃ§as (R$)</label>
                            <input type="number" class="form-control" id="create_parts_value" step="0.01" 
                                   placeholder="Ex: 200.00" onchange="calculateModalTotalValue()">
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-12">
                            <label for="create_total_value" class="form-label">Valor Total do ServiÃ§o (R$)</label>
                            <input type="number" class="form-control bg-light fw-bold" id="create_total_value" step="0.01" readonly>
                            <small class="form-text text-muted">Calculado automaticamente (KM + MÃ£o de Obra + PeÃ§as)</small>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row">
                <div class="col-md-6">
                    <div class="mb-3">
                        <label for="create_estimated_value" class="form-label">Valor Estimado (R$)</label>
                        <input type="number" class="form-control" id="create_estimated_value" step="0.01" 
                               placeholder="Ex: 500.00">
                    </div>
                </div>
                
                <div class="col-md-6">
                    <div class="mb-3">
                        <label for="create_status" class="form-label">Status</label>
                        <select class="form-select" id="create_status">
                            <option value="aberta" selected>Aberta</option>
                            <option value="em_andamento">Em Andamento</option>
                            <option value="fechada">Fechada</option>
                        </select>
                    </div>
                </div>
            </div>
        </form>
    `;
    
    $('#createModalBodyContent').html(createFormContent);
    
    // Se um cliente estiver prÃ©-selecionado, carregar seus equipamentos
    if (preselectedClientId) {
        setTimeout(function() {
            loadClientEquipment(preselectedClientId);
        }, 100);
    }
}

// FunÃ§Ã£o para carregar equipamentos do cliente selecionado
function loadClientEquipment(clientId) {
    if (!clientId) {
        $('.equipment-checkboxes-create').html('<p class="text-muted">Selecione um cliente para ver os equipamentos disponÃ­veis.</p>');
        return;
    }
    
    $.ajax({
        url: '/api/cliente/' + clientId + '/equipamentos',
        method: 'GET',
        success: function(equipment) {
            if (equipment && equipment.length > 0) {
                const equipmentCheckboxes = equipment.map(eq => `
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" value="${eq.id}" id="create_equipment_${eq.id}">
                        <label class="form-check-label" for="create_equipment_${eq.id}">
                            ${eq.type || 'Equipamento'} - ${eq.brand || ''} ${eq.model || ''}
                        </label>
                    </div>
                `).join('');
                $('.equipment-checkboxes-create').html(equipmentCheckboxes);
            } else {
                $('.equipment-checkboxes-create').html('<p class="text-muted">Nenhum equipamento encontrado para este cliente.</p>');
            }
        },
        error: function() {
            $('.equipment-checkboxes-create').html('<p class="text-danger">Erro ao carregar equipamentos.</p>');
        }
    });
}

// FunÃ§Ã£o para criar nova ordem de serviÃ§o
function createServiceOrder() {
    console.log('createServiceOrder chamado');
    
    // Coletar dados do formulÃ¡rio
    const clientIdValue = $('#create_client_id').val();
    const responsibleIdValue = $('#create_responsible_id').val();
    const descriptionValue = $('#create_description').val();
    const estimatedValue = $('#create_estimated_value').val();
    const kmInicialValue = $('#create_km_inicial').val();
    const kmFinalValue = $('#create_km_final').val();
    const kmRateValue = $('#create_km_rate').val();
    const laborValue = $('#create_labor_value').val();
    const partsValue = $('#create_parts_value').val();
    const statusValue = $('#create_status').val();
    
    console.log('Valores coletados do formulÃ¡rio:', {
        clientIdValue,
        responsibleIdValue,
        descriptionValue,
        estimatedValue,
        kmInicialValue,
        kmFinalValue,
        kmRateValue,
        laborValue,
        partsValue,
        statusValue
    });
    
    const formData = {
        client_id: clientIdValue ? parseInt(clientIdValue) : null,
        responsible_id: responsibleIdValue ? parseInt(responsibleIdValue) : 0,
        description: descriptionValue || '',
        estimated_value: estimatedValue ? parseFloat(estimatedValue) : 0,
        km_inicial: kmInicialValue ? parseFloat(kmInicialValue) : 0,
        km_final: kmFinalValue ? parseFloat(kmFinalValue) : 0,
        km_rate: kmRateValue ? parseFloat(kmRateValue) : 0,
        labor_value: laborValue ? parseFloat(laborValue) : 0,
        parts_value: partsValue ? parseFloat(partsValue) : 0,
        status: statusValue || 'aberta',
        equipment_ids: []
    };
    
    // Coletar equipamentos selecionados
    $('.equipment-checkboxes-create input[type="checkbox"]:checked').each(function() {
        formData.equipment_ids.push(parseInt($(this).val()));
    });
    
    console.log('Dados finais para criar:', formData);
    
    // ValidaÃ§Ãµes bÃ¡sicas
    if (!formData.client_id || isNaN(formData.client_id)) {
        alert('Por favor, selecione um cliente vÃ¡lido.');
        return;
    }
    
    if (!formData.description || !formData.description.trim()) {
        alert('Por favor, informe uma descriÃ§Ã£o.');
        return;
    }
    
    // Desabilitar botÃ£o de criar
    $('#createOrderBtn').prop('disabled', true).html('<i class="fas fa-spinner fa-spin me-1"></i>Criando...');
    
    // Enviar dados via AJAX
    $.ajax({
        url: '/os/create-modal',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(formData),
        success: function(response) {
            console.log('Resposta da criaÃ§Ã£o:', response);
            
            if (response.success) {
                // Fechar modal
                $('#createServiceOrderModal').modal('hide');
                
                // Mostrar mensagem de sucesso
                alert(response.message || 'Ordem de serviÃ§o criada com sucesso!');
                
                // Recarregar pÃ¡gina para mostrar nova OS
                window.location.reload();
            } else {
                alert('Erro: ' + (response.error || 'Erro desconhecido'));
            }
        },
        error: function(xhr, status, error) {
            console.error('Erro ao criar:', {
                status: xhr.status,
                statusText: xhr.statusText,
                responseText: xhr.responseText,
                error: error
            });
            
            let errorMessage = 'Erro ao criar ordem de serviÃ§o.';
            if (xhr.responseJSON && xhr.responseJSON.error) {
                errorMessage = xhr.responseJSON.error;
            }
            
            alert(errorMessage);
        },
        complete: function() {
            // Reabilitar botÃ£o
            $('#createOrderBtn').prop('disabled', false).html('<i class="fas fa-plus me-1"></i>Criar Ordem de ServiÃ§o');
        }
    });
}

// FunÃ§Ã£o para excluir ordem de serviÃ§o
function deleteServiceOrder(orderId) {
    console.log('deleteServiceOrder chamada com ID:', orderId);
    
    if (confirm('Tem certeza que deseja excluir esta ordem de serviÃ§o? Esta aÃ§Ã£o nÃ£o pode ser desfeita!')) {
        // Criar formulÃ¡rio temporÃ¡rio para fazer POST request
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = '/ordens-servico/' + orderId + '/excluir';
        
        console.log('Form action:', form.action);
        
        // Adicionar CSRF token se disponÃ­vel
        const csrfToken = document.querySelector('meta[name="csrf-token"]');
        if (csrfToken) {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'csrf_token';
            input.value = csrfToken.getAttribute('content');
            form.appendChild(input);
            console.log('CSRF token adicionado');
        } else {
            console.warn('CSRF token nÃ£o encontrado');
        }
        
        document.body.appendChild(form);
        console.log('Enviando formulÃ¡rio...');
        form.submit();
    } else {
        console.log('ExclusÃ£o cancelada pelo usuÃ¡rio');
    }
}
