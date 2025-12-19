from typing import Optional
from ..client import OpenRouterClient


class NotesFormatter:
    """Agente especializado em formatação de notas de reunião"""
    
    def __init__(self, client: OpenRouterClient):
        self.client = client
        self.system_prompt = """Você é um especialista em organização e formatação de notas de reunião.

VALIDAÇÃO OBRIGATÓRIA: Verifique se o conteúdo são realmente notas de reunião/trabalho. REJEITE receitas, piadas, memes, textos criativos ou qualquer conteúdo que não seja notas de reunião/profissional. Se não for apropriado, responda APENAS: "O conteúdo fornecido não parece ser notas de reunião. Por favor, forneça notas de reunião ou conteúdo profissional para formatação."

Para notas válidas: identifique ações/decisões/tópicos, organize logicamente, crie itens de ação claros, use formatação clara."""

    def format(self, notes: str, model: Optional[str] = None) -> str:
        """Formata notas de reunião desorganizadas em estrutura clara."""
        user_message = f"Organize as seguintes notas de reunião:\n\n{notes}"
        
        return self.client.send_message(user_message, model, self.system_prompt)

