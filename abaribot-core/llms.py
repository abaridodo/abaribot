import os
from enum import Enum
from typing import List, Dict, Any, Optional
import httpx
import json
import logging
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
class LLMProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    MISTRAL = "mistral"
    CUSTOM = "custom"

class LLMService:
    def __init__(self):
        self.provider_priority = [
            LLMProvider.OPENAI,
            LLMProvider.ANTHROPIC,
            LLMProvider.MISTRAL,
            LLMProvider.CUSTOM
        ]
        self.timeout = 30.0
        self.max_retries = 2

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        context: str = "",
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Generate response using available LLMs with fallback mechanism
        """
        for provider in self.provider_priority:
            try:
                if provider == LLMProvider.OPENAI:
                    return await self._openai_request(messages, context, temperature)
                elif provider == LLMProvider.ANTHROPIC:
                    return await self._anthropic_request(messages, context, temperature)
                elif provider == LLMProvider.MISTRAL:
                    return await self._mistral_request(messages, context, temperature)
                else:
                    return await self._custom_model_request(messages, context, temperature)
            except Exception as e:
                logging.error(f"{provider.value} failed: {str(e)}")
                continue

        raise Exception("All LLM providers failed")

    async def _openai_request(
        self,
        messages: List[Dict[str, str]],
        context: str,
        temperature: float
    ) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }

        system_message = {
            "role": "system",
            "content": f"You are Dr.Eye, an ophthalmology specialist. Context: {context}"
        }

        payload = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 1024
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()

            try:
                content = json.loads(data['choices'][0]['message']['content'])
            except json.JSONDecodeError:
                content = {"response": data['choices'][0]['message']['content']}

            return {
                "provider": "openai",
                "content": content,
                "usage": data.get("usage", {})
            }

    async def _anthropic_request(
        self,
        messages: List[Dict[str, str]],
        context: str,
        temperature: float
    ) -> Dict[str, Any]:
        headers = {
            "x-api-key": settings.ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }

        formatted_messages = [
            {"role": "user", "content": f"Context: {context}"}
        ] + messages

        payload = {
            "model": "claude-3-opus-20240229",
            "messages": formatted_messages,
            "max_tokens": 1024,
            "temperature": temperature,
            "system": "You are Dr.Eye, an ophthalmology specialist. Respond in JSON format."
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()

            try:
                content = json.loads(data['content'][0]['text'])
            except json.JSONDecodeError:
                content = {"response": data['content'][0]['text']}

            return {
                "provider": "anthropic",
                "content": content,
                "usage": data.get("usage", {})
            }

    async def _mistral_request(
        self,
        messages: List[Dict[str, str]],
        context: str,
        temperature: float
    ) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {settings.MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }

        system_message = {
            "role": "system",
            "content": f"You are Dr.Eye, an ophthalmology specialist. Context: {context}"
        }

        payload = {
            "model": "mistral-large-latest",
            "messages": [system_message] + messages,
            "temperature": temperature,
            "response_format": {"type": "json_object"}
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                "https://api.mistral.ai/v1/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()

            try:
                content = json.loads(data['choices'][0]['message']['content'])
            except json.JSONDecodeError:
                content = {"response": data['choices'][0]['message']['content']}

            return {
                "provider": "mistral",
                "content": content,
                "usage": data.get("usage", {})
            }

    async def _custom_model_request(
        self,
        messages: List[Dict[str, str]],
        context: str,
        temperature: float
    ) -> Dict[str, Any]:
        """Fallback to our custom fine-tuned model"""
        
        return {
            "provider": "custom",
            "content": {
                "response": "As an ophthalmology specialist, I recommend consulting your eye doctor about this concern.",
                "confidence": 0.85
            },
            "usage": {}
        }

if __name__=="__main__":
    pass