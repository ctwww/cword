"""
Document Generator - Generate PRD and technical design documents
"""

from jinja2 import Environment, FileSystemLoader, Template
from pathlib import Path
from typing import Dict, List
from datetime import datetime

from core.session import Session


class DocumentGenerator:
    """Generate documents from session data"""

    def __init__(self, config: dict):
        self.config = config
        self.template_dir = self._get_template_dir()
        self.env = Environment(loader=FileSystemLoader(self.template_dir))

    def _get_template_dir(self) -> Path:
        """Get templates directory"""
        # Check user templates first
        user_templates = Path.home() / ".cword" / "templates"
        if user_templates.exists():
            return str(user_templates)

        # Fall back to project templates
        project_templates = Path.cwd() / "templates"
        if project_templates.exists():
            return str(project_templates)

        # Create default templates
        default_templates = Path(__file__).parent / "templates"
        return str(default_templates)

    async def generate_prd(self, session: Session) -> str:
        """Generate PRD document"""
        try:
            template = self.env.get_template("prd_template.md")
        except:
            # Use built-in template if file doesn't exist
            template = Template(self._get_default_prd_template())

        # Extract data from session
        data = self._extract_prd_data(session)

        # Render template
        content = template.render(**data)

        return content

    async def generate_tech_spec(self, session: Session) -> str:
        """Generate technical design document"""
        try:
            template = self.env.get_template("tech_spec_template.md")
        except:
            template = Template(self._get_default_tech_spec_template())

        # Extract data from session
        data = self._extract_tech_data(session)

        # Render template
        content = template.render(**data)

        return content

    async def generate_decision_history(self, session: Session) -> str:
        """Generate decision history"""
        try:
            template = self.env.get_template("decision_record_template.md")
        except:
            template = Template(self._get_default_decision_template())

        data = {
            "product_name": session.product_name or "Untitled",
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "decisions": session.decisions
        }

        content = template.render(**data)
        return content

    async def generate_realtime_preview(self, session: Session) -> str:
        """Generate real-time document preview"""
        # Simplified preview for display during conversation
        preview = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 Document Preview (PRD - Product Requirements Document)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 1. Product Overview
- Product Name: {session.product_name or '(To be determined)'}
- Stage: {session.current_stage}

## 2. Requirements Analysis
### 2.1 User Scenarios
{self._extract_user_scenarios(session)}

### 2.2 Functional Requirements
{self._extract_features_summary(session)}

## 3. Technical Solution
{self._extract_tech_summary(session)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        return preview

    def _extract_prd_data(self, session: Session) -> Dict:
        """Extract data for PRD template"""
        return {
            "product_name": session.product_name or "Untitled",
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "1.0.0",
            "product_background": self._extract_background(session),
            "target_users": self._extract_users(session),
            "core_value": self._extract_value(session),
            "user_stories": self._extract_stories(session),
            "features": self._extract_features(session),
            "decisions": session.decisions
        }

    def _extract_tech_data(self, session: Session) -> Dict:
        """Extract data for technical design template"""
        tech_decisions = [
            d for d in session.decisions
            if "technical" in d.topic.lower() or "技术" in d.topic or "架构" in d.topic or "方案" in d.topic
        ]

        return {
            "product_name": session.product_name or "Untitled",
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "architecture": self._infer_architecture(session),
            "tech_decisions": tech_decisions,
            "tech_stack": self._infer_tech_stack(session)
        }

    def _extract_user_scenarios(self, session: Session) -> str:
        """Extract user scenarios from conversation"""
        # This would use LLM to extract structured info
        # For now, return placeholder
        return "\n".join([f"- {msg.content[:100]}..." for msg in session.messages[:5]])

    def _extract_features_summary(self, session: Session) -> str:
        """Extract feature summary"""
        if not session.decisions:
            return "To be discussed..."

        features = []
        for decision in session.decisions:
            features.append(f"- {decision.decision}")

        return "\n".join(features)

    def _extract_tech_summary(self, session: Session) -> str:
        """Extract technical summary"""
        tech_decisions = [
            d for d in session.decisions
            if "technical" in d.topic.lower() or "技术" in d.topic
        ]

        if not tech_decisions:
            return "To be discussed..."

        return "\n".join([f"- {d.decision}" for d in tech_decisions])

    def _extract_background(self, session: Session) -> str:
        """Extract product background"""
        return "Product background based on conversation..."

    def _extract_users(self, session: Session) -> List:
        """Extract target users"""
        return [{"name": "User", "description": "Target user to be determined"}]

    def _extract_value(self, session: Session) -> str:
        """Extract core value"""
        return "Core value proposition to be determined..."

    def _extract_stories(self, session: Session) -> List:
        """Extract user stories"""
        return []

    def _extract_features(self, session: Session) -> Dict:
        """Extract features"""
        return {
            "p0": [],
            "p1": [],
            "p2": []
        }

    def _infer_architecture(self, session: Session) -> str:
        """Infer system architecture from decisions"""
        return "System architecture to be designed..."

    def _infer_tech_stack(self, session: Session) -> Dict:
        """Infer technology stack"""
        return {
            "backend": "To be determined",
            "frontend": "To be determined",
            "database": "To be determined"
        }

    def _get_default_prd_template(self) -> str:
        """Get default PRD template"""
        return """# {{ product_name }} Product Requirements Document (PRD)

**Generated**: {{ generated_at }}
**Version**: {{ version }}

---

## 1. Product Overview

### 1.1 Product Background
{{ product_background }}

### 1.2 Target Users
{% for user in target_users %}
- **{{ user.name }}**: {{ user.description }}
{% endfor %}

### 1.3 Core Value
{{ core_value }}

---

## 2. User Stories

{% for story in user_stories %}
### {{ story.title }}
- **User**: {{ story.user }}
- **Goal**: {{ story.goal }}
- **Story**: {{ story.story }}

{% endfor %}

---

## 3. Functional Requirements

### 3.1 Core Features (P0)
{% for feature in features.p0 %}
- {{ feature }}
{% endfor %}

### 3.2 Auxiliary Features (P1)
{% for feature in features.p1 %}
- {{ feature }}
{% endfor %}

---

## Appendix: Decision History

{% for decision in decisions %}
### Decision {{ loop.index }}: {{ decision.topic }}
- **Time**: {{ decision.timestamp }}
- **Decision**: {{ decision.decision }}
- **Participants**: {{ decision.participants | join(', ') }}
- **Reasoning**: {{ decision.reasoning }}

{% endfor %}

---

**End of Document**
"""

    def _get_default_tech_spec_template(self) -> str:
        """Get default technical spec template"""
        return """# {{ product_name }} Technical Design Document

**Generated**: {{ generated_at }}

---

## 1. Technical Solution Overview

### 1.1 Architecture
{{ architecture }}

### 1.2 Technology Stack
- Backend: {{ tech_stack.backend }}
- Frontend: {{ tech_stack.frontend }}
- Database: {{ tech_stack.database }}

---

## 2. System Architecture

(Detailed architecture to be designed)

---

## 3. Data Model

(Data models to be designed)

---

## 4. API Design

(API specifications to be designed)

---

## 5. Deployment

(Deployment strategy to be designed)

---

## Appendix: Technical Decisions

{% for decision in tech_decisions %}
### {{ decision.topic }}
**Decision**: {{ decision.decision }}
**Reasoning**: {{ decision.reasoning }}

{% endfor %}

---

**End of Document**
"""

    def _get_default_decision_template(self) -> str:
        """Get default decision record template"""
        return """# {{ product_name }} Decision History

**Generated**: {{ generated_at }}

---

{% for decision in decisions %}
## Decision {{ loop.index }}: {{ decision.topic }}

**Time**: {{ decision.timestamp.strftime('%Y-%m-%d %H:%M') }}
**Decision**: {{ decision.decision }}
**Participants**: {{ decision.participants | join(', ') }}

### Reasoning
{{ decision.reasoning }}

---

{% endfor %}

**End of Document**
"""
