"""
Tests for Core Session Management
"""

import pytest
from datetime import datetime
from core.session import Session, Message, Decision, SessionManager


@pytest.fixture
def sample_session():
    """Create a sample session for testing"""
    session = Session(
        session_id="test001",
        product_name="Test Product"
    )

    # Add some messages
    session.add_message(Message(role="user", content="I want to build a todo app"))
    session.add_message(Message(role="agent", agent_name="Product Manager", content="Great idea!"))

    # Add a decision
    decision = Decision(
        id="decision_001",
        topic="Technical Stack",
        decision="Use Python + FastAPI",
        participants=["Tech Lead"],
        reasoning="Simplicity and rapid development"
    )
    session.add_decision(decision)

    return session


def test_session_creation():
    """Test session creation"""
    session = Session(session_id="test001", product_name="Test Product")

    assert session.session_id == "test001"
    assert session.product_name == "Test Product"
    assert len(session.messages) == 0
    assert len(session.decisions) == 0


def test_message_addition(sample_session):
    """Test adding messages to session"""
    initial_count = len(sample_session.messages)

    new_message = Message(role="user", content="New message")
    sample_session.add_message(new_message)

    assert len(sample_session.messages) == initial_count + 1
    assert sample_session.updated_at > sample_session.created_at


def test_decision_addition(sample_session):
    """Test adding decisions to session"""
    initial_count = len(sample_session.decisions)

    new_decision = Decision(
        id="decision_002",
        topic="Database",
        decision="Use PostgreSQL",
        participants=["Tech Lead"],
        reasoning="Need ACID compliance"
    )
    sample_session.add_decision(new_decision)

    assert len(sample_session.decisions) == initial_count + 1


def test_session_serialization(sample_session):
    """Test session to_dict and from_dict"""
    data = sample_session.to_dict()

    assert data["session_id"] == "test001"
    assert data["product_name"] == "Test Product"
    assert len(data["messages"]) == 2
    assert len(data["decisions"]) == 1

    # Test deserialization
    restored_session = Session.from_dict(data)

    assert restored_session.session_id == sample_session.session_id
    assert restored_session.product_name == sample_session.product_name
    assert len(restored_session.messages) == len(sample_session.messages)


def test_context_summary(sample_session):
    """Test context summary generation"""
    summary = sample_session.get_context_summary()

    assert "todo app" in summary
    assert "Great idea" in summary
