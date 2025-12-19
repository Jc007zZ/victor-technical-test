from __future__ import annotations

import sys
from typing import Optional

import questionary
import typer
from prompt_toolkit.styles import Style

from .agent import OpenRouterClient
from .agents import EmailDrafter, NotesFormatter, PromptGenerator
from .config import (
    API_KEY_ERROR_KEYWORDS,
    EXIT_COMMANDS,
    RETRY_API_KEY_SIGNAL,
    AppConfig,
)
from .exceptions import (
    ConnectionError as OpenRouterConnectionError,
    InvalidAPIKeyError,
    RateLimitError,
)
from .utils import get_api_key, sanitize_input, validate_input_length

custom_style = Style([
    ('qmark', 'fg:#00ff00'),
    ('question', ''),
    ('answer', 'fg:#3A96DD'),
    ('pointer', 'fg:#3A96DD'),
    ('highlighted', 'fg:#3A96DD'),
    ('selected', 'fg:#3A96DD'),
    ('separator', ''),
    ('instruction', 'fg:#3A96DD'),
    ('text', ''),
    ('disabled', 'fg:#858585 italic')
])

app = typer.Typer(help="CLI para agentes especializados usando OpenRouter")

AGENT_CONFIG = {
    "Email Drafter": {
        "class": EmailDrafter,
        "prompt": "Descreva o email:",
        "action": "Gerando email...",
        "method": "draft"
    },
    "Creative Writing Prompt Generator": {
        "class": PromptGenerator,
        "prompt": "Gêneros/temas de interesse",
        "action": "Gerando prompts...",
        "method": "generate"
    },
    "Meeting Notes Formatter": {
        "class": NotesFormatter,
        "prompt": "Cole as notas",
        "action": "Formatando notas...",
        "method": "format"
    }
}


def _is_api_key_error(error: Exception) -> bool:
    """Verifica se o erro é relacionado a API key"""
    error_str = str(error)
    return any(keyword in error_str for keyword in API_KEY_ERROR_KEYWORDS)


def get_client(api_key: Optional[str] = None, model: Optional[str] = None) -> OpenRouterClient:
    """Cria e valida cliente OpenRouter."""
    try:
        resolved_api_key = get_api_key(api_key)
    except ValueError as e:
        raise ValueError(str(e))
    
    config = AppConfig()
    client = OpenRouterClient(
        api_key=resolved_api_key, 
        model=model or config.default_model
    )
    
    if not client.validate_api_key():
        raise InvalidAPIKeyError("API key inválida ou não autorizada")
    
    return client


def run_agent_interactive(
    agent_name: str, 
    client: OpenRouterClient, 
    model: Optional[str] = None
) -> Optional[str]:
    """Executa agente em modo interativo."""
    config = AGENT_CONFIG.get(agent_name)
    if not config:
        raise ValueError(f"Agente desconhecido: {agent_name}")
    
    agent = config["class"](client)
    typer.echo(f"\n{agent_name}")
    typer.echo("Digite 'sair' para voltar\n")
    
    while True:
        user_input = questionary.text(config["prompt"], style=custom_style).ask()
        if user_input is None:
            return None
        if not user_input or user_input.lower() in EXIT_COMMANDS:
            break
        
        try:
            validate_input_length(user_input)
            sanitized_input = sanitize_input(user_input)
        except ValueError as e:
            typer.echo(f"Erro: {e}", err=True)
            continue
        
        typer.echo(config["action"])
        try:
            method = getattr(agent, config["method"])
            result = method(sanitized_input, model)
            typer.echo(f"\n{result}\n")
        except (InvalidAPIKeyError, ValueError) as e:
            if _is_api_key_error(e):
                typer.echo(f"Erro: {e}", err=True)
                typer.echo("Voltando para inserir API key novamente...\n", err=True)
                return RETRY_API_KEY_SIGNAL
            typer.echo(f"Erro: {e}", err=True)
        except (RateLimitError, OpenRouterConnectionError) as e:
            typer.echo(f"Erro: {e}", err=True)
        except Exception as e:
            typer.echo(f"Erro: {e}", err=True)


def run_agent_command(
    agent_name: str,
    input_arg: Optional[str],
    api_key: Optional[str],
    model: Optional[str],
    interactive: bool
) -> None:
    """Função genérica para executar comandos de agentes."""
    config = AGENT_CONFIG.get(agent_name)
    if not config:
        raise ValueError(f"Agente desconhecido: {agent_name}")
    
    try:
        client = get_client(api_key, model)
        
        if interactive:
            run_agent_interactive(agent_name, client, model)
        else:
            if not input_arg:
                typer.echo(
                    f"Erro: É necessário fornecer o input ou usar --interactive",
                    err=True
                )
                raise typer.Exit(1)
            
            try:
                validate_input_length(input_arg)
                sanitized_input = sanitize_input(input_arg)
            except ValueError as e:
                typer.echo(f"Erro: {e}", err=True)
                raise typer.Exit(1)
            
            typer.echo(config["action"])
            agent = config["class"](client)
            method = getattr(agent, config["method"])
            result = method(sanitized_input, model)
            typer.echo(f"\n{result}")
            
    except typer.Exit:
        raise
    except Exception as e:
        typer.echo(f"Erro: {e}", err=True)
        raise typer.Exit(1)


def run_interactive_menu(api_key: Optional[str] = None, model: Optional[str] = None) -> None:
    """Menu interativo para seleção de agentes."""
    try:
        while True:
            client = None
            
            while client is None:
                if not api_key:
                    api_key = questionary.password("API key do OpenRouter", style=custom_style).ask()
                    if api_key is None:
                        sys.exit(0)
                    if not api_key:
                        typer.echo("Erro: API key é obrigatória", err=True)
                        typer.echo()
                        continue
                
                try:
                    client = get_client(api_key, model)
                except (ValueError, InvalidAPIKeyError) as e:
                    typer.echo(f"Erro: {e}", err=True)
                    api_key = None
                    continue
            
            while True:
                agent_choice = questionary.select(
                    "Selecione um agente",
                    choices=[
                        "Email Drafter",
                        "Creative Writing Prompt Generator",
                        "Meeting Notes Formatter",
                        "Sair"
                    ],
                    style=custom_style,
                    use_arrow_keys=True,
                    use_indicator=False,
                    pointer=">"
                ).ask()
                
                if agent_choice is None:
                    sys.exit(0)
                if not agent_choice or agent_choice == "Sair":
                    return
                
                result = run_agent_interactive(agent_choice, client, model)
                if result == RETRY_API_KEY_SIGNAL:
                    api_key = None
                    break
            
    except KeyboardInterrupt:
        sys.exit(0)
    except typer.Exit:
        raise
    except Exception as e:
        typer.echo(f"Erro: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def main(
    api_key: Optional[str] = typer.Option(None, "--api-key", "-k", help="Chave da API do OpenRouter"),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="Modelo a ser usado")
) -> None:
    """Menu interativo para seleção de agentes"""
    run_interactive_menu(api_key, model)


@app.command()
def email(
    email_description: Optional[str] = typer.Argument(None, help="Descrição do conteúdo do email"),
    api_key: Optional[str] = typer.Option(None, "--api-key", "-k", help="Chave da API do OpenRouter"),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="Modelo a ser usado"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Modo interativo")
) -> None:
    """Email Drafter: Crie emails profissionais a partir de uma descrição"""
    run_agent_command("Email Drafter", email_description, api_key, model, interactive)


@app.command()
def prompt(
    genres_or_themes: Optional[str] = typer.Argument(None, help="Gêneros ou temas para gerar prompts"),
    api_key: Optional[str] = typer.Option(None, "--api-key", "-k", help="Chave da API do OpenRouter"),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="Modelo a ser usado"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Modo interativo")
) -> None:
    """Creative Writing Prompt Generator: Gere prompts criativos para escrita"""
    run_agent_command("Creative Writing Prompt Generator", genres_or_themes, api_key, model, interactive)


@app.command()
def notes(
    raw_notes: Optional[str] = typer.Argument(None, help="Notas desorganizadas para formatar"),
    api_key: Optional[str] = typer.Option(None, "--api-key", "-k", help="Chave da API do OpenRouter"),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="Modelo a ser usado"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Modo interativo")
) -> None:
    """Meeting Notes Formatter: Organize notas de reunião em itens de ação"""
    run_agent_command("Meeting Notes Formatter", raw_notes, api_key, model, interactive)


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        run_interactive_menu()
    else:
        app()
