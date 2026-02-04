"""
Context Manager - Manage conversation context
"""

from typing import List
from datetime import datetime

from core.session import Session, Message


class ContextManager:
    """Manage conversation context for LLM calls"""

    def __init__(self, max_tokens: int = 4000):
        self.max_tokens = max_tokens

    async def prepare_context(
        self,
        session: Session,
        agent_name: str = None
    ) -> List[Message]:
        """Prepare context for LLM call (with compression)"""
        messages = session.messages

        # Strategy 1: If few messages, return all
        if len(messages) <= 10:
            return messages

        # Strategy 2: Generate summary if too many
        if len(messages) > 20:
            summary = await self._generate_summary(session)
            important_messages = self._filter_important(messages[-10:])
            return [summary] + important_messages

        # Strategy 3: Filter important messages
        return self._filter_important(messages)

    async def _generate_summary(self, session: Session) -> Message:
        """Generate conversation summary"""
        # This would use LLM to generate summary
        # For now, return a simple summary
        summary_text = f"""
[Conversation Summary]
Product: {session.product_name or 'Untitled'}
Stage: {session.current_stage}
Messages: {len(session.messages)}
Decisions: {len(session.decisions)}

Key points:
"""

        if session.decisions:
            for decision in session.decisions[-3:]:
                summary_text += f"- {decision.topic}: {decision.decision}\n"

        return Message(
            role="system",
            content=summary_text
        )

    def _filter_important(self, messages: List[Message]) -> List[Message]:
        """Filter important messages"""
        important = []

        for msg in messages:
            # Keep user messages
            if msg.role == "user":
                important.append(msg)
                continue

            # Keep agent messages with questions or decisions
            content_lower = msg.content.lower()
            if any(keyword in content_lower for keyword in
                   ["?", "确认", "confirm", "决定", "decide", "选择", "choose"]):
                important.append(msg)

        return important

    def format_context_for_llm(self, messages: List[Message]) -> str:
        """Format messages for LLM prompt"""
        formatted = []

        for msg in messages:
            if msg.role == "system":
                formatted.append(f"System: {msg.content}")
            elif msg.role == "user":
                formatted.append(f"User: {msg.content}")
            else:
                agent = msg.agent_name or "Agent"
                formatted.append(f"{agent}: {msg.content}")

        return "\n".join(formatted)

    def count_tokens(self, text: str) -> int:
        """Estimate token count (rough approximation)"""
        # Rough estimate: ~4 characters per token
        return len(text) // 4
