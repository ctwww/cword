# {{ product_name }} Decision History

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
