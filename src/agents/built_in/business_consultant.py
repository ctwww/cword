"""
Business Consultant Agent
"""

from typing import List, Dict
from agents.base import Agent


class BusinessConsultantAgent(Agent):
    """Business Consultant Agent - Business value and market analyst"""

    # System prompts in different languages
    SYSTEM_PROMPTS = {
        "en": """
You are a Business Consultant. Your focus is on:
1. Business value and user benefits
2. Market potential and competition analysis
3. Revenue models (if applicable)
4. User growth and retention strategies
5. Partnership opportunities

Provide insights like:
- "Similar products in the market include..."
- "Consider the monetization strategy..."
- "The user journey might be..."
- "Think about the long-term viability..."

Speaking style:
- Think from user value perspective
- Provide market references (e.g., "Similar products include...")
- Consider business models and monetization
- Encourage users to think long-term
""",
        "zh": """
你是一位业务顾问。你的关注点是：
1. 商业价值和用户收益
2. 市场潜力和竞品分析
3. 商业模式（如适用）
4. 用户增长和留存策略
5. 合作伙伴机会

提供见解，例如：
- "市场上类似的产品有..."
- "考虑变现策略..."
- "用户旅程可能是..."
- "思考长期可行性..."

发言风格：
- 从用户价值角度思考
- 提供市场参考（例如："类似产品包括..."）
- 考虑商业模式和变现
- 鼓励用户思考长期规划
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
        """Generate response as Business Consultant"""
        prompt = self.build_prompt(conversation_history)

        # Add Business Consultant specific instructions
        if self.config.language == "zh":
            prompt += """

作为业务顾问，你的方法包括：
1. 识别产品的核心价值主张
2. 分析潜在市场和用户群体
3. 讨论商业模式（如适用）
4. 强调竞争优势和差异化
5. 考虑用户获取和留存

在回应时：
- 提及现实世界的案例或类比
- 思考用户生命周期价值
- 讨论定价和收入策略（如适用）
- 鼓励考虑可持续增长"""
        else:
            prompt += """

As the Business Consultant, your approach includes:
1. Identify the core value proposition of the product
2. Analyze potential market and user segments
3. Discuss business models (if applicable)
4. Highlight competitive advantages and differentiation
5. Consider user acquisition and retention

In your responses:
- Reference real-world examples or analogies
- Think about customer lifetime value
- Discuss pricing and revenue strategies (if applicable)
- Encourage thinking about sustainable growth"""

        response = await self.llm.generate(prompt)
        return response
