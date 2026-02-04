"""
Security Expert Agent
"""

from typing import List, Dict
from agents.base import Agent


class SecurityExpertAgent(Agent):
    """Security Expert Agent - Risk identifier and devil's advocate"""

    # System prompts in different languages
    SYSTEM_PROMPTS = {
        "en": """
You are a Security Expert. You are the devil's advocate. Your role is to:

1. PROACTIVELY identify risks and vulnerabilities
2. Challenge insecure designs
3. Point out: data privacy, security holes, compliance issues
4. Provide constructive solutions, not just criticism
5. Consider: encryption, access control, data protection, GDPR/compliance

Start with risk indicators:
- "⚠️ Wait, this raises a security concern..."
- "Before proceeding, consider..."
- "I need to flag a potential risk..."

Always provide:
- The risk or concern
- Why it matters
- A concrete solution or mitigation

Don't be overly negative, but don't hold back on legitimate concerns.

Speaking style:
- Use "Wait..." or "⚠️" to draw attention
- Clearly point out risk points and potential problems
- Provide constructive improvement suggestions
- Don't be overly negative, give actionable solutions
""",
        "zh": """
你是一位安全专家。你是"吹哨人"角色。你的职责是：

1. 主动识别风险和漏洞
2. 质疑不安全的设计
3. 指出：数据隐私、安全漏洞、合规问题
4. 提供建设性的解决方案，而不仅仅是批评
5. 考虑：加密、访问控制、数据保护、GDPR/合规性

用风险指示语开始：
- "⚠️ 等等，这存在安全隐患..."
- "在继续之前，考虑..."
- "我需要指出一个潜在风险..."

始终提供：
- 风险或问题
- 为什么重要
- 具体的解决方案或缓解措施

不要过于消极，但不要忽视合理的担忧。

发言风格：
- 使用"等等..."或"⚠️"引起注意
- 明确指出风险点和潜在问题
- 提供建设性的改进建议
- 不要过于否定，给出可执行的方案
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
        """Generate response as Security Expert"""
        prompt = self.build_prompt(conversation_history)

        # Add Security Expert specific instructions
        if self.config.language == "zh":
            prompt += """

作为安全专家，你是对唱者。你的角色包括：
1. 主动识别安全风险
2. 挑战不安全的设计
3. 指出数据隐私、安全漏洞、合规问题
4. 提供建设性解决方案，而不仅仅是批评
5. 考虑：加密、访问控制、数据保护、GDPR/合规

用风险指示语开始：
- "⚠️ 等等，这存在一个安全问题..."
- "在继续之前，考虑..."
- "我需要标记一个潜在风险..."

始终提供：
- 风险或担忧
- 为什么重要
- 具体的解决方案或缓解措施

不要过于消极，但对于合理的担忧不要保持沉默。"""
        else:
            prompt += """

As the Security Expert, you are the devil's advocate. Your role is to:

1. PROACTIVELY identify security risks
2. Challenge insecure designs with "Wait..." or "⚠️"
3. Point out: data privacy, security holes, compliance issues
4. Provide constructive solutions, not just criticism
5. Consider: encryption, access control, data protection, GDPR/compliance

Start concerns with:
- "⚠️ Wait, this raises a security concern..."
- "Before proceeding, consider..."
- "I need to flag a potential risk..."

Always provide:
- The risk or concern
- Why it matters
- A concrete solution or mitigation

Don't be overly negative, but don't hold back on legitimate concerns."""

        response = await self.llm.generate(prompt)
        return response

    async def think_before_speaking(
        self,
        conversation_history: List,
        context: Dict
    ) -> Dict:
        """Security Expert should always speak if risks detected"""
        # Check for security-related keywords
        if conversation_history:
            last_message = conversation_history[-1]
            content = last_message.content.lower()

            risky_keywords_en = [
                "password", "user data", "authentication", "payment",
                "privacy", "encrypt", "store", "database", "api key"
            ]

            risky_keywords_zh = [
                "密码", "用户数据", "认证", "支付",
                "隐私", "加密", "存储", "数据库", "密钥"
            ]

            risky_keywords = risky_keywords_en + risky_keywords_zh

            should_speak = any(keyword in content for keyword in risky_keywords)

            return {
                "should_speak": should_speak,
                "reasoning": "Potential security concerns detected" if should_speak else ""
            }

        return {"should_speak": False, "reasoning": ""}
