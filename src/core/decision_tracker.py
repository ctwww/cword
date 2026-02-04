"""
Decision Tracker - Track and manage decisions
"""

from typing import List, Dict
from datetime import datetime

from core.session import Decision, Session


class DecisionTracker:
    """Track decisions made during conversation"""

    def __init__(self):
        self.decisions: Dict[str, Decision] = {}

    def add_decision(self, decision: Decision):
        """Add decision to tracker"""
        self.decisions[decision.id] = decision

    def get_decision(self, decision_id: str) -> Decision:
        """Get decision by ID"""
        return self.decisions.get(decision_id)

    def get_all_decisions(self) -> List[Decision]:
        """Get all decisions"""
        return list(self.decisions.values())

    def get_decisions_by_topic(self, topic: str) -> List[Decision]:
        """Get decisions by topic"""
        return [
            decision for decision in self.decisions.values()
            if topic.lower() in decision.topic.lower()
        ]

    def get_decisions_by_participant(self, participant: str) -> List[Decision]:
        """Get decisions by participant"""
        return [
            decision for decision in self.decisions.values()
            if participant in decision.participants
        ]

    def export_decisions_markdown(self) -> str:
        """Export decisions as markdown"""
        lines = ["# Decision History\n"]

        for decision in self.decisions.values():
            lines.append(f"\n## {decision.id}: {decision.topic}")
            lines.append(f"**Time**: {decision.timestamp.strftime('%Y-%m-%d %H:%M')}")
            lines.append(f"**Decision**: {decision.decision}")
            lines.append(f"**Participants**: {', '.join(decision.participants)}")
            lines.append(f"**Reasoning**: {decision.reasoning}")

        return "\n".join(lines)
