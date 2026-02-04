# {{ product_name }} Technical Design Document

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
