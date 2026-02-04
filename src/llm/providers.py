"""
LLM Provider Implementations
"""

import os
from typing import AsyncIterator

from llm.base import LLMProvider


class AnthropicProvider(LLMProvider):
    """Anthropic Claude API Provider"""

    def __init__(self, model: str, api_key: str, **kwargs):
        super().__init__(model, api_key, **kwargs)
        try:
            from anthropic import AsyncAnthropic
            base_url = kwargs.get("base_url")
            self.client = AsyncAnthropic(api_key=api_key, base_url=base_url)
        except ImportError:
            raise ImportError("anthropic package is required. Install with: pip install anthropic")

    async def generate(
        self,
        prompt: str,
        max_tokens: int = 2000,
        temperature: float = 0.7
    ) -> str:
        """Generate text using Anthropic Claude"""
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return response.content[0].text
        except Exception as e:
            raise RuntimeError(f"Anthropic API error: {e}")

    async def generate_stream(
        self,
        prompt: str,
        max_tokens: int = 2000,
        temperature: float = 0.7
    ) -> AsyncIterator[str]:
        """Generate streaming text using Anthropic Claude"""
        try:
            stream = await self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                stream=True
            )

            async for event in stream:
                if event.type == "content_block_delta":
                    yield event.delta.text

        except Exception as e:
            raise RuntimeError(f"Anthropic API streaming error: {e}")


class OpenAIProvider(LLMProvider):
    """OpenAI GPT API Provider"""

    def __init__(self, model: str, api_key: str, **kwargs):
        super().__init__(model, api_key, **kwargs)
        try:
            from openai import AsyncOpenAI
            base_url = kwargs.get("base_url")
            self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        except ImportError:
            raise ImportError("openai package is required. Install with: pip install openai")

    async def generate(
        self,
        prompt: str,
        max_tokens: int = 2000,
        temperature: float = 0.7
    ) -> str:
        """Generate text using OpenAI GPT"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )

            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {e}")

    async def generate_stream(
        self,
        prompt: str,
        max_tokens: int = 2000,
        temperature: float = 0.7
    ) -> AsyncIterator[str]:
        """Generate streaming text using OpenAI GPT"""
        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                stream=True
            )

            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            raise RuntimeError(f"OpenAI API streaming error: {e}")


def create_llm_provider(config: dict) -> LLMProvider:
    """Factory function to create LLM provider from config"""

    # Get API key from config or environment
    provider = config.get("provider", "anthropic").lower()
    model = config.get("model", "claude-sonnet-4-5-20250929")

    # Try to get API key from config, then environment
    api_key = config.get("api_key") or os.getenv(
        "ANTHROPIC_API_KEY" if provider == "anthropic" else "OPENAI_API_KEY"
    )

    if not api_key:
        raise ValueError(f"API key not found for {provider}")

    # Create provider instance
    if provider == "anthropic":
        return AnthropicProvider(model, api_key, **config)
    elif provider == "openai":
        return OpenAIProvider(model, api_key, **config)
    else:
        raise ValueError(f"Unsupported provider: {provider}")
