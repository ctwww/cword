"""
Config Store - Manage configuration files
"""

import yaml
from pathlib import Path
from typing import Dict


class ConfigStore:
    """Store and manage configuration"""

    def __init__(self, config: dict):
        self.config = config
        self.config_dir = self._get_config_dir()

    def _get_config_dir(self) -> Path:
        """Get config directory path"""
        config_path = Path.home() / ".cword" / "config"
        config_path.mkdir(parents=True, exist_ok=True)
        return config_path

    def save_config(self, name: str, config_data: Dict):
        """Save configuration to file"""
        config_file = self.config_dir / f"{name}.yaml"

        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)

    def load_config(self, name: str) -> Dict:
        """Load configuration from file"""
        config_file = self.config_dir / f"{name}.yaml"

        if not config_file.exists():
            return {}

        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}

    def list_configs(self) -> list:
        """List all configuration files"""
        return list(self.config_dir.glob("*.yaml"))

    def get_default_agents_config(self) -> Dict:
        """Get default agents configuration"""
        return {
            "default_model": {
                "provider": "anthropic",
                "api_key_env": "ANTHROPIC_API_KEY",
                "model": "claude-sonnet-4-5-20250929",
                "temperature": 0.7,
                "max_tokens": 2000
            },
            "agents": [
                {
                    "name": "Product Manager",
                    "role": "product_manager",
                    "emoji": "🎯",
                    "description": "Experienced product manager, skilled in requirement mining and user stories",
                    "system_prompt": "You are a Product Manager...",
                    "model": {}
                },
                {
                    "name": "Tech Lead",
                    "role": "tech_lead",
                    "emoji": "🔧",
                    "description": "Senior technical expert, skilled in architecture design and technology selection",
                    "system_prompt": "You are a Tech Lead...",
                    "model": {}
                },
                {
                    "name": "Business Consultant",
                    "role": "business_consultant",
                    "emoji": "💼",
                    "description": "Business value analyst, skilled in scenario expansion and market analysis",
                    "system_prompt": "You are a Business Consultant...",
                    "model": {}
                },
                {
                    "name": "Security Expert",
                    "role": "security_expert",
                    "emoji": "🛡️",
                    "description": "Security expert, skilled in identifying risks and privacy issues",
                    "system_prompt": "You are a Security Expert...",
                    "model": {}
                }
            ],
            "conversation": {
                "max_turns": 100,
                "summary_interval": 10,
                "decision_checkpoint": True
            },
            "output": {
                "format": "markdown",
                "directory": "./cword_output",
                "include_decision_history": True,
                "include_conversation_summary": True
            }
        }
