/**
 * Funções JavaScript comuns para modals de Ordem de Serviço
 * Este arquivo deve ser incluído em todas as páginas que precisam dos modals de OS
 */

let currentOrderId = null;

// Função de teste para verificar se tudo está funcionando
function testServiceOrderModals() {
    console.log('=== TESTE DE DIAGNÓSTICO DOS MODALS ===');
    console.log('jQuery carregado:', typeof $ !== 'undefined');
    console.log('Bootstrap carregado:', typeof bootstrap !== 'undefined');
    console.log('Modal de visualização existe:', !!document.getElementById('viewServiceOrderModal'));
    console.log('Modal de edição existe:', !!document.getElementById('editServiceOrderModal'));
    console.log('Current Order ID:', currentOrderId);
    
    if (typeof $ !== 'undefined') {
        console.log('Versão do jQuery:', $.fn.jquery);
    }
    
    return {
        jquery: typeof $ !== 'undefined',
        bootstrap: typeof bootstrap !== 'undefined',
        viewModal: !!document.getElementById('viewServiceOrderModal'),
        editModal: !!document.getElementById('editServiceOrderModal'),
        currentOrderId: currentOrderId
    };
}

// Aguardar o carregamento do jQuery antes de executar
function initializeServiceOrderModals() {
    if (typeof $ === 'undefined') {
        setTimeout(initializeServiceOrderModals, 100);
        return;
    }
    
    console.log('Service Order Modals inicializados');
}

// Inicializar quando o DOM estiver pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeServiceOrderModals);
} else {
    initializeServiceOrderModals();
}

// Função para visualizar ordem de serviço em modal
function viewServiceOrder(orderId) {
    console.log('viewServiceOrder chamado com ID:', orderId);
    
    if (typeof $ === 'undefined') {
        console.error('jQuery não está carregado');
        return;
    }
    
    currentOrderId = orderId;
    
    const modal = new bootstrap.Modal(document.getElementById('viewServiceOrderModal'));
    modal.show();
    
    $('#modalBodyContent').html(`
        <div class="text-center py-3">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Carregando...</span>
            </div>
        </div>
    `);
    
    $.ajax({
        url: '/os/' + orderId + '/modal',
        method: 'GET',
        dataType: 'json',
        timeout: 10000,
        success: function(data) {
            renderOrderModal(data);
            $('#editOrderBtn').show();
            $('#fullViewBtn').attr('href', '/os/' + orderId).show();
        },
        error: function(xhr, status, error) {
            $('#modalBodyContent').html(`
                <div class="alert alert-danger" role="alert">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    <strong>Erro ao carregar a ordem de serviço:</strong><br>
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

// Função para renderizar os dados da OS no modal
function renderOrderModal(order) {
    console.log('renderOrderModal chamado com dados:', order);
    
    if (!order) {
        console.error('Dados da ordem não fornecidos');
        return;
    }
    
    const statusClass = {
        'aberta': 'warning',
        'em_andamento': 'info', 
        'fechada': 'success'
    }[order.status] || 'secondary';
    
    const modalContent = `
        <div class="row">
            <!-- Informações Básicas -->
            <div class="col-md-6">
                <div class="card mb-3">
                    <div class="card-header">
                        <h6 class="mb-0"><i class="fas fa-info-circle me-2"></i>Informações Básicas</h6>
                    </div>
                    <div class="card-body">
                        <p><strong>OS #:</strong> ${order.id}</p>
                        <p><strong>Status:</strong> <span class="badge bg-${statusClass}">${order.status_label}</span></p>
                        <p><strong>Criada em:</strong> ${order.created_at}</p>
                        <p><strong>Atualizada em:</strong> ${order.updated_at}</p>
                        <p><strong>Responsável:</strong> ${order.responsible.name}</p>
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
                                <p><strong>Nº Série:</strong> ${equipment.serial_number}</p>
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
                        <p><strong>Valor Estimado:</strong> ${order.estimated_value}</p>
                        <p><strong>Valor da Nota:</strong> ${order.invoice_amount}</p>
                        <p><strong>KM Inicial:</strong> ${order.km_inicial}</p>
                        <p><strong>KM Final:</strong> ${order.km_final}</p>
                        ${order.km_total && order.km_total !== 'N/A' ? 
                            `<p><strong>KM Total:</strong> ${order.km_total}</p>` : ''
                        }
                    </div>
                </div>
            </div>
            
            <!-- Descrição do Serviço -->
            <div class="col-12">
                <div class="card mb-3">
                    <div class="card-header">
                        <h6 class="mb-0"><i class="fas fa-clipboard-list me-2"></i>Descrição do Serviço</h6>
                    </div>
                    <div class="card-body">
                        <p class="mb-0">${order.description || 'Nenhuma descrição informada'}</p>
                    </div>
                </div>
            </div>
            
            <!-- Detalhes do Serviço -->
            ${order.service_details && order.service_details !== 'Nenhum detalhe informado' ? `
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h6 class="mb-0"><i class="fas fa-sticky-note me-2"></i>Detalhes do Serviço</h6>
                    </div>
                    <div class="card-body">
                        <p class="mb-0">${order.service_details}</p>
                    </div>
                </div>
            </div>
            ` : ''}
            
            <!-- Informações da Nota Fiscal -->
            ${order.invoice_number && order.invoice_number !== 'Não informado' ? `
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h6 class="mb-0"><i class="fas fa-file-invoice me-2"></i>Nota Fiscal</h6>
                    </div>
                    <div class="card-body">
                        <p class="mb-0"><strong>Número da Nota:</strong> ${order.invoice_number}</p>
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

// Função para editar a OS atual
function editCurrentOrder() {
    if (currentOrderId) {
        openEditModal(currentOrderId);
    }
}

// Função para abrir modal de edição
function openEditModal(orderId) {
    console.log('openEditModal chamado com ID:', orderId);
    
    if (typeof $ === 'undefined') {
        console.error('jQuery não está carregado');
        return;
    }
    
    if (typeof bootstrap === 'undefined') {
        console.error('Bootstrap não está carregado');
        return;
    }
    
    if (!document.getElementById('editServiceOrderModal')) {
        console.error('Modal de edição não encontrado no DOM');
        return;
    }
    
    currentOrderId = orderId;
    
    // Fechar modal de visualização se estiver aberto
    $('#viewServiceOrderModal').modal('hide');
    
    // Abrir modal de edição
    const editModal = new bootstrap.Modal(document.getElementById('editServiceOrderModal'));
    editModal.show();
    
    // Resetar conteúdo do modal
    $('#editModalBodyContent').html(`
        <div class="text-center py-3">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Carregando...</span>
            </div>
        </div>
    `);
    
    // Buscar dados da OS para edição via AJAX
    console.log('Fazendo requisição AJAX para:', '/os/' + orderId + '/edit-modal');
    $.ajax({
        url: '/os/' + orderId + '/edit-modal',
        method: 'GET',
        dataType: 'json',
        timeout: 10000,
        success: function(data) {
            console.log('Dados recebidos para edição:', data);
            renderEditModal(data);
        },
        error: function(xhr, status, error) {
            console.error('Erro na requisição AJAX:', {
                status: xhr.status,
                statusText: xhr.statusText,
                responseText: xhr.responseText,
                error: error
            });
            $('#editModalBodyContent').html(`
                <div class="alert alert-danger" role="alert">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    <strong>Erro ao carregar formulário de edição:</strong><br>
                    Status: ${xhr.status}<br>
                    Erro: ${error}<br>
                    Resposta: ${xhr.responseText || 'Nenhuma resposta'}
                </div>
            `);
        }
    });
}

// Função para renderizar formulário de edição
function renderEditModal(data) {
    console.log('renderEditModal chamado com dados:', data);
    
    if (!data) {
        console.error('Dados da ordem não fornecidos para edição');
        return;
    }
    
    // Gerar opções para clientes
    const clientOptions = data.clients.map(client => 
        `<option value="${client.id}" ${client.id === data.client_id ? 'selected' : ''}>${client.name}</option>`
    ).join('');
    
    // Gerar opções para responsáveis
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
                        <label for="edit_responsible_id" class="form-label">Responsável</label>
                        <select class="form-select" id="edit_responsible_id">
                            ${userOptions}
                        </select>
                    </div>
                </div>
                
                <div class="col-12">
                    <div class="mb-3">
                        <label for="edit_description" class="form-label">Descrição *</label>
                        <textarea class="form-control" id="edit_description" rows="3" required>${data.description}</textarea>
                    </div>
                </div>
                
                <div class="col-md-4">
                    <div class="mb-3">
                        <label for="edit_estimated_value" class="form-label">Valor Estimado</label>
                        <input type="number" class="form-control" id="edit_estimated_value" step="0.01" value="${data.estimated_value}">
                    </div>
                </div>
                
                <div class="col-md-4">
                    <div class="mb-3">
                        <label for="edit_km_inicial" class="form-label">KM Inicial</label>
                        <input type="number" class="form-control" id="edit_km_inicial" step="0.01" value="${data.km_inicial}">
                    </div>
                </div>
                
                <div class="col-md-4">
                    <div class="mb-3">
                        <label for="edit_km_final" class="form-label">KM Final</label>
                        <input type="number" class="form-control" id="edit_km_final" step="0.01" value="${data.km_final}">
                    </div>
                </div>
                
                <div class="col-md-6">
                    <div class="mb-3">
                        <label for="edit_status" class="form-label">Status</label>
                        <select class="form-select" id="edit_status">
                            <option value="aberta" ${data.status === 'aberta' ? 'selected' : ''}>Aberta</option>
                            <option value="em_andamento" ${data.status === 'em_andamento' ? 'selected' : ''}>Em Andamento</option>
                            <option value="fechada" ${data.status === 'fechada' ? 'selected' : ''}>Fechada</option>
                        </select>
                    </div>
                </div>
                
                <div class="col-12">
                    <div class="mb-3">
                        <label for="edit_service_details" class="form-label">Detalhes do Serviço</label>
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

// Função para salvar alterações da OS
function saveServiceOrder() {
    console.log('saveServiceOrder chamado');
    
    if (!currentOrderId) {
        console.error('ID da ordem não definido');
        alert('Erro: ID da ordem não foi definido. Tente abrir a edição novamente.');
        return;
    }
    
    // Verificar se os elementos do formulário existem
    if (!$('#edit_client_id').length) {
        console.error('Formulário de edição não encontrado');
        alert('Erro: Formulário de edição não foi carregado corretamente. Tente novamente.');
        return;
    }
    
    // Coletar dados do formulário
    const clientIdValue = $('#edit_client_id').val();
    const responsibleIdValue = $('#edit_responsible_id').val();
    const descriptionValue = $('#edit_description').val();
    const estimatedValue = $('#edit_estimated_value').val();
    const kmInicialValue = $('#edit_km_inicial').val();
    const kmFinalValue = $('#edit_km_final').val();
    const statusValue = $('#edit_status').val();
    const serviceDetailsValue = $('#edit_service_details').val();
    
    console.log('Valores coletados do formulário:', {
        clientIdValue,
        responsibleIdValue,
        descriptionValue,
        estimatedValue,
        kmInicialValue,
        kmFinalValue,
        statusValue,
        serviceDetailsValue
    });
    
    const formData = {
        client_id: clientIdValue ? parseInt(clientIdValue) : null,
        responsible_id: responsibleIdValue ? parseInt(responsibleIdValue) : 0,
        description: descriptionValue || '',
        estimated_value: estimatedValue ? parseFloat(estimatedValue) : null,
        km_inicial: kmInicialValue ? parseFloat(kmInicialValue) : null,
        km_final: kmFinalValue ? parseFloat(kmFinalValue) : null,
        status: statusValue || 'aberta',
        service_details: serviceDetailsValue || '',
        equipment_ids: []
    };
    
    // Coletar equipamentos selecionados
    $('.equipment-checkboxes input[type="checkbox"]:checked').each(function() {
        formData.equipment_ids.push(parseInt($(this).val()));
    });
    
    console.log('Dados finais para salvar:', formData);
    
    // Validações básicas
    if (!formData.client_id || isNaN(formData.client_id)) {
        alert('Por favor, selecione um cliente válido.');
        return;
    }
    
    if (!formData.description || !formData.description.trim()) {
        alert('Por favor, informe uma descrição.');
        return;
    }
    
    // Desabilitar botão de salvar
    $('#saveOrderBtn').prop('disabled', true).html('<i class="fas fa-spinner fa-spin me-1"></i>Salvando...');
    
    // Enviar dados via AJAX
    console.log('Enviando dados via AJAX para:', '/os/' + currentOrderId + '/update-ajax');
    
    // Log dos dados finais
    console.log('FormData sendo enviado:', JSON.stringify(formData, null, 2));
    
    // CSRF DESABILITADO - Dados simples JSON
    console.log('CSRF desabilitado - enviando dados simples');
    
    const requestData = JSON.stringify(formData);
    const requestHeaders = {
        'Content-Type': 'application/json'
    };
    
    console.log('Dados sendo enviados:', formData);
    console.log('Headers:', requestHeaders);
    console.log('JSON string:', requestData);
    
    console.log('Request headers:', requestHeaders);
    console.log('Request data type:', requestData.constructor.name);
    if (requestData.constructor.name === 'String') {
        console.log('Request data (JSON):', requestData);
    } else {
        console.log('Request data (FormData):', 'FormData object created');
        // Log dos dados do FormData
        for (let pair of requestData.entries()) {
            console.log('FormData entry:', pair[0] + ' = ' + pair[1]);
        }
    }
    
    // Verificar conectividade
    console.log('Verificando conectividade...');
    console.log('URL de destino:', '/os/' + currentOrderId + '/update-ajax');
    console.log('Método:', 'POST');
    console.log('Navegador online:', navigator.onLine);
    
    // Configuração AJAX simplificada
    const ajaxConfig = {
        url: '/os/' + currentOrderId + '/update-ajax',
        method: 'POST',
        data: requestData,
        headers: requestHeaders,
        contentType: 'application/json',
        timeout: 30000, // 30 segundos
        beforeSend: function(xhr) {
            console.log('Enviando requisição AJAX...');
            console.log('URL:', '/os/' + currentOrderId + '/update-ajax');
            console.log('Headers sendo enviados:', requestHeaders);
            console.log('Data sendo enviada:', requestData);
            console.log('XHR readyState:', xhr.readyState);
        },
    };
    
    console.log('Configuração AJAX final:', ajaxConfig);
    
    // Adicionar handlers de sucesso e erro à configuração
    ajaxConfig.success = function(response) {
        console.log('Resposta da atualização:', response);
        
        if (response.success) {
            // Fechar modal
            $('#editServiceOrderModal').modal('hide');
            
            // Mostrar mensagem de sucesso
            alert(response.message || 'Ordem de serviço atualizada com sucesso!');
            
            // Recarregar página para mostrar alterações
            window.location.reload();
        } else {
            console.error('Erro na resposta:', response);
            alert('Erro: ' + (response.error || 'Erro desconhecido'));
        }
    };
    
    ajaxConfig.error = function(xhr, status, error) {
            console.error('=== ERRO AJAX DETALHADO ===');
            console.error('Status:', xhr.status);
            console.error('Status Text:', xhr.statusText);
            console.error('Ready State:', xhr.readyState);
            console.error('Error:', error);
            console.error('Response Text RAW:', xhr.responseText);
            console.error('Response Headers:', xhr.getAllResponseHeaders());
            
            // Tentar obter mais detalhes da resposta
            if (xhr.responseText) {
                console.error('Tamanho da resposta:', xhr.responseText.length);
                console.error('Primeiros 500 chars:', xhr.responseText.substring(0, 500));
                
                try {
                    const errorResponse = JSON.parse(xhr.responseText);
                    console.error('Response JSON parsed:', errorResponse);
                } catch (e) {
                    console.error('Response não é JSON válido:', e.message);
                }
            } else {
                console.error('Response Text está vazio!');
            }
            
            let errorMessage = 'Erro ao salvar alterações.';
            
            if (xhr.status === 0) {
                errorMessage = 'Erro de conexão. Verifique sua internet.';
            } else if (xhr.status === 400) {
                errorMessage = 'Dados inválidos enviados.';
            } else if (xhr.status === 403) {
                errorMessage = 'Acesso negado. Faça login novamente.';
            } else if (xhr.status === 404) {
                errorMessage = 'Ordem de serviço não encontrada.';
            } else if (xhr.status === 500) {
                errorMessage = 'Erro interno do servidor.';
            }
            
            if (xhr.responseJSON && xhr.responseJSON.error) {
                errorMessage = xhr.responseJSON.error;
            } else if (xhr.responseText) {
                try {
                    const response = JSON.parse(xhr.responseText);
                    if (response.error) {
                        errorMessage = response.error;
                    }
                } catch (e) {
                    console.error('Erro ao parsear resposta:', e);
                }
            }
            
            // Mostrar erro detalhado para debug
            console.error('=== ERRO COMPLETO ===');
            console.error('Status:', xhr.status);
            console.error('Status Text:', xhr.statusText);
            console.error('Response Text:', xhr.responseText);
            console.error('Ready State:', xhr.readyState);
            console.error('Response Headers:', xhr.getAllResponseHeaders());
            
            alert('ERRO: ' + errorMessage + '\n\nVerifique o console para mais detalhes (F12)');
    };
    
    ajaxConfig.complete = function() {
        // Reabilitar botão
        $('#saveOrderBtn').prop('disabled', false).html('<i class="fas fa-save me-1"></i>Salvar Alterações');
    };
    
    // Executar a requisição AJAX
    $.ajax(ajaxConfig);
}