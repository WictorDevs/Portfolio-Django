# Portfolio Django + Microserviço de Notificações

Projeto acadêmico composto por dois sistemas independentes:

- **Portfolio** (porta 8000) — sistema principal com perfil, projetos e certificados
- **Notificação MS** (porta 8001) — microserviço de notificações consumido pelo portfolio

---

## Pré-requisitos

- Python 3.10 ou superior instalado
- Git instalado
- Dois terminais abertos ao mesmo tempo

---

## Passo 1 — Clonar os repositórios

Abra o terminal e escolha uma pasta para os projetos:

```bash
cd ~/Projetos   # ou qualquer pasta de sua preferência
```

Clone os dois repositórios:

```bash
git clone https://github.com/WictorDevs/Portfolio-Django.git
git clone https://github.com/WictorDevs/Notification.git
```

---

## Passo 2 — Configurar o Microserviço de Notificações

### 2.1 Criar e ativar o ambiente virtual

```bash
cd Notification
python -m venv venv
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 2.2 Instalar dependências

```bash
pip install django djangorestframework django-cors-headers requests
```

### 2.3 Aplicar migrações

```bash
python manage.py migrate
```

### 2.4 Criar superusuário

```bash
python manage.py createsuperuser
```

Preencha username, email e senha quando solicitado.

### 2.5 Iniciar o servidor na porta 8001

```bash
python manage.py runserver 8001
```

### 2.6 Cadastrar a Empresa no Admin

Acesse `http://127.0.0.1:8001/admin/` e faça login com o superusuário criado.

- Clique em **Empresas → Adicionar**
- Nome: `Portfolio UAST`
- Salve — o hash será gerado automaticamente
- **Anote o hash gerado** (ex: `cad4eb183b567f6b`) — você vai precisar dele no próximo passo

---

## Passo 3 — Configurar o Portfolio

Abra um **segundo terminal** e volte para a pasta dos projetos:

```bash
cd ~/Projetos   # ou qualquer pasta de sua preferência
```

### 3.1 Criar e ativar o ambiente virtual

```bash
cd Portfolio-Django
python -m venv venv
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 3.2 Instalar dependências

```bash
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers
```

### 3.3 Configurar a API Key do microserviço

Abra o arquivo `mysite/settings.py` e atualize a linha 146:

```python
NOTIFICACAO_MS_API_KEY = 'cole_aqui_o_hash_da_empresa'
```

Substitua `cole_aqui_o_hash_da_empresa` pelo hash anotado no passo 2.6.

### 3.4 Aplicar migrações

```bash
python manage.py migrate
```

### 3.5 Criar superusuário

```bash
python manage.py createsuperuser
```

### 3.6 Iniciar o servidor na porta 8000

```bash
python manage.py runserver
```

---

## Passo 4 — Popular o banco do Portfolio

Acesse `http://127.0.0.1:8000/admin/` e faça login.

- Clique em **Perfis Pessoais → Adicionar** e preencha seus dados


---

## Passo 5 — Testar o sistema

### 5.1 Acessar o portfolio

Acesse `http://127.0.0.1:8000/portfolio/` — você deve ver o portfolio com seus dados.

### 5.2 Verificar o sino de notificações

O sino no canto superior direito deve aparecer com:
- 🔘 **X cinza** — sem conexão com o microserviço
- 🟢 **0 verde** — conectado, sem notificações
- 🔴 **N vermelho** — N notificações não lidas

### 5.3 Configurar e rodar o script de envio

Abra o arquivo `enviar_notificacao.py` na raiz do projeto `Notification` e atualize a linha 6:

```python
API_KEY = 'cole_aqui_o_hash_da_empresa'
```

Substitua pelo mesmo hash anotado no passo 2.6.

Abra um **novo terminal**, entre na pasta do microserviço e ative o venv:

**Linux/Mac:**
```bash
cd Notification
source venv/bin/activate
```

**Windows:**
```bash
cd Notification
venv\Scripts\activate
```

Rode o script:

```bash
python enviar_notificacao.py
```

Saída esperada:
```
✓ Notificacao enviada: Matricula
✓ Notificacao enviada: Notas
✓ Notificacao enviada: Agenda
```


### 5.4 Testar o dropdown

- Clique no sino para ver a lista de notificações
- Clique em uma notificação não lida para marcá-la como lida
- Clique em **Marcar todas como lidas** para limpar todas de uma vez

### 5.5 Testar o isolamento entre empresas (opcional)

No admin do microserviço (`http://127.0.0.1:8001/admin/`), crie uma segunda empresa (ex: "Sistema RH") e anote o hash dela. Use o script abaixo para enviar notificações por ela:

**Linux/Mac:**
```bash
curl -X POST http://127.0.0.1:8001/api/notificacoes/criar/ \
     -H "X-Api-Key: HASH_SISTEMA_RH" \
     -H "Content-Type: application/json" \
     -d '{"user_id": 1, "mensagem": "Notificacao do RH", "titulo": "RH"}'
```

**Windows (PowerShell):**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8001/api/notificacoes/criar/" `
  -Method POST `
  -Headers @{ "X-Api-Key" = "HASH_SISTEMA_RH"; "Content-Type" = "application/json" } `
  -Body '{"user_id": 1, "mensagem": "Notificacao do RH", "titulo": "RH"}'
```

Liste as notificações com o hash do RH — só as notificações dessa empresa aparecerão, comprovando o isolamento.



---

## Endpoints do Microserviço

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/notificacoes/` | Lista notificações do usuário |
| GET | `/api/notificacoes/nao-lidas/` | Conta notificações não lidas |
| PATCH | `/api/notificacoes/<id>/lida/` | Marca uma notificação como lida |
| PATCH | `/api/notificacoes/marcar-todas-lidas/` | Marca todas como lidas |
| POST | `/api/notificacoes/criar/` | Cria uma notificação |

Todos os endpoints exigem o header `X-Api-Key`. Os endpoints de leitura também exigem `X-User-Id`.

---

## Observações

- Os dois servidores precisam estar rodando ao mesmo tempo
- O `db.sqlite3` não é versionado no Git — cada clone começa com banco vazio
- O hash da empresa no microserviço deve ser o mesmo configurado em `NOTIFICACAO_MS_API_KEY` no portfolio
