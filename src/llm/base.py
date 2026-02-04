"""
LLM Provider Base Class
"""

from abc import ABC, abstractmethod
from typing import AsyncIterator, Optional


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""

    def __init__(self, model: str, api_key: str, **kwargs):
        self.model = model
        self.api_key = api_key
        self.kwargs = kwargs

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        max_tokens: int = 2000,
        temperature: float = 0.7
    ) -> str:
        """Generate text completion"""
        pass

    @abstractmethod
    async def generate_stream(
        self,
        prompt: str,
        max_tokens: int = 2000,
        temperature: float = 0.7
    ) -> AsyncIterator[str]:
        """Generate text with streaming"""
        pass

    def count_tokens(self, text: str) -> int:
        """Estimate token count (rough approximation)"""
        # Rough estimate: ~4 characters per token for English
        # For Chinese, ~2 characters per token
        chinese_chars = sum(1 for char in text if '\u4e00' <= char <= '\u9fff')
        non_chinese = len(text) - chinese_chars

        return (chinese_chars // 2) + (non_chinese // 4)

    def validate_api_key(self) -> bool:
        """Validate API key"""
        return bool(self.api_key and len(self.api_key) > 10)

    async def test_connection(self) -> bool:
        """Test connection to LLM API"""
        try:
            response = await self.generate("Hello", max_tokens=10)
            return len(response) > 0
        except Exception:
            return False
