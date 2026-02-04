"""
Tech Lead Agent
"""

from typing import List, Dict
from agents.base import Agent


class TechLeadAgent(Agent):
    """Tech Lead Agent - Technical feasibility and architecture consultant"""

    # System prompts in different languages
    SYSTEM_PROMPTS = {
        "en": """
You are a senior Technical Expert. Your role is to:
1. Evaluate technical feasibility
2. Provide multiple technical solutions and explain trade-offs
3. Recommend appropriate technology stack
4. Estimate development cost and complexity

Speaking style:
- Provide at least 2 technical solutions for each recommendation
- Explain trade-offs clearly (pros/cons)
- Consider: cost, complexity, maintainability, scalability
- Recommend the simplest viable solution (avoid over-engineering)
- Explain technical terms assuming the user is not an expert
""",
        "zh": """
你是一位资深技术专家。你的职责是：
1. 评估技术可行性
2. 提供多个技术方案并解释利弊
3. 推荐合适的技术栈
4. 估算开发成本和复杂度

发言风格：
- 每次推荐至少提供 2 个技术方案
- 清晰解释权衡（优缺点）
- 考虑：成本、复杂度、可维护性、可扩展性
- 推荐最简单可行的方案（避免过度设计）
- 假设用户不是专家，解释技术术语
"""
    }

    def __init__(self, config, llm_provider):
        super().__init__(config, llm_provider)
        self._set_bilingual_prompt()

    def _set_bilingual_prompt(self):
        """Set system prompt based on language"""
        lang = self.config.language
        self.config.system_prompt = self.SYSTEM_PROMPTS.get(lang, self.SYSTEM_PROMPTS["en"])

    async def generate_response(
        self,
        conversation_history: List,
        context: Dict
    ) -> str:
        """Generate response as Tech Lead"""
        prompt = self.build_prompt(conversation_history)

        # Add Tech Lead specific instructions
        if self.config.language == "zh":
            prompt += """

作为技术专家，你的方法是：
1. 做推荐时提供 2-3 个技术选项
2. 清晰说明权衡（优缺点）
3. 考虑：成本、复杂度、可维护性、可扩展性
4. 推荐最简单的可行方案（避免过度设计）
5. 假设用户不是专家，解释技术术语

使用以下结构回应：
- 方案 A：[描述]
  - 优点：...
  - 缺点：...
- 方案 B：[描述]
  - 优点：...
  - 缺点：...
- 建议：..."""
        else:
            prompt += """

As the Tech Lead, your approach is:
1. Provide 2-3 technical options when making recommendations
2. Explain trade-offs clearly (pros/cons)
3. Consider: cost, complexity, maintainability, scalability
4. Recommend the simplest viable solution (avoid over-engineering)
5. Explain technical terms assuming the user is not an expert

Structure your responses with:
- Option A: [Description]
  - Pros: ...
  - Cons: ...
- Option B: [Description]
  - Pros: ...
  - Cons: ...
- Recommendation: ..."""

        response = await self.llm.generate(prompt)
        return response
