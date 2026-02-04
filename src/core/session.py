"""
Session Management - Manage conversation sessions
"""

import uuid
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from pathlib import Path
import json

from storage.session_store import SessionStore


@dataclass
class Message:
    """Single message in conversation"""
    role: str  # "user" or "agent"
    agent_name: Optional[str] = None
    content: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "role": self.role,
            "agent_name": self.agent_name,
            "content": self.content,
            "timestamp": self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Message":
        return cls(
            role=data["role"],
            agent_name=data.get("agent_name"),
            content=data["content"],
            timestamp=datetime.fromisoformat(data["timestamp"])
        )


@dataclass
class Decision:
    """Decision record"""
    id: str
    topic: str
    decision: str
    participants: List[str]
    reasoning: str
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "topic": self.topic,
            "decision": self.decision,
            "participants": self.participants,
            "reasoning": self.reasoning,
            "timestamp": self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Decision":
        return cls(
            id=data["id"],
            topic=data["topic"],
            decision=data["decision"],
            participants=data["participants"],
            reasoning=data["reasoning"],
            timestamp=datetime.fromisoformat(data["timestamp"])
        )


@dataclass
class Session:
    """Conversation session"""
    session_id: str
    product_name: str = ""
    messages: List[Message] = field(default_factory=list)
    decisions: List[Decision] = field(default_factory=list)
    current_stage: str = "initial"  # initial, requirements, design, complete
    metadata: Dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def add_message(self, message: Message):
        """Add message to session"""
        self.messages.append(message)
        self.updated_at = datetime.now()

    def add_decision(self, decision: Decision):
        """Add decision to session"""
        self.decisions.append(decision)
        self.updated_at = datetime.now()

    def get_context_summary(self, max_tokens: int = 4000) -> str:
        """Get context summary for LLM calls"""
        # Implement context compression logic
        if len(self.messages) <= 10:
            return self._format_messages(self.messages)

        # If too many messages, return recent ones
        recent_messages = self.messages[-10:]
        return self._format_messages(recent_messages)

    def _format_messages(self, messages: List[Message]) -> str:
        """Format messages to string"""
        formatted = []
        for msg in messages:
            if msg.role == "user":
                formatted.append(f"User: {msg.content}")
            else:
                formatted.append(f"{msg.agent_name}: {msg.content}")
        return "\n".join(formatted)

    def to_dict(self) -> dict:
        """Convert session to dictionary"""
        return {
            "session_id": self.session_id,
            "product_name": self.product_name,
            "messages": [msg.to_dict() for msg in self.messages],
            "decisions": [dec.to_dict() for dec in self.decisions],
            "current_stage": self.current_stage,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Session":
        """Create session from dictionary"""
        return cls(
            session_id=data["session_id"],
            product_name=data.get("product_name", ""),
            messages=[Message.from_dict(m) for m in data.get("messages", [])],
            decisions=[Decision.from_dict(d) for d in data.get("decisions", [])],
            current_stage=data.get("current_stage", "initial"),
            metadata=data.get("metadata", {}),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"])
        )


class SessionManager:
    """Manage conversation sessions"""

    def __init__(self, config: dict):
        self.config = config
        self.store = SessionStore(config)
        self.current_session: Optional[Session] = None

    def create_session(self, product_name: str = "") -> Session:
        """Create new session"""
        session_id = str(uuid.uuid4())[:8]
        session = Session(
            session_id=session_id,
            product_name=product_name
        )
        self.current_session = session
        return session

    def get_session(self, session_id: str) -> Optional[Session]:
        """Get session by ID"""
        return self.store.load_session(session_id)

    def get_current_session(self) -> Optional[Session]:
        """Get current active session"""
        if not self.current_session:
            self.current_session = self.create_session()
        return self.current_session

    def save_session(self, session_id: str):
        """Save session to storage"""
        if self.current_session:
            self.store.save_session(self.current_session)

    def update_session(self, session: Session):
        """Update session"""
        session.updated_at = datetime.now()
        if session.session_id == self.current_session.session_id:
            self.current_session = session
        self.store.save_session(session)

    def delete_session(self, session_id: str):
        """Delete session"""
        self.store.delete_session(session_id)
        if self.current_session and self.current_session.session_id == session_id:
            self.current_session = None

    def list_sessions(self) -> List[Session]:
        """List all sessions"""
        return self.store.list_sessions()

    def set_current_session(self, session: Session):
        """Set current active session"""
        self.current_session = session
