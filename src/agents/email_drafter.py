from typing import Optional
from ..agent import OpenRouterClient


class EmailDrafter:
    """Agente especializado em criação de emails profissionais"""
    
    def __init__(self, client: OpenRouterClient):
        self.client = client
        self.system_prompt = """Você é um assistente especializado em emails profissionais.

VALIDAÇÃO OBRIGATÓRIA: Verifique se o conteúdo é apropriado para email profissional. REJEITE receitas, piadas, memes ou qualquer assunto não profissional. Se não for apropriado, responda APENAS: "O conteúdo descrito não é apropriado para um email profissional. Por favor, forneça um assunto relacionado a trabalho, negócios ou contexto profissional."

Para emails válidos: use tom profissional, estruture com saudação/corpo/fechamento, seja claro e objetivo."""

    def draft(self, description: str, model: Optional[str] = None) -> str:
        """Cria um email profissional baseado na descrição fornecida."""
        user_message = f"Crie um email profissional baseado na descrição:\n\n{description}"
        
        return self.client.send_message(user_message, model, self.system_prompt)

