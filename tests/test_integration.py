"""
Integration Tests - End-to-End System Tests
"""

import pytest
import asyncio
from pathlib import Path
import tempfile
import shutil

from core.session import SessionManager, Message
from core.coordinator import AgentCoordinator
from agents.factory import AgentFactory
from documents.generator import DocumentGenerator
from storage.session_store import SessionStore
from storage.document_store import DocumentStore


class MockLLMProvider:
    """Mock LLM Provider for testing"""

    def __init__(self, model="test-model", api_key="test-key"):
        self.model = model
        self.api_key = api_key
        self.call_count = 0

    async def generate(self, prompt: str, max_tokens=2000, temperature=0.7) -> str:
        self.call_count += 1
        return f"Mock response #{self.call_count} for: {prompt[:50]}..."

    async def generate_stream(self, prompt: str, **kwargs):
        yield f"Mock stream response for: {prompt[:50]}..."


@pytest.fixture
def temp_config():
    """Create temporary config for testing"""
    temp_dir = tempfile.mkdtemp()

    config = {
        "app": {
            "name": "CWord-Test",
            "version": "1.0.0"
        },
        "directories": {
            "sessions": temp_dir + "/sessions",
            "output": temp_dir + "/output",
            "logs": temp_dir + "/logs",
            "templates": temp_dir + "/templates"
        },
        "default_model": {
            "provider": "anthropic",
            "model": "claude-test",
            "temperature": 0.7,
            "max_tokens": 2000
        }
    }

    yield config

    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def mock_agents(temp_config):
    """Create agents with mock LLM"""
    config = {
        "default_language": "en",
        "default_model": {
            "provider": "anthropic",
            "model": "test-model"
        }
    }

    factory = AgentFactory(config)

    # Create agents with mock LLM
    from agents.base import AgentConfig

    agents = []

    agent_configs = [
        {
            "name": "Product Manager",
            "role": "product_manager",
            "description": "Test PM",
            "system_prompt": "You are a PM",
            "emoji": "🎯",
            "language": "en",
            "model_config": {}
        },
        {
            "name": "Tech Lead",
            "role": "tech_lead",
            "description": "Test Tech Lead",
            "system_prompt": "You are a Tech Lead",
            "emoji": "🔧",
            "language": "en",
            "model_config": {}
        }
    ]

    for agent_config in agent_configs:
        config_obj = AgentConfig(agent_config)
        mock_llm = MockLLMProvider()
        agent = factory.create_agent(agent_config)

        # Replace LLM with mock
        agent.llm = mock_llm
        agents.append(agent)

    return agents


@pytest.mark.asyncio
async def test_session_lifecycle(temp_config):
    """Test complete session lifecycle"""
    session_manager = SessionManager(temp_config)

    # Create session
    session = session_manager.create_session("Test Product")
    assert session.product_name == "Test Product"
    assert len(session.messages) == 0

    # Add messages
    msg1 = Message(role="user", content="I want to build a todo app")
    session.add_message(msg1)

    msg2 = Message(role="agent", agent_name="Product Manager", content="Great idea!")
    session.add_message(msg2)

    assert len(session.messages) == 2

    # Save session
    session_manager.save_session(session.session_id)

    # Load session
    loaded_session = session_manager.get_session(session.session_id)
    assert loaded_session is not None
    assert loaded_session.product_name == "Test Product"
    assert len(loaded_session.messages) == 2


@pytest.mark.asyncio
async def test_coordinator_agent_interaction(mock_agents):
    """Test coordinator orchestrating agents"""
    coordinator = AgentCoordinator(mock_agents)
    session_manager = SessionManager({})

    session = session_manager.create_session("Integration Test Product")

    # Add user message
    user_msg = Message(role="user", content="I want to build an invoicing system")
    session.add_message(user_msg)

    # Let Product Manager speak
    response = await coordinator.let_agent_speak("Product Manager", session)

    assert response is not None
    assert len(session.messages) == 2  # User + PM
    assert session.messages[-1].agent_name == "Product Manager"

    # Let Tech Lead speak
    response2 = await coordinator.let_agent_speak("Tech Lead", session)

    assert response2 is not None
    assert len(session.messages) == 3  # User + PM + Tech Lead


@pytest.mark.asyncio
async def test_coordinator_suggestions(mock_agents):
    """Test coordinator agent suggestions"""
    coordinator = AgentCoordinator(mock_agents)
    session_manager = SessionManager({})

    session = session_manager.create_session()

    # Test with sensitive data
    msg = Message(role="user", content="We need to store user passwords securely")
    session.add_message(msg)

    suggestions = coordinator.suggest_agents(session)
    # Should suggest security expert if available
    assert isinstance(suggestions, list)


@pytest.mark.asyncio
async def test_document_generation(temp_config):
    """Test document generation"""
    session_manager = SessionManager(temp_config)
    doc_generator = DocumentGenerator(temp_config)

    # Create session with some content
    session = session_manager.create_session("Test Product")

    # Add messages
    session.add_message(Message(role="user", content="I want a todo app"))
    session.add_message(Message(
        role="agent",
        agent_name="Product Manager",
        content="Let's define the requirements"
    ))

    # Add a decision
    from core.session import Decision
    decision = Decision(
        id="decision_001",
        topic="Tech Stack",
        decision="Use Python",
        participants=["Tech Lead"],
        reasoning="Simplicity"
    )
    session.add_decision(decision)

    # Generate PRD
    prd = await doc_generator.generate_prd(session)
    assert prd is not None
    assert "Test Product" in prd

    # Generate tech spec
    tech_spec = await doc_generator.generate_tech_spec(session)
    assert tech_spec is not None

    # Generate decision history
    decisions_doc = await doc_generator.generate_decision_history(session)
    assert decisions_doc is not None
    assert "Tech Stack" in decisions_doc


@pytest.mark.asyncio
async def test_document_storage(temp_config):
    """Test document storage"""
    doc_store = DocumentStore(temp_config)

    # Save a test document
    content = "# Test PRD\n\nThis is a test PRD document."
    path = doc_store.save_prd("Test Product", content)

    assert path.exists()
    assert path.read_text(encoding='utf-8') == content

    # List documents
    docs = doc_store.list_documents("Test Product")
    assert len(docs) > 0


@pytest.mark.asyncio
async def test_agent_bilingual_support():
    """Test agent language switching"""
    from agents.base import AgentConfig
    from agents.built_in.product_manager import ProductManagerAgent

    # Test English
    config_en = AgentConfig({
        "name": "Product Manager",
        "role": "product_manager",
        "description": "Test",
        "system_prompt": "Test",
        "emoji": "🎯",
        "language": "en"
    })

    mock_llm = MockLLMProvider()
    agent_en = ProductManagerAgent(config_en, mock_llm)

    assert agent_en.config.language == "en"
    assert "Product Manager" in agent_en.config.system_prompt

    # Test Chinese
    config_zh = AgentConfig({
        "name": "产品经理",
        "role": "product_manager",
        "description": "测试",
        "system_prompt": "测试",
        "emoji": "🎯",
        "language": "zh"
    })

    agent_zh = ProductManagerAgent(config_zh, mock_llm)

    assert agent_zh.config.language == "zh"
    assert "产品经理" in agent_zh.config.system_prompt or "产品" in agent_zh.config.system_prompt


@pytest.mark.asyncio
async def test_full_workflow(temp_config, mock_agents):
    """Test complete workflow from start to document export"""
    # Setup
    session_manager = SessionManager(temp_config)
    coordinator = AgentCoordinator(mock_agents)
    doc_generator = DocumentGenerator(temp_config)
    doc_store = DocumentStore(temp_config)

    # Create session
    session = session_manager.create_session("Invoice Management System")

    # User input
    session.add_message(Message(role="user", content="I want to build an invoice management system"))

    # Agent responses
    await coordinator.let_agent_speak("Product Manager", session)
    await coordinator.let_agent_speak("Tech Lead", session)

    # Record decision
    from core.session import Decision
    coordinator.record_decision(
        session,
        "Database",
        "Use PostgreSQL",
        ["Tech Lead", "Product Manager"],
        "Need ACID compliance for financial data"
    )

    # Generate and save documents
    prd = await doc_generator.generate_prd(session)
    tech_spec = await doc_generator.generate_tech_spec(session)
    decisions = await doc_generator.generate_decision_history(session)

    prd_path = doc_store.save_prd("Invoice Management System", prd)
    tech_path = doc_store.save_tech_design("Invoice Management System", tech_spec)
    decision_path = doc_store.save_decision_history("Invoice Management System", decisions)

    # Verify
    assert prd_path.exists()
    assert tech_path.exists()
    assert decision_path.exists()
    assert len(session.messages) >= 2
    assert len(session.decisions) == 1
