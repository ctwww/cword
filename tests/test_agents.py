"""
Tests for Agent System
"""

import pytest
from datetime import datetime
from agents.base import Agent, AgentConfig
from agents.built_in.product_manager import ProductManagerAgent


class MockLLMProvider:
    """Mock LLM Provider for testing"""

    async def generate(self, prompt: str, **kwargs) -> str:
        return "This is a test response from the agent"


@pytest.mark.asyncio
async def test_agent_config():
    """Test AgentConfig initialization"""
    config_dict = {
        "name": "Test Agent",
        "role": "test",
        "description": "A test agent",
        "system_prompt": "You are a test agent",
        "emoji": "🧪"
    }

    config = AgentConfig(config_dict)

    assert config.name == "Test Agent"
    assert config.role == "test"
    assert config.emoji == "🧪"


@pytest.mark.asyncio
async def test_product_manager_agent():
    """Test ProductManagerAgent"""
    config_dict = {
        "name": "Product Manager",
        "role": "product_manager",
        "description": "Test PM agent",
        "system_prompt": "You are a PM",
        "emoji": "🎯"
    }

    config = AgentConfig(config_dict)
    llm = MockLLMProvider()
    agent = ProductManagerAgent(config, llm)

    assert agent.name == "Product Manager"
    assert agent.role == "product_manager"

    # Test response generation
    from core.session import Message
    messages = [Message(role="user", content="I want to build a todo app")]
    context = {"stage": "initial"}

    response = await agent.generate_response(messages, context)

    assert response == "This is a test response from the agent"


@pytest.mark.asyncio
async def test_agent_build_prompt():
    """Test prompt building"""
    config_dict = {
        "name": "Test Agent",
        "role": "test",
        "description": "Test",
        "system_prompt": "You are helpful",
        "emoji": "🧪"
    }

    config = AgentConfig(config_dict)
    llm = MockLLMProvider()
    agent = Agent(config, llm)  # Can't instantiate abstract class directly

    # Test with ProductManagerAgent instead
    pm_agent = ProductManagerAgent(config, llm)

    from core.session import Message
    messages = [
        Message(role="user", content="Hello"),
        Message(role="agent", agent_name="Test", content="Hi there")
    ]

    prompt = pm_agent.build_prompt(messages)

    assert "Product Manager" in prompt
    assert "Hello" in prompt
    assert "Hi there" in prompt
