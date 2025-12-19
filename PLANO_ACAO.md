# Plano de Ação - Projeto de Agentes Python CLI

## Objetivo
Criar uma aplicação CLI em Python que utiliza OpenRouter para interagir com modelos de linguagem via linha de comando. A CLI oferece 3 agentes especializados que o usuário pode escolher:
- **Email Drafter**: Describe what you need to say and get a professional email
- **Creative Writing Prompt Generator**: Get writing prompts based on genres/themes
- **Meeting Notes Formatter**: Convert messy notes into organized action items

## Estrutura do Projeto

```
agentes-python/
├── .env                    # (opcional, se necessário)
├── .gitignore
├── requirements.txt        # Dependências do projeto
├── README.md              # Documentação principal
├── PLANO_ACAO.md          # Este arquivo
├── src/
│   ├── cli.py              # Interface CLI principal
│   ├── agent.py            # Lógica do agente e comunicação com OpenRouter
│   └── agents/             # Agentes especializados
│       ├── __init__.py
│       ├── email_drafter.py
│       ├── prompt_generator.py
│       └── notes_formatter.py
└── utils.py                # Funções auxiliares (opcional)
```

## Dependências

- `typer`: Framework para criar CLI moderna e intuitiva
- `openai`: SDK oficial da OpenAI (compatível com OpenRouter)

## Plano de Implementação

### Fase 1: Configuração Inicial ✅
- [x] Criar estrutura de diretórios
- [x] Configurar `requirements.txt`
- [x] Criar `README.md` com instruções
- [x] Criar `.gitignore`

### Fase 2: Implementação do Agente (agent.py)
- [x] Criar classe ou função para comunicação com OpenRouter
- [x] Implementar função para enviar mensagens à API
- [x] Implementar tratamento de erros
- [x] Implementar parsing de respostas da API
- [x] Adicionar suporte a diferentes modelos

**Funcionalidades do agent.py:**
```python
# Estrutura sugerida
def send_message(api_key: str, message: str, model: str = "gpt-4o-mini") -> str:
    """
    Envia mensagem para OpenRouter e retorna resposta
    """
    pass

def validate_api_key(api_key: str) -> bool:
    """
    Valida se a API key está no formato correto
    """
    pass
```

### Fase 3: Implementação dos Agentes Especializados ✅
- [x] Criar estrutura de diretórios para agentes (`src/agents/`)
- [x] Implementar Email Drafter agent
- [x] Implementar Creative Writing Prompt Generator agent
- [x] Implementar Meeting Notes Formatter agent
- [x] Criar sistema de prompts especializados para cada agente

**Funcionalidades dos Agentes:**
- **Email Drafter**: Recebe descrição do que precisa ser dito e gera email profissional
- **Prompt Generator**: Recebe gêneros/temas e gera prompts criativos para escrita
- **Notes Formatter**: Recebe notas desorganizadas e converte em itens de ação organizados

### Fase 4: Implementação da CLI (cli.py) ✅
- [x] Configurar Typer app
- [x] Criar comando para seleção de agente (`email`, `prompt`, `notes`)
- [x] Adicionar opção `--api-key` para receber chave via CLI
- [x] Adicionar opção `--model` para escolher modelo
- [x] Implementar modo interativo para cada agente
- [x] Adicionar tratamento de erros na CLI
- [x] Adicionar mensagens de ajuda e feedback ao usuário

**Estrutura da CLI:**
```bash
# Comandos principais
python -m src.cli email --api-key <key> "descrição do email"
python -m src.cli prompt --api-key <key> "gênero/tema"
python -m src.cli notes --api-key <key> "notas desorganizadas"

# Com modelo específico
python -m src.cli email --api-key <key> --model <model> "descrição"

# Modo interativo
python -m src.cli email --api-key <key> --interactive
python -m src.cli prompt --api-key <key> --interactive
python -m src.cli notes --api-key <key> --interactive
```

### Fase 5: Melhorias e Refinamentos
- [ ] Adicionar formatação de saída (rich para output colorido)
- [ ] Implementar histórico de conversação no modo interativo
- [ ] Adicionar validações de entrada
- [ ] Melhorar tratamento de erros com mensagens claras
- [ ] Adicionar suporte a streaming de respostas (opcional)
- [ ] Criar testes básicos (opcional)

### Fase 6: Documentação e Finalização
- [ ] Atualizar README com exemplos completos
- [ ] Documentar todos os comandos disponíveis
- [ ] Adicionar exemplos de uso avançado
- [ ] Revisar código e garantir qualidade

## Detalhamento Técnico

### agent.py - Responsabilidades
1. **Comunicação com OpenRouter**
   - Usar SDK da OpenAI configurado para OpenRouter
   - Configurar base_url para `https://openrouter.ai/api/v1`
   - Enviar headers corretos (Authorization via api_key)
   - Processar respostas do SDK

2. **Tratamento de Erros**
   - Erros de conexão
   - Erros de autenticação (API key inválida)
   - Erros de rate limiting
   - Erros de formato de resposta

3. **Configuração**
   - URL base da API
   - Modelo padrão
   - Timeout de requisições

### agents/ - Responsabilidades
1. **Email Drafter (email_drafter.py)**
   - Receber descrição do conteúdo do email
   - Gerar prompt especializado para criação de email profissional
   - Formatar saída como email estruturado

2. **Creative Writing Prompt Generator (prompt_generator.py)**
   - Receber gêneros/temas de interesse
   - Gerar prompts criativos e inspiradores
   - Oferecer variações de prompts

3. **Meeting Notes Formatter (notes_formatter.py)**
   - Receber notas desorganizadas
   - Identificar ações, decisões e tópicos
   - Formatar em estrutura organizada com itens de ação

### cli.py - Responsabilidades
1. **Interface do Usuário**
   - Receber argumentos via linha de comando
   - Permitir seleção de agente (email, prompt, notes)
   - Validar inputs do usuário
   - Exibir respostas formatadas
   - Gerenciar modo interativo para cada agente

2. **Orquestração**
   - Instanciar agente selecionado
   - Chamar funções do `agent.py` para comunicação com OpenRouter
   - Gerenciar fluxo de conversação específico de cada agente
   - Tratar erros e exibir mensagens amigáveis

3. **UX**
   - Mensagens de ajuda claras para cada agente
   - Feedback durante processamento
   - Formatação de saída legível e específica por agente

## Endpoints OpenRouter

**URL Base:** `https://openrouter.ai/api/v1/chat/completions`

**Método:** POST

**Headers:**
```
Authorization: Bearer <api_key>
Content-Type: application/json
```

**Body:**
```json
{
  "model": "gpt-4o-mini",
  "messages": [
    {
      "role": "user",
      "content": "mensagem do usuário"
    }
  ]
}
```

**Response:**
```json
{
  "choices": [
    {
      "message": {
        "content": "resposta do modelo"
      }
    }
  ]
}
```

## Ordem de Execução Recomendada

1. **Criar `.gitignore`** - Ignorar arquivos desnecessários ✅
2. **Implementar `agent.py`** - Lógica core primeiro ✅
3. **Testar `agent.py` isoladamente** - Garantir que funciona
4. **Criar estrutura de agentes** - Diretório `src/agents/`
5. **Implementar cada agente especializado** - Email, Prompt, Notes
6. **Implementar `cli.py` básico** - Comandos para cada agente
7. **Adicionar modo interativo** - Expandir funcionalidades
8. **Refinar e melhorar** - Melhorar UX e tratamento de erros

## Checklist de Validação

Antes de considerar o projeto completo:

- [ ] CLI funciona com API key via `--api-key`
- [ ] Todos os 3 agentes (email, prompt, notes) funcionam corretamente
- [ ] Modo único funciona para cada agente
- [ ] Modo interativo funciona para cada agente
- [ ] Cada agente gera saídas apropriadas ao seu propósito
- [ ] Erros são tratados e exibidos claramente
- [ ] Código está limpo e organizado
- [ ] README está completo e atualizado com exemplos de cada agente
- [ ] Projeto pode ser instalado e executado por terceiros

## Próximos Passos Imediatos

1. ✅ Criar `.gitignore`
2. ✅ Implementar `agent.py` com classe de comunicação com OpenRouter
3. Criar estrutura de diretórios para agentes (`src/agents/`)
4. Implementar Email Drafter agent
5. Implementar Creative Writing Prompt Generator agent
6. Implementar Meeting Notes Formatter agent
7. Implementar `cli.py` com comandos para cada agente
8. Testar fluxo completo de cada agente

