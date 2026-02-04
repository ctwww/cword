"""
Agent Coordinator - Orchestrate multi-agent conversations
"""

from typing import List
from datetime import datetime

from core.session import Session, Message, Decision
from agents.base import Agent
from utils.event_bus import EventBus, Event


class AgentCoordinator:
    """Coordinate agent interactions and conversations"""

    def __init__(self, agents: List[Agent]):
        self.agents = {agent.name: agent for agent in agents}
        self.event_bus = EventBus()
        self.decision_count = 0

    async def let_agent_speak(
        self,
        agent_name: str,
        session: Session
    ) -> str:
        """Let specified agent speak"""
        agent = self.agents.get(agent_name)
        if not agent:
            raise ValueError(f"Agent {agent_name} does not exist")

        # Build context
        context = {
            "stage": session.current_stage,
            "decisions": session.decisions,
            "product_name": session.product_name
        }

        # Generate response
        response = await agent.generate_response(
            session.messages,
            context
        )

        # Record message
        message = Message(
            role="agent",
            agent_name=agent_name,
            content=response
        )
        session.add_message(message)

        # Publish event
        await self.event_bus.publish(Event(
            type="agent_spoke",
            data={
                "agent": agent_name,
                "response": response,
                "timestamp": datetime.now().isoformat()
            }
        ))

        return response

    async def let_all_speak(self, session: Session) -> List[str]:
        """Let all agents speak in turn"""
        responses = []

        for agent_name in self.agents.keys():
            response = await self.let_agent_speak(agent_name, session)
            responses.append(response)

        return responses

    def suggest_agents(self, session: Session) -> List[str]:
        """Intelligently suggest which agents should speak"""
        suggestions = []

        if not session.messages:
            return suggestions

        # Get last message
        last_message = session.messages[-1]
        last_content = last_message.content.lower()

        # Rule 1: If involving sensitive data, suggest Security Expert
        sensitive_keywords = [
            "id card", "password", "bank card", "privacy",
            "身份证", "密码", "银行卡", "隐私"
        ]
        if any(keyword in last_content for keyword in sensitive_keywords):
            if "Security Expert" in self.agents:
                suggestions.append("Security Expert")

        # Rule 2: If early stage, suggest Product Manager
        if session.current_stage == "initial" and len(session.messages) < 5:
            if "Product Manager" in self.agents:
                suggestions.append("Product Manager")

        # Rule 3: If discussing technology, suggest Tech Lead
        tech_keywords = [
            "architecture", "database", "api", "framework", "technical",
            "架构", "数据库", "技术"
        ]
        if any(keyword in last_content for keyword in tech_keywords):
            if "Tech Lead" in self.agents:
                suggestions.append("Tech Lead")

        # Rule 4: If discussing business, suggest Business Consultant
        business_keywords = [
            "business", "market", "customer", "revenue",
            "商业", "市场", "用户", "收入"
        ]
        if any(keyword in last_content for keyword in business_keywords):
            if "Business Consultant" in self.agents:
                suggestions.append("Business Consultant")

        return suggestions

    def should_confirm_decision(self, session: Session) -> bool:
        """Determine if decision should be confirmed"""
        # Confirm every 5 turns
        if len(session.messages) % 5 == 0:
            return True

        if not session.messages:
            return False

        # If decision language detected
        last_message = session.messages[-1]
        last_content = last_message.content.lower()

        decision_keywords = [
            "just use", "choose", "determine", "decide",
            "就用", "选择", "确定", "决定"
        ]

        return any(keyword in last_content for keyword in decision_keywords)

    def record_decision(
        self,
        session: Session,
        topic: str,
        decision: str,
        participants: List[str],
        reasoning: str
    ):
        """Record a decision"""
        self.decision_count += 1

        decision_obj = Decision(
            id=f"decision_{self.decision_count:03d}",
            topic=topic,
            decision=decision,
            participants=participants,
            reasoning=reasoning
        )

        session.add_decision(decision_obj)

        # Publish event
        self.event_bus.publish_sync(Event(
            type="decision_made",
            data={
                "decision_id": decision_obj.id,
                "topic": topic,
                "decision": decision
            }
        ))

        return decision_obj

    def get_agent(self, agent_name: str) -> Agent:
        """Get agent by name"""
        return self.agents.get(agent_name)

    def list_agents(self) -> List[str]:
        """List all available agents"""
        return list(self.agents.keys())

    def add_agent(self, agent: Agent):
        """Add new agent"""
        self.agents[agent.name] = agent

    def remove_agent(self, agent_name: str):
        """Remove agent"""
        if agent_name in self.agents:
            del self.agents[agent_name]
