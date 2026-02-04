"""
Agent Factory - Create agents from configuration
"""

from typing import List, Dict
import yaml
from pathlib import Path
import os

from agents.base import Agent, AgentConfig
from agents.built_in.product_manager import ProductManagerAgent
from agents.built_in.tech_lead import TechLeadAgent
from agents.built_in.business_consultant import BusinessConsultantAgent
from agents.built_in.security_expert import SecurityExpertAgent


class AgentFactory:
    """Factory for creating agents"""

    def __init__(self, config: Dict):
        self.config = config
        self.default_language = self._get_default_language()
        self.agent_configs = self._load_agent_configs()

    def _get_default_language(self) -> str:
        """Get default language from config or environment"""
        # Check config first
        if "default_language" in self.config:
            return self.config["default_language"]

        # Check environment variable
        env_lang = os.getenv("CWORD_LANGUAGE", "")
        if env_lang in ["zh", "en"]:
            return env_lang

        # Default to Chinese for Chinese users
        # Could also check system locale here
        return "zh"

    def _load_agent_configs(self) -> List[Dict]:
        """Load agent configurations from file"""
        config_path = Path.home() / ".cword" / "config" / "agents.yaml"

        # Also check project config directory
        project_config_path = Path.cwd() / "config" / "agents.yaml"

        # Use project config if exists, otherwise use home directory
        if project_config_path.exists():
            config_path = project_config_path

        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
                agents_config = config_data.get("agents", [])

                # Apply default language if not specified
                for agent_config in agents_config:
                    if "language" not in agent_config:
                        agent_config["language"] = self.default_language

                return agents_config

        # Return default configs if file doesn't exist
        return self._get_default_agent_configs()

    def _get_default_agent_configs(self) -> List[Dict]:
        """Get default agent configurations"""
        lang = self.default_language

        return [
            {
                "name": "产品经理" if lang == "zh" else "Product Manager",
                "role": "product_manager",
                "emoji": "🎯",
                "description": "Experienced product manager, skilled in requirement mining" if lang == "en" else "经验丰富的产品经理，擅长需求挖掘",
                "system_prompt": "Auto-generated from built-in prompts",
                "language": lang,
                "model": {}
            },
            {
                "name": "技术专家" if lang == "zh" else "Tech Lead",
                "role": "tech_lead",
                "emoji": "🔧",
                "description": "Senior technical expert, skilled in architecture design" if lang == "en" else "资深技术专家，擅长架构设计",
                "system_prompt": "Auto-generated from built-in prompts",
                "language": lang,
                "model": {}
            },
            {
                "name": "业务顾问" if lang == "zh" else "Business Consultant",
                "role": "business_consultant",
                "emoji": "💼",
                "description": "Business value analyst, skilled in market analysis" if lang == "en" else "商业价值分析师，擅长市场分析",
                "system_prompt": "Auto-generated from built-in prompts",
                "language": lang,
                "model": {}
            },
            {
                "name": "安全专家" if lang == "zh" else "Security Expert",
                "role": "security_expert",
                "emoji": "🛡️",
                "description": "Security expert, skilled in identifying risks" if lang == "en" else "安全专家，擅长识别风险",
                "system_prompt": "Auto-generated from built-in prompts",
                "language": lang,
                "model": {}
            }
        ]

    def create_agent(self, config_dict: Dict) -> Agent:
        """Create single agent from config"""
        config = AgentConfig(config_dict)

        # Import LLM provider here to avoid circular import
        from llm.providers import create_llm_provider
        llm_provider = create_llm_provider(config.model_config or {})

        # Create agent based on role
        role = config.role

        if role == "product_manager":
            return ProductManagerAgent(config, llm_provider)
        elif role == "tech_lead":
            return TechLeadAgent(config, llm_provider)
        elif role == "business_consultant":
            return BusinessConsultantAgent(config, llm_provider)
        elif role == "security_expert":
            return SecurityExpertAgent(config, llm_provider)
        else:
            # Generic agent
            return GenericAgent(config, llm_provider)

    def create_all_agents(self) -> List[Agent]:
        """Create all agents from configuration"""
        agents = []

        for agent_config in self.agent_configs:
            try:
                agent = self.create_agent(agent_config)
                agents.append(agent)
            except Exception as e:
                print(f"Warning: Failed to create agent {agent_config.get('name')}: {e}")

        return agents


class GenericAgent(Agent):
    """Generic agent for custom roles"""

    async def generate_response(
        self,
        conversation_history: List,
        context: Dict
    ) -> str:
        """Generate response"""
        prompt = self.build_prompt(conversation_history)

        # Add context-specific instructions
        if context.get("stage") == "initial":
            if self.config.language == "zh":
                prompt += "\n\n注意：这是对话的开始阶段。"
            else:
                prompt += "\n\nNote: This is the beginning of the conversation."

        response = await self.llm.generate(prompt)
        return response
