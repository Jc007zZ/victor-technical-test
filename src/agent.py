from openai import OpenAI
from typing import Optional

from .exceptions import InvalidAPIKeyError, RateLimitError, ConnectionError as OpenRouterConnectionError
from .config import AppConfig, SUPPORTED_MODELS
from .utils import retry_with_backoff, RateLimiter


class OpenRouterClient:
    """Cliente para interagir com a API do OpenRouter"""
    
    def __init__(
        self, 
        api_key: str, 
        model: str = "gpt-4o-mini", 
        timeout: int = 30,
        max_retries: int = 3,
        config: Optional[AppConfig] = None
    ):
        self.api_key = api_key
        self.config = config or AppConfig()
        self.model = model
        self.timeout = timeout
        self.max_retries = max_retries
        self.rate_limiter = RateLimiter()
        self._validate_model(model)
        
        self.client = OpenAI(
            api_key=api_key,
            base_url=self.config.openrouter_base_url,
            timeout=timeout
        )

    def _validate_model(self, model: str) -> None:
        if model not in SUPPORTED_MODELS:
            raise ValueError(
                f"Modelo '{model}' não suportado. "
                f"Modelos disponíveis: {', '.join(sorted(SUPPORTED_MODELS))}"
            )

    def send_message(
        self, 
        message: str, 
        model: Optional[str] = None, 
        system_prompt: Optional[str] = None
    ) -> str:
        """Envia mensagem para a API do OpenRouter."""
        if model:
            self._validate_model(model)
        model = model or self.model

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": message})

        def _make_request():
            self.rate_limiter()
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages
                )
                
                if response.choices and len(response.choices) > 0:
                    return response.choices[0].message.content
                else:
                    raise ValueError("Resposta da API não contém choices válidas")
                    
            except Exception as e:
                error_message = str(e)
                if "401" in error_message or "Unauthorized" in error_message:
                    raise InvalidAPIKeyError("API key inválida ou não autorizada")
                elif "429" in error_message or "rate limit" in error_message.lower():
                    raise RateLimitError("Rate limit excedido. Tente novamente mais tarde")
                elif "Connection" in str(type(e).__name__) or "timeout" in error_message.lower():
                    raise OpenRouterConnectionError(f"Erro de conexão: {error_message}")
                else:
                    raise ValueError(f"Erro na requisição: {error_message}")

        try:
            return retry_with_backoff(
                _make_request,
                max_retries=self.max_retries,
                base_delay=self.config.retry_delay
            )
        except (InvalidAPIKeyError, RateLimitError, OpenRouterConnectionError):
            raise
        except Exception as e:
            raise ValueError(f"Erro na requisição: {str(e)}")

    def validate_api_key(self) -> bool:
        """Valida a API key."""
        if not self.api_key or not isinstance(self.api_key, str):
            return False
        if len(self.api_key.strip()) == 0:
            return False
        return self.api_key.startswith('sk-or-')