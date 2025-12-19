import os
import re
import stat
import time
from pathlib import Path
from typing import Callable, Optional, TypeVar
from collections import deque

from .exceptions import RateLimitError, ConnectionError
from .config import MAX_INPUT_LENGTH

T = TypeVar('T')


def mask_api_key(api_key: str, visible_chars: int = 4) -> str:
    """Mascara API key mostrando apenas últimos caracteres"""
    if len(api_key) <= visible_chars:
        return "*" * len(api_key)
    return "*" * (len(api_key) - visible_chars) + api_key[-visible_chars:]


def sanitize_input(text: str, max_length: int = MAX_INPUT_LENGTH) -> str:
    """Sanitiza input do usuário"""
    if not text or not isinstance(text, str):
        raise ValueError("Input inválido")
    
    text = text.strip()
    
    if len(text) == 0:
        raise ValueError("Input não pode estar vazio")
    
    if len(text) > max_length:
        raise ValueError(f"Input muito longo (máximo: {max_length} caracteres)")
    
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)
    
    return text


def validate_input_length(text: str, max_length: int = MAX_INPUT_LENGTH) -> bool:
    """Valida tamanho do input"""
    if len(text) > max_length:
        raise ValueError(f"Input muito longo. Máximo: {max_length} caracteres")
    return True


def get_api_key_from_env_or_file() -> Optional[str]:
    """Busca API key de variável de ambiente ou arquivo de configuração"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if api_key:
        return api_key
    
    config_file = Path.home() / ".openrouter" / "api_key"
    if config_file.exists():
        return config_file.read_text().strip()
    
    return None


def get_api_key(api_key_arg: Optional[str] = None) -> str:
    """Obtém API key com prioridade: argumento CLI > env > arquivo"""
    if api_key_arg:
        return api_key_arg
    
    env_key = get_api_key_from_env_or_file()
    if env_key:
        return env_key
    
    raise ValueError("API key não encontrada")


def create_config_file(path: Path, content: str) -> None:
    """Cria arquivo de configuração com permissões adequadas"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    path.chmod(stat.S_IRUSR | stat.S_IWUSR)


def retry_with_backoff(
    func: Callable[[], T],
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0
) -> T:
    """Retry automático com backoff exponencial"""
    for attempt in range(max_retries):
        try:
            return func()
        except (ConnectionError, RateLimitError) as e:
            if attempt == max_retries - 1:
                raise
            delay = min(base_delay * (2 ** attempt), max_delay)
            time.sleep(delay)
    raise Exception("Max retries exceeded")


class RateLimiter:
    """Rate limiter para controlar chamadas à API"""
    
    def __init__(self, max_calls: int = 10, time_window: int = 60):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = deque()
    
    def __call__(self):
        """Verifica se pode fazer chamada, levanta exceção se rate limit excedido"""
        now = time.time()
        while self.calls and self.calls[0] < now - self.time_window:
            self.calls.popleft()
        
        if len(self.calls) >= self.max_calls:
            raise RateLimitError(
                f"Rate limit excedido: {self.max_calls} chamadas por {self.time_window}s"
            )
        
        self.calls.append(now)

