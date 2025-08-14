
from typing import List
import httpx

from src.config import settings
import logging

logger = logging.getLogger(__name__)

OPENROUTER_API_KEY = settings.OPENROUTER_API_KEY

class OpenRouterService:
    def __init__(self):
        self.api_key = OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
    
    async def generate_response(self, messages: List[dict], qa_entries: List[dict]) -> str:
        system_message = {
            "role": "system",
            "content": f"""You are a helpful university chatbot assistant. You can answer questions based on the following Q&A database:

{chr(10).join([f"Q: {qa['question']}{chr(10)}A: {qa['answer']}{chr(10)}" for qa in qa_entries])}

Rules:
1. Only answer questions based on the provided Q&A database
2. Be friendly and helpful in your responses
3. If you cannot find the answer in the database, respond with exactly: "I don't know the answer to that question yet, but don't worry! Please reach back out in the next 24-48 hours as I will inform our admin team to provide you with an accurate answer."
4. Do not provide information outside of the Q&A database
5. Keep responses concise but informative
"""
        }
        
        all_messages = [system_message] + messages
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        # "model": "anthropic/claude-3-sonnet",
                        "model": "deepseek/deepseek-r1-0528:free",
                        "messages": all_messages,
                        "max_tokens": 500,
                        "temperature": 0.7
                    }
                )
                response.raise_for_status()
                result = response.json()
                logger.info("Bot response generated successfully")
                logger.info(result)
                return result["choices"][0]["message"]["content"]
            
            except Exception as e:
                print(f"OpenRouter API error: {e}")
                logger.error(f"error generating bot response: {e}")
                return "I'm sorry, I'm experiencing technical difficulties. Please try again later."

openrouter_service = OpenRouterService()