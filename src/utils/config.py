"""
Configuration Management
"""

import os
import yaml
from pathlib import Path
from typing import Dict


def load_config(config_path: str = None) -> Dict:
    """Load configuration from file"""

    # Default config paths
    default_paths = [
        Path.cwd() / "config" / "cword.yaml",
        Path.home() / ".cword" / "config" / "cword.yaml",
        Path.cwd() / "cword.yaml"
    ]

    # Use provided path or search defaults
    if config_path:
        config_file = Path(config_path)
    else:
        for path in default_paths:
            if path.exists():
                config_file = path
                break
        else:
            # Return default config if none found
            return get_default_config()

    # Load YAML file
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            return config or {}
    except Exception as e:
        print(f"Warning: Failed to load config from {config_file}: {e}")
        return get_default_config()


def get_default_config() -> Dict:
    """Get default configuration"""
    return {
        "app": {
            "name": "CWord",
            "version": "1.0.0",
            "log_level": "INFO"
        },
        "directories": {
            "sessions": "~/.cword/sessions",
            "logs": "~/.cword/logs",
            "output": "~/.cword/output",
            "templates": "~/.cword/templates"
        },
        "default_model": {
            "provider": "anthropic",
            "api_key_env": "ANTHROPIC_API_KEY",
            "model": "claude-sonnet-4-5-20250929",
            "temperature": 0.7,
            "max_tokens": 2000
        },
        "conversation": {
            "max_history": 50,
            "summary_interval": 10,
            "auto_save_interval": 300
        },
        "documents": {
            "format": "markdown",
            "include_decision_history": True,
            "include_conversation_summary": True,
            "auto_export": False
        },
        "agents_config": "config/agents.yaml"
    }


def save_config(config: Dict, config_path: str = None):
    """Save configuration to file"""

    if not config_path:
        config_dir = Path.home() / ".cword" / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        config_path = config_dir / "cword.yaml"

    config_file = Path(config_path)
    config_file.parent.mkdir(parents=True, exist_ok=True)

    with open(config_file, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)


def get_env_var(key: str, default: str = None) -> str:
    """Get environment variable"""
    return os.getenv(key, default)


def get_api_key(provider: str) -> str:
    """Get API key from environment or config"""
    env_keys = {
        "anthropic": "ANTHROPIC_API_KEY",
        "openai": "OPENAI_API_KEY"
    }

    env_key = env_keys.get(provider.lower())
    if env_key:
        return os.getenv(env_key, "")

    return ""
