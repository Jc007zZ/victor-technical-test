class OpenRouterError(Exception):
    """Base exception for OpenRouter errors"""
    pass


class InvalidAPIKeyError(OpenRouterError):
    """Raised when API key is invalid or unauthorized"""
    pass


class RateLimitError(OpenRouterError):
    """Raised when rate limit is exceeded"""
    pass


class ConnectionError(OpenRouterError):
    """Raised when connection fails or timeout occurs"""
    pass

