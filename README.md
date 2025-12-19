# Agentes Python CLI

CLI em Python que utiliza OpenRouter para acessar modelos de linguagem e oferece agentes especializados para tarefas comuns.

## 🚀 Funcionalidades

- **Email Drafter**: Cria emails profissionais a partir de uma descrição
- **Creative Writing Prompt Generator**: Gera prompts criativos para escrita baseados em gêneros/temas
- **Meeting Notes Formatter**: Organiza notas de reunião em itens de ação estruturados

## 💡 Capacidades

- **Múltiplos Modelos**: Suporte para GPT-4o, GPT-4o-mini, Claude 3 (Haiku, Sonnet, Opus) e Llama 3.1
- **Rate Limiting**: Controle automático de taxa de requisições (10 chamadas por minuto)
- **Retry Automático**: Tentativas automáticas com backoff exponencial em caso de falhas temporárias
- **Validação de Input**: Verificação automática de conteúdo apropriado para cada agente
- **Modo Interativo**: Interface amigável para uso contínuo
- **Comandos CLI**: Execução direta via linha de comando

## 📋 Requisitos

- Python 3.8 ou superior
- API key do OpenRouter ([obter aqui](https://openrouter.ai/keys))

## 🚀 Início Rápido

### 1. Preparar o Ambiente

#### Criar e Ativar Ambiente Virtual (Recomendado)

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Instalar Dependências

```bash
pip install -r requirements.txt
```


## 📖 Como Usar

### Iniciar o Menu Interativo

```bash
python -m src.cli
```

O menu permite escolher entre os três agentes e usar de forma interativa.

### Exemplos de Uso

#### Email Drafter

Após iniciar o menu e selecionar "Email Drafter":

```
Descreva o email: Solicitar reunião com o time de desenvolvimento para discutir novas features

Gerando email...

Assunto: Solicitação de Reunião - Discussão de Novas Features

Prezado Time de Desenvolvimento,

Gostaria de solicitar uma reunião para discutirmos as novas features que estão planejadas para o próximo ciclo de desenvolvimento...

Atenciosamente,
[Seu nome]
```

#### Creative Writing Prompt Generator

Após iniciar o menu e selecionar "Creative Writing Prompt Generator":

```
Gêneros/temas de interesse: ficção científica, cyberpunk, futuro distópico

Gerando prompts...

1. Em Neo-Tóquio 2087, um hacker descoberto descobre que sua mente foi clonada...

2. Uma corporação controla todos os sonhos da humanidade, mas você acorda...
```

#### Meeting Notes Formatter

Após iniciar o menu e selecionar "Meeting Notes Formatter":

```
Cole as notas: Reunião hoje discutimos novo projeto precisa de timeline definimos prazo para próxima semana João vai enviar proposta

Formatando notas...

📋 REUNIÃO - [Data]

📌 TÓPICOS DISCUTIDOS:
- Novo projeto em desenvolvimento
- Necessidade de definição de timeline

✅ DECISÕES:
- Prazo estabelecido para próxima semana

📝 AÇÕES:
- [ ] João: Enviar proposta até [data]
```

## ⚠️ Solução de Problemas

### "API key inválida ou não autorizada"
- Verifique se a API key está correta no [OpenRouter](https://openrouter.ai/keys)
- Certifique-se de que a API key tem créditos disponíveis

### "Rate limit excedido"
- Aguarde alguns segundos antes de tentar novamente
- O sistema implementa rate limiting automático

### Erro de conexão
- Verifique sua conexão com a internet
- O sistema tenta novamente automaticamente em caso de falhas temporárias

## 📁 Estrutura do Projeto

```
.
├── src/
│   ├── __main__.py          # Ponto de entrada
│   ├── cli.py                # Interface CLI principal
│   ├── client.py              # Cliente OpenRouter
│   ├── config.py             # Configurações
│   ├── utils.py              # Funções auxiliares
│   ├── exceptions.py         # Exceções customizadas
│   └── agents/               # Agentes especializados
│       ├── __init__.py
│       ├── email_drafter.py
│       ├── notes_formatter.py
│       └── prompt_generator.py
├── requirements.txt          # Dependências
└── README.md                # Este arquivo
```

