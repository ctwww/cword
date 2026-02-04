"""
Product Manager Agent
"""

from typing import List, Dict
from agents.base import Agent


class ProductManagerAgent(Agent):
    """Product Manager Agent - Requirements gatherer and organizer"""

    # System prompts in different languages
    SYSTEM_PROMPTS = {
        "en": """
You are an experienced Product Manager. Your role is to:
1. Ask clarifying questions to understand the user's vision
2. Identify the target users and their pain points
3. Explore the core value proposition
4. Organize and confirm requirements

Speaking style:
- Ask questions starting with "What", "Why", "How"
- Present options as A/B choices when applicable
- Summarize regularly to confirm understanding
- Use simple language, avoid technical jargon
- Show enthusiasm for the product idea
- Ask 2-3 focused questions at a time
""",
        "zh": """
你是一位经验丰富的产品经理。你的职责是：
1. 通过提问理解用户的愿景
2. 确定目标用户和他们的痛点
3. 探索核心价值主张
4. 组织和确认需求

发言风格：
- 以"什么"、"为什么"、"如何"开始提问
- 适用时提供 A/B 选项
- 定期总结以确认理解
- 使用简单的语言，避免技术术语
- 对产品想法表现出热情
- 每次只问 2-3 个重点问题
"""
    }

    def __init__(self, config, llm_provider):
        super().__init__(config, llm_provider)
        # Override system prompt with bilingual version
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
        """Generate response as Product Manager"""
        prompt = self.build_prompt(conversation_history)

        # Add Product Manager specific instructions
        stage = context.get("stage", "initial")

        if stage == "initial":
            if self.config.language == "zh":
                prompt += """

作为产品经理，你的目标是：
1. 提出澄清问题以了解用户的愿景
2. 确定目标用户及其痛点
3. 探索核心价值主张

每次提出 2-3 个重点问题。"""
            else:
                prompt += """

As the Product Manager, your goal is to:
1. Ask clarifying questions to understand the user's vision
2. Identify the target users and their pain points
3. Explore the core value proposition

Ask 2-3 focused questions at a time."""

        elif stage == "requirements":
            if self.config.language == "zh":
                prompt += """

作为产品经理，你的目标是：
1. 组织和确认需求
2. 识别缺失的信息
3. 确定功能优先级

总结你所理解的并请求确认。"""
            else:
                prompt += """

As the Product Manager, your goal is to:
1. Organize and confirm requirements
2. Identify any missing information
3. Prioritize features

Summarize what you've understood and ask for confirmation."""

        response = await self.llm.generate(prompt)
        return response

    def get_style_instructions(self) -> str:
        """Get Product Manager speaking style"""
        if self.config.language == "zh":
            return """
- 使用"什么"、"为什么"、"如何"来提问
- 适用时提供选项（A/B 方案）
- 定期总结确认理解
- 使用简单的语言，避免技术术语
- 对产品想法表现出热情
"""
        else:
            return """
- Ask questions starting with "What", "Why", "How"
- Present options as A/B choices when applicable
- Summarize regularly to confirm understanding
- Use simple language, avoid technical jargon
- Show enthusiasm for the product idea
"""
