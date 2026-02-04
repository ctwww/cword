# {{ product_name }} Product Requirements Document (PRD)

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
