"""
Base Agent Class - Abstract base for all agents
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class AgentConfig:
    """Agent configuration"""
    name: str
    role: str
    description: str
    system_prompt: str
    emoji: str = "🤖"
    model_config: Dict = None
    language: str = "en"  # Language: "en" or "zh"

    def __init__(self, config_dict: dict):
        self.name = config_dict.get("name", "Agent")
        self.role = config_dict.get("role", "generic")
        self.description = config_dict.get("description", "")
        self.system_prompt = config_dict.get("system_prompt", "")
        self.emoji = config_dict.get("emoji", "🤖")
        self.model_config = config_dict.get("model", {})
        self.language = config_dict.get("language", "en")


class Agent(ABC):
    """Abstract base class for all agents"""

    def __init__(self, config: AgentConfig, llm_provider):
        self.config = config
        self.llm = llm_provider
        self.name = config.name
        self.role = config.role
        self.description = config.description
        self.emoji = config.emoji

    @abstractmethod
    async def generate_response(
        self,
        conversation_history: List,
        context: Dict
    ) -> str:
        """Generate response based on conversation history and context"""
        pass

    def build_prompt(self, conversation_history: List) -> str:
        """Build prompt for LLM (can be overridden by subclasses)"""
        prompt = f"""You are {self.name}, {self.description}

{self.config.system_prompt}

Conversation history:
"""
        # Add last 10 messages
        for msg in conversation_history[-10:]:
            if msg.role == "user":
                prompt += f"User: {msg.content}\n"
            else:
                agent_name = msg.agent_name or "Agent"
                prompt += f"{agent_name}: {msg.content}\n"

        prompt += f"\nPlease respond as {self.name}:"
        return prompt

    async def think_before_speaking(
        self,
        conversation_history: List,
        context: Dict
    ) -> Dict:
        """Think before speaking (optional, for complex reasoning)"""
        return {
            "should_speak": True,
            "reasoning": ""
        }

    def get_style_instructions(self) -> str:
        """Get speaking style instructions"""
        return ""
