# 🚀 Guia de Instalação: Evolution API para WhatsApp

## O que é Evolution API?
Uma API open-source que permite enviar mensagens, arquivos, áudios e muito mais pelo WhatsApp de forma automatizada.

---

## 📋 Pré-requisitos

1. **Docker Desktop** instalado (Windows/Mac/Linux)
   - Download: https://www.docker.com/products/docker-desktop/

2. **Servidor/VPS** (opcional, mas recomendado para produção)
   - Opções gratuitas: Railway, Render, Fly.io
   - Opções pagas: DigitalOcean (R$ 25/mês), AWS, Azure

---

## 🔧 Opção 1: Instalação Local (Windows - Desenvolvimento)

### Passo 1: Instalar Docker Desktop
```bash
# Baixe e instale o Docker Desktop:
# https://www.docker.com/products/docker-desktop/

# Após instalar, verifique:
docker --version
docker-compose --version
```

### Passo 2: Criar arquivo docker-compose.yml
Crie uma pasta `evolution-api` e dentro dela crie o arquivo `docker-compose.yml`:

```yaml
version: '3.3'

services:
  evolution-api:
    container_name: evolution_api
    image: atendai/evolution-api:latest
    restart: always
    ports:
      - "8080:8080"
    environment:
      # Configurações básicas
      - SERVER_TYPE=http
      - SERVER_PORT=8080
      - SERVER_URL=http://localhost:8080
      
      # Chave de API (TROQUE POR UMA SENHA FORTE!)
      - AUTHENTICATION_API_KEY=SUA_CHAVE_SECRETA_AQUI_TROQUE
      
      # Configurações de instância
      - AUTHENTICATION_EXPOSE_IN_FETCH_INSTANCES=true
      
      # Database (SQLite - para desenvolvimento local)
      - DATABASE_ENABLED=true
      - DATABASE_PROVIDER=sqlite
      - DATABASE_CONNECTION_URI=file:./evolution.db
      
      # Webhook (URL do seu sistema SAMAPE)
      - WEBHOOK_GLOBAL_URL=http://host.docker.internal:5000/webhook/whatsapp
      - WEBHOOK_GLOBAL_ENABLED=true
      - WEBHOOK_GLOBAL_WEBHOOK_BY_EVENTS=false
      
      # Configurações de sessão
      - CONFIG_SESSION_PHONE_CLIENT=Evolution API
      - CONFIG_SESSION_PHONE_NAME=Chrome
      
      # QR Code
      - QRCODE_LIMIT=30
      - QRCODE_COLOR=#198754
      
    volumes:
      - evolution_instances:/evolution/instances
      - evolution_store:/evolution/store

volumes:
  evolution_instances:
  evolution_store:
```

### Passo 3: Subir o servidor
```powershell
# Entre na pasta
cd c:\Users\aless\Desktop\ALESSANDRO\evolution-api

# Suba o container
docker-compose up -d

# Verifique se está rodando
docker ps

# Ver logs (se precisar debugar)
docker logs -f evolution_api
```

### Passo 4: Testar a API
Abra o navegador: http://localhost:8080

Você verá a documentação da API.

---

## ☁️ Opção 2: Deploy na Nuvem (PRODUÇÃO - Railway)

### Por que Railway?
- ✅ Gratuito (500 horas/mês)
- ✅ Fácil de configurar
- ✅ Conecta direto com GitHub
- ✅ Domínio público automático

### Passo 1: Criar conta no Railway
1. Acesse: https://railway.app/
2. Faça login com GitHub

### Passo 2: Deploy da Evolution API
1. Clique em "New Project"
2. Selecione "Deploy from GitHub repo"
3. Escolha: `https://github.com/EvolutionAPI/evolution-api`
4. Ou use o template pronto: https://railway.app/template/evolution-api

### Passo 3: Configurar Variáveis de Ambiente
No Railway, adicione estas variáveis:

```
SERVER_TYPE=https
SERVER_URL=https://seu-app.up.railway.app
AUTHENTICATION_API_KEY=SUA_CHAVE_SECRETA_FORTE
DATABASE_ENABLED=true
DATABASE_PROVIDER=postgresql
DATABASE_CONNECTION_URI=${DATABASE_URL}
WEBHOOK_GLOBAL_URL=https://seu-sistema-samape.railway.app/webhook/whatsapp
WEBHOOK_GLOBAL_ENABLED=true
```

### Passo 4: Adicionar PostgreSQL
1. No Railway, clique em "New" > "Database" > "PostgreSQL"
2. Conecte ao serviço Evolution API
3. A variável `DATABASE_URL` será criada automaticamente

---

## 📱 Conectar WhatsApp (QR Code)

### Via Postman/Insomnia:

#### 1. Criar Instância
```http
POST http://localhost:8080/instance/create
Headers:
  apikey: SUA_CHAVE_SECRETA_AQUI_TROQUE
Body (JSON):
{
  "instanceName": "samape_whatsapp",
  "qrcode": true,
  "integration": "WHATSAPP-BAILEYS"
}
```

#### 2. Pegar QR Code
```http
GET http://localhost:8080/instance/connect/samape_whatsapp
Headers:
  apikey: SUA_CHAVE_SECRETA_AQUI_TROQUE
```

**Resposta:**
```json
{
  "code": "https://...",  // URL do QR Code como imagem
  "base64": "data:image/png;base64,..."  // QR Code em base64
}
```

#### 3. Escanear QR Code
- Abra WhatsApp no celular
- Vá em "Aparelhos conectados"
- Clique em "Conectar um aparelho"
- Escaneie o QR Code retornado

---

## 📤 Enviar PDF pelo WhatsApp

### Exemplo de Request:

```http
POST http://localhost:8080/message/sendMedia/samape_whatsapp
Headers:
  apikey: SUA_CHAVE_SECRETA_AQUI_TROQUE
Body (JSON):
{
  "number": "5511987654321",
  "mediatype": "document",
  "mimetype": "application/pdf",
  "caption": "📋 Ordem de Serviço #123 - Cliente: João Silva",
  "media": "https://seu-sistema.com/os/123/pdf",
  "fileName": "OS_123_Joao_Silva.pdf"
}
```

**OU enviar base64:**
```json
{
  "number": "5511987654321",
  "mediatype": "document",
  "mimetype": "application/pdf",
  "caption": "📋 Ordem de Serviço #123",
  "media": "data:application/pdf;base64,JVBERi0xLjQKJcfsj6IKNSAwIG9iago8PC...",
  "fileName": "OS_123.pdf"
}
```

---

## 🔗 Integrar com SAMAPE (Flask)

### 1. Adicionar variáveis de ambiente no `.env`:
```env
EVOLUTION_API_URL=http://localhost:8080
EVOLUTION_API_KEY=SUA_CHAVE_SECRETA_AQUI_TROQUE
EVOLUTION_INSTANCE_NAME=samape_whatsapp
```

### 2. Criar helper para Evolution API (`evolution_api.py`):
```python
import requests
import os
from flask import current_app

class EvolutionAPI:
    def __init__(self):
        self.base_url = os.getenv('EVOLUTION_API_URL', 'http://localhost:8080')
        self.api_key = os.getenv('EVOLUTION_API_KEY')
        self.instance = os.getenv('EVOLUTION_INSTANCE_NAME', 'samape_whatsapp')
    
    def send_pdf(self, phone_number, pdf_url, caption, filename):
        """
        Envia PDF via WhatsApp
        
        Args:
            phone_number: Número com DDI (ex: 5511987654321)
            pdf_url: URL pública do PDF
            caption: Texto da mensagem
            filename: Nome do arquivo
        """
        url = f"{self.base_url}/message/sendMedia/{self.instance}"
        
        headers = {
            'apikey': self.api_key,
            'Content-Type': 'application/json'
        }
        
        payload = {
            "number": phone_number,
            "mediatype": "document",
            "mimetype": "application/pdf",
            "caption": caption,
            "media": pdf_url,
            "fileName": filename
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Erro ao enviar PDF via WhatsApp: {e}")
            raise

evolution_api = EvolutionAPI()
```

### 3. Criar rota no `routes.py`:
```python
from evolution_api import evolution_api

@app.route('/os/<int:id>/send-whatsapp', methods=['POST'])
@login_required
def send_order_whatsapp(id):
    """Envia OS via WhatsApp automaticamente"""
    order = ServiceOrder.query.get_or_404(id)
    
    # Valida telefone
    if not order.client or not order.client.phone:
        flash('Cliente não possui telefone cadastrado', 'error')
        return redirect(url_for('view_service_order', id=id))
    
    # Limpa e formata telefone
    phone = re.sub(r'\D', '', order.client.phone)
    if not phone.startswith('55'):
        phone = '55' + phone
    
    # URL pública do PDF (precisa ser acessível externamente)
    pdf_url = url_for('export_service_order_pdf', id=order.id, _external=True)
    
    # Monta mensagem
    caption = f"""📋 *Ordem de Serviço #{order.id}*
👤 Cliente: {order.client.name}
📝 {order.description or order.service_details or 'Serviço realizado'}

✅ SAMAPE - Sistema de Gerenciamento"""
    
    filename = f"OS_{order.id}_{order.client.name.replace(' ', '_')}.pdf"
    
    try:
        # Envia via Evolution API
        result = evolution_api.send_pdf(phone, pdf_url, caption, filename)
        
        flash(f'✅ PDF enviado com sucesso para {order.client.name}!', 'success')
        
        # Registra no log
        log = ActionLog(
            user_id=current_user.id,
            action='envio_os_whatsapp',
            entity_type='service_order',
            entity_id=order.id,
            details=f'PDF enviado via WhatsApp para {phone}'
        )
        db.session.add(log)
        db.session.commit()
        
    except Exception as e:
        flash(f'Erro ao enviar WhatsApp: {str(e)}', 'error')
    
    return redirect(url_for('view_service_order', id=id))
```

---

## 🔐 Segurança IMPORTANTE

### 1. Proteja a API Key
```python
# NUNCA coloque a chave no código!
# Use variáveis de ambiente:
API_KEY = os.getenv('EVOLUTION_API_KEY')
```

### 2. Configure CORS (se necessário)
No Evolution API, adicione:
```
CORS_ORIGIN=https://seu-dominio.com
CORS_METHODS=GET,POST,PUT,DELETE
CORS_CREDENTIALS=true
```

### 3. Use HTTPS em produção
```
SERVER_TYPE=https
SERVER_URL=https://seu-dominio.com
```

---

## 📊 Monitoramento

### Ver instâncias conectadas:
```http
GET http://localhost:8080/instance/fetchInstances
Headers:
  apikey: SUA_CHAVE_SECRETA
```

### Ver status de conexão:
```http
GET http://localhost:8080/instance/connectionState/samape_whatsapp
Headers:
  apikey: SUA_CHAVE_SECRETA
```

### Desconectar (logout):
```http
DELETE http://localhost:8080/instance/logout/samape_whatsapp
Headers:
  apikey: SUA_CHAVE_SECRETA
```

---

## 🆘 Troubleshooting

### Container não inicia:
```powershell
docker logs evolution_api
```

### Erro de conexão com banco:
Verifique se o PostgreSQL está rodando:
```powershell
docker ps | grep postgres
```

### QR Code expira rapidamente:
Aumente o timeout:
```yaml
- QRCODE_LIMIT=60  # 60 segundos
```

### WhatsApp desconecta sozinho:
Configure keep-alive:
```yaml
- WEBSOCKET_ENABLED=true
- WEBSOCKET_AUTO_RECONNECT=true
```

---

## 📚 Documentação Oficial

- **Evolution API**: https://doc.evolution-api.com/
- **GitHub**: https://github.com/EvolutionAPI/evolution-api
- **Postman Collection**: https://www.postman.com/evolutionapi

---

## 💰 Custos Estimados

| Opção | Custo | Uso |
|-------|-------|-----|
| **Local (Docker)** | R$ 0 | Desenvolvimento |
| **Railway Free** | R$ 0 | Até 500h/mês |
| **Railway Pro** | R$ 25/mês | Ilimitado |
| **DigitalOcean VPS** | R$ 25/mês | Controle total |
| **AWS/Azure** | R$ 50-100/mês | Produção grande |

---

## ✅ Próximos Passos

1. ☐ Instalar Docker Desktop
2. ☐ Criar `docker-compose.yml`
3. ☐ Subir container local
4. ☐ Testar conexão (http://localhost:8080)
5. ☐ Criar instância via Postman
6. ☐ Escanear QR Code no celular
7. ☐ Testar envio de mensagem
8. ☐ Integrar com SAMAPE (Flask)
9. ☐ Deploy no Railway (produção)

---

**Quer que eu ajude a implementar alguma dessas etapas?** 🚀
