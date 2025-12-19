from typing import Optional
from ..agent import OpenRouterClient


class PromptGenerator:
    """Agente especializado em geração de prompts criativos para escrita"""
    
    def __init__(self, client: OpenRouterClient):
        self.client = client
        self.system_prompt = """Você é um gerador especializado de prompts criativos para escrita.

VALIDAÇÃO OBRIGATÓRIA: Verifique se o conteúdo são gêneros/temas de escrita criativa. REJEITE notas de reunião, emails, receitas ou qualquer conteúdo que não seja relacionado a escrita criativa. Se não for apropriado, responda APENAS: "O conteúdo fornecido não é apropriado para geração de prompts de escrita criativa. Por favor, forneça gêneros literários, temas ou ideias para escrita criativa."

Para inputs válidos: crie prompts envolventes com personagens/cenários/conflitos, adapte ao gênero, seja criativo mas claro."""

    def generate(self, genres_themes: str, model: Optional[str] = None) -> str:
        """Gera prompts criativos para escrita baseado em gêneros/temas."""
        user_message = f"Gere prompts criativos para escrita baseado em:\n\n{genres_themes}"
        
        return self.client.send_message(user_message, model, self.system_prompt)

