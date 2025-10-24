// Teste simples de CSRF e FormData
function testCSRF() {
    console.log('=== TESTE CSRF ===');
    
    // Verificar se conseguimos obter o token
    const csrfToken1 = $('meta[name=csrf-token]').attr('content');
    const csrfToken2 = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
    
    console.log('CSRF Token (jQuery):', csrfToken1);
    console.log('CSRF Token (Vanilla):', csrfToken2);
    
    // Testar criação de FormData
    const testData = {
        client_id: 1,
        description: 'teste',
        status: 'aberta'
    };
    
    console.log('Dados de teste:', testData);
    
    // Criar FormData
    const formData = new FormData();
    if (csrfToken1) {
        formData.append('csrf_token', csrfToken1);
    }
    
    for (const [key, value] of Object.entries(testData)) {
        formData.append(key, value);
    }
    
    console.log('FormData criado:');
    for (let pair of formData.entries()) {
        console.log('  ' + pair[0] + ': ' + pair[1]);
    }
    
    // Teste básico de conectividade
    console.log('Navigator online:', navigator.onLine);
    console.log('Base URL:', window.location.origin);
    
    return {
        csrfToken: csrfToken1,
        formData: formData,
        testData: testData
    };
}

// Executar teste automaticamente
$(document).ready(function() {
    console.log('Executando teste CSRF...');
    testCSRF();
});