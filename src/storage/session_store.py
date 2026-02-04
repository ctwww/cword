"""
Session Store - Persist and retrieve sessions
"""

import json
from pathlib import Path
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from core.session import Session


class SessionStore:
    """Store sessions to file system"""

    def __init__(self, config: dict):
        self.config = config
        self.sessions_dir = self._get_sessions_dir()

    def _get_sessions_dir(self) -> Path:
        """Get sessions directory path"""
        sessions_path = self.config.get("directories", {}).get("sessions", "~/.cword/sessions")
        path = Path(sessions_path).expanduser()
        path.mkdir(parents=True, exist_ok=True)
        return path

    def save_session(self, session):
        """Save session to file"""
        session_file = self.sessions_dir / f"{session.session_id}.json"

        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session.to_dict(), f, indent=2, ensure_ascii=False)

    def load_session(self, session_id: str):
        """Load session from file"""
        from core.session import Session

        session_file = self.sessions_dir / f"{session_id}.json"

        if not session_file.exists():
            return None

        with open(session_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return Session.from_dict(data)

    def delete_session(self, session_id: str):
        """Delete session file"""
        session_file = self.sessions_dir / f"{session_id}.json"

        if session_file.exists():
            session_file.unlink()

    def list_sessions(self):
        """List all sessions"""
        from core.session import Session

        sessions = []

        for session_file in self.sessions_dir.glob("*.json"):
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    sessions.append(Session.from_dict(data))
            except Exception as e:
                print(f"Warning: Failed to load session from {session_file}: {e}")

        # Sort by updated time
        sessions.sort(key=lambda s: s.updated_at, reverse=True)

        return sessions

    def exists(self, session_id: str) -> bool:
        """Check if session exists"""
        session_file = self.sessions_dir / f"{session_id}.json"
        return session_file.exists()
