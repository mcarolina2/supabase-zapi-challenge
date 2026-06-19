# supabase-zapi-challenge— Envio de Mensagens Personalizadas (Supabase + Z-API)

Script Python que lê contatos cadastrados no Supabase e envia, via Z-API, a mensagem
personalizada `"Olá, <nome_contato> tudo bem com você?"` para até 3 números.

## Stack

- Python 3.10+
- [Supabase](https://supabase.com) (Postgres + API, plano gratuito) — fonte dos contatos
- [Z-API](https://www.z-api.io) (plano gratuito) — envio de mensagens via WhatsApp

## Estrutura do projeto

```
.
├── main.py                  # ponto de entrada
├── src/
│   ├── config.py            # leitura de variáveis de ambiente e logging
│   ├── supabase_client.py   # consulta de contatos no Supabase
│   └── zapi_client.py       # envio de mensagens via Z-API
├── sql/
│   └── create_table.sql     # script de criação da tabela "contacts"
├── requirements.txt
├── .env.example
└── .gitignore
```

## 1. Setup da tabela no Supabase

1. Crie um projeto gratuito em [supabase.com](https://supabase.com).
2. No **SQL Editor**, rode o script `sql/create_table.sql`. Ele cria a tabela:

   | coluna       | tipo        | descrição                          |
   |--------------|-------------|-------------------------------------|
   | id           | bigint      | identificador, gerado automaticamente |
   | nome         | text        | nome do contato (usado em `<nome_contato>`) |
   | telefone     | text        | número no formato DDI+DDD+número, ex.: `5583999999999` |
   | created_at   | timestamptz | data de criação                     |

3. O script já insere 3 contatos de exemplo — **substitua os números pelos seus** (ou de pessoas que possam receber o teste) antes de rodar o envio real.
4. Em **Project Settings > API**, copie a **Project URL** e a **anon key** (ou service_role, se preferir) para o `.env`.

## 2. Setup da Z-API

1. Crie uma conta gratuita em [z-api.io](https://www.z-api.io) e crie uma instância.
2. Conecte seu WhatsApp lendo o QR Code exibido no painel da instância.
3. Copie o **ID da instância** e o **Token** da instância.
4. Em **Segurança > Token de Segurança da Conta**, gere e copie o **Client-Token**.

## 3. Variáveis de ambiente

Copie `.env.example` para `.env` e preencha:

```env
SUPABASE_URL=https://xxxxxxxxxxxx.supabase.co
SUPABASE_KEY=sua_chave_aqui
SUPABASE_TABLE=contacts

ZAPI_INSTANCE_ID=id_da_instancia
ZAPI_TOKEN=token_da_instancia
ZAPI_CLIENT_TOKEN=token_de_seguranca_da_conta

MAX_CONTACTS=3
```

## 4. Instalação e execução

```bash
# (opcional) crie um ambiente virtual
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# instale as dependências
pip install -r requirements.txt

# rode o script
python main.py
```

## Como funciona

1. `src/config.py` carrega e valida as variáveis de ambiente.
2. `src/supabase_client.py` busca até `MAX_CONTACTS` contatos válidos (com `nome` e `telefone` preenchidos) na tabela configurada.
3. `main.py` monta a mensagem `"Olá, <nome> tudo bem com você?"` para cada contato.
4. `src/zapi_client.py` normaliza o telefone (remove máscara/formatação) e envia via `POST /send-text` da Z-API.
5. Erros de configuração, de consulta ao banco ou de envio são logados (console + `app.log`) sem interromper o envio para os demais contatos; ao final, é exibido um resumo de sucessos e falhas.

## Logs e tratamento de erros

- Logs estruturados em console e no arquivo `app.log`.
- Falha em um envio individual não interrompe os demais (o script continua e reporta o resumo no final).
- Variáveis de ambiente ausentes geram erro claro antes de qualquer chamada externa.

## Licença

Projeto de teste técnico, sem licença específica.

