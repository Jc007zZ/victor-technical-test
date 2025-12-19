from dataclasses import dataclass

EXIT_COMMANDS = ['sair', 'exit', 'quit', 'voltar']
API_KEY_ERROR_KEYWORDS = ["API key", "não autorizada", "inválida"]
RETRY_API_KEY_SIGNAL = "retry_api_key"
MAX_INPUT_LENGTH = 10000

SUPPORTED_MODELS = {
    "gpt-4o-mini",
    "gpt-4o",
    "claude-3-haiku",
    "claude-3-sonnet",
    "claude-3-opus",
    "llama-3.1-8b-instruct",
    "llama-3.1-70b-instruct",
}


@dataclass
class AppConfig:
    """Configuração centralizada da aplicação"""
    default_model: str = "gpt-4o-mini"
    default_timeout: int = 30
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    max_retries: int = 3
    retry_delay: float = 1.0

