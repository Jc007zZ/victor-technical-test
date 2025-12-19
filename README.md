# Agentes Python CLI

CLI em Python que utiliza OpenRouter para acessar modelos de linguagem e oferece agentes especializados para tarefas comuns.

## 🚀 Funcionalidades

- **Email Drafter**: Cria emails profissionais a partir de uma descrição
- **Creative Writing Prompt Generator**: Gera prompts criativos para escrita baseados em gêneros/temas
- **Meeting Notes Formatter**: Organiza notas de reunião em itens de ação estruturados

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

### Iniciar

```bash
python -m src.cli
```

O menu permite escolher entre os três agentes e usar de forma interativa.

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
│   ├── agent.py              # Cliente OpenRouter
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

## 📝 Informações Adicionais

- O sistema valida automaticamente o conteúdo para garantir que seja apropriado para cada agente
- Entradas muito longas (>10.000 caracteres) serão rejeitadas
- O modo interativo permite múltiplas execuções sem precisar fornecer a API key novamente
- A API key nunca é exibida no terminal (exceto os últimos 4 caracteres quando necessário)
- O arquivo de configuração é criado com permissões restritas
- **Nunca compartilhe sua API key publicamente**

## 📄 Licença

Este projeto é fornecido como está, sem garantias.
