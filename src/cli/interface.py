"""
CLI Interface - Main User Interaction Handler
"""

import asyncio
import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import questionary

from core.session import SessionManager
from core.coordinator import AgentCoordinator
from agents.factory import AgentFactory
from documents.generator import DocumentGenerator
from storage.document_store import DocumentStore


class CLIInterface:
    """Command Line Interface for CWord"""

    def __init__(self, config: dict):
        self.config = config
        self.console = Console()
        self.session_manager = SessionManager(config)
        self.agents = []
        self.coordinator = None
        self.document_generator = DocumentGenerator(config)
        self.document_store = DocumentStore(config)
        self.language = self._get_language()

    def _get_language(self) -> str:
        """Get language setting from environment or config"""
        # Check environment variable first
        env_lang = os.getenv("CWORD_LANGUAGE", "")
        if env_lang in ["zh", "en"]:
            return env_lang

        # Check config
        if "default_language" in self.config:
            return self.config["default_language"]

        # Default to Chinese
        return "zh"

    def run(self):
        """Run the CLI interface"""
        self._show_welcome()
        self._initialize_agents()

        # Main loop
        while True:
            user_input = self._get_user_input()

            if user_input.lower() in ['/exit', 'quit', 'exit']:
                self._show_goodbye()
                break
            elif user_input.lower() in ['/help', 'h']:
                self._show_help()
            elif user_input.lower() in ['/agents', 'a']:
                self._list_agents()
            elif user_input.lower() in ['/preview', 'p']:
                self._show_preview()
            elif user_input.lower() in ['/save', 's']:
                self._save_session()
            elif user_input.lower() in ['/export', 'e']:
                self._export_documents()
            else:
                # Process user message
                asyncio.run(self._process_message(user_input))

    def _show_welcome(self):
        """Show welcome screen"""
        if self.language == "zh":
            welcome_text = """
  🎯 CWord - 您的虚拟产品团队
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
版本: 1.0.0

当前团队成员: 产品经理, 技术专家, 业务顾问, 安全专家

💡 提示:
  - 输入 'help' 查看帮助
  - 输入 'agents' 查看所有可用角色
  - 输入 'preview' 查看当前文档进度
  - 输入 'save' 保存当前会话
  - 输入 'exit' 退出程序

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            """
        else:
            welcome_text = """
  🎯 CWord - Your Virtual Product Team
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Version: 1.0.0

Current Team: Product Manager, Tech Lead, Business Consultant, Security Expert

💡 Tips:
  - Enter 'help' to view help
  - Enter 'agents' to view all available roles
  - Enter 'preview' to view current document progress
  - Enter 'save' to save current session
  - Enter 'exit' to quit

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            """

        self.console.print(Panel(welcome_text, style="bold blue"))

    def _initialize_agents(self):
        """Initialize all agents from configuration"""
        agent_factory = AgentFactory(self.config)
        self.agents = agent_factory.create_all_agents()
        self.coordinator = AgentCoordinator(self.agents)

        self.console.print("✅ Agents initialized successfully!", style="green")

    def _get_user_input(self) -> str:
        """Get user input"""
        if self.language == "zh":
            prompt = "💬 请告诉我您想做什么产品？"
        else:
            prompt = "💬 Tell me about your product idea"

        return questionary.text(
            prompt,
            multiline=False
        ).ask()

    async def _process_message(self, message: str):
        """Process user message"""
        # Create or get session
        session = self.session_manager.get_current_session()

        # Add user message to session
        from core.session import Message
        user_msg = Message(role="user", content=message)
        session.add_message(user_msg)

        # Suggest agents
        suggestions = self.coordinator.suggest_agents(session)

        if suggestions:
            if self.language == "zh":
                self.console.print(f"\n⚠️  建议: {', '.join(suggestions)} 可能想要发言\n")
            else:
                self.console.print(f"\n⚠️  Suggestion: {', '.join(suggestions)} may want to speak\n")

        # Let user choose which agent should speak
        agent_name = self._select_agent()

        if agent_name and agent_name != "skip":
            if agent_name == "all":
                # Let all agents speak
                for agent in self.agents:
                    response = await self.coordinator.let_agent_speak(agent.name, session)
                    self._display_agent_response(agent.name, response)
            else:
                # Get agent response
                response = await self.coordinator.let_agent_speak(agent_name, session)

                # Display response
                self._display_agent_response(agent_name, response)

    def _select_agent(self) -> str:
        """Let user select which agent should speak"""
        if self.language == "zh":
            choices = [
                {"name": f"🎯 产品经理     - 需求梳理者", "value": "产品经理"},
                {"name": f"🔧 技术专家     - 技术顾问", "value": "技术专家"},
                {"name": f"💼 业务顾问     - 商业分析师", "value": "业务顾问"},
                {"name": f"🛡️  安全专家     - 风险识别者", "value": "安全专家"},
                {"name": f"📢 全体发言     - 所有人依次发言", "value": "all"},
                {"name": f"⏭️  跳过，我继续说", "value": "skip"},
            ]
            prompt = "🎤 谁想发言？"
        else:
            choices = [
                {"name": f"🎯 Product Manager     - Requirements Organizer", "value": "Product Manager"},
                {"name": f"🔧 Tech Lead           - Technical Consultant", "value": "Tech Lead"},
                {"name": f"💼 Business Consultant - Business Analyst", "value": "Business Consultant"},
                {"name": f"🛡️  Security Expert     - Risk Identifier", "value": "Security Expert"},
                {"name": f"📢 All Speak           - Everyone speaks in turn", "value": "all"},
                {"name": f"⏭️  Skip, I'll continue", "value": "skip"},
            ]
            prompt = "🎤 Who wants to speak?"

        choice = questionary.select(
            prompt,
            choices=choices
        ).ask()

        return choice

    def _display_agent_response(self, agent_name: str, response: str):
        """Display agent response"""
        emoji_map = {
            "Product Manager": "🎯",
            "Tech Lead": "🔧",
            "Business Consultant": "💼",
            "Security Expert": "🛡️",
            "产品经理": "🎯",
            "技术专家": "🔧",
            "业务顾问": "💼",
            "安全专家": "🛡️"
        }

        emoji = emoji_map.get(agent_name, "🤖")

        self.console.print(f"\n{emoji} {agent_name}:\n")
        self.console.print(Panel(response, style="cyan"))
        self.console.print("")

    def _list_agents(self):
        """List all available agents"""
        if self.language == "zh":
            table = Table(title="可用智能体")
        else:
            table = Table(title="Available Agents")

        table.add_column("名称" if self.language == "zh" else "Name", style="cyan")
        table.add_column("角色" if self.language == "zh" else "Role", style="magenta")
        table.add_column("描述" if self.language == "zh" else "Description", style="white")

        for agent in self.agents:
            table.add_row(
                agent.name,
                agent.role,
                agent.config.description[:50] + "..."
            )

        self.console.print(table)

    def _show_preview(self):
        """Show document preview"""
        session = self.session_manager.get_current_session()
        if not session or not session.messages:
            if self.language == "zh":
                self.console.print("❌ 还没有对话内容，请先开始聊天！", style="red")
            else:
                self.console.print("❌ No conversation yet. Start chatting first!", style="red")
            return

        # Generate preview
        preview = asyncio.run(self.document_generator.generate_realtime_preview(session))
        title = "📄 文档预览" if self.language == "zh" else "📄 Document Preview"
        self.console.print(Panel(preview, title=title, style="cyan"))

    def _export_documents(self):
        """Export all documents"""
        session = self.session_manager.get_current_session()
        if not session or not session.messages:
            if self.language == "zh":
                self.console.print("❌ 没有可导出的内容，请先开始聊天！", style="red")
            else:
                self.console.print("❌ No conversation to export. Start chatting first!", style="red")
            return

        if self.language == "zh":
            self.console.print("\n📄 正在生成文档...", style="yellow")
        else:
            self.console.print("\n📄 Generating documents...", style="yellow")

        # Generate documents
        prd = asyncio.run(self.document_generator.generate_prd(session))
        tech_spec = asyncio.run(self.document_generator.generate_tech_spec(session))
        decisions = asyncio.run(self.document_generator.generate_decision_history(session))

        # Save documents
        product_name = session.product_name or ("未命名产品" if self.language == "zh" else "Untitled_Product")
        prd_path = self.document_store.save_prd(product_name, prd)
        tech_path = self.document_store.save_tech_design(product_name, tech_spec)
        decision_path = self.document_store.save_decision_history(product_name, decisions)

        if self.language == "zh":
            self.console.print(f"\n✅ 文档导出成功！", style="green")
            self.console.print(f"  - 需求文档: {prd_path}")
            self.console.print(f"  - 技术设计: {tech_path}")
            self.console.print(f"  - 决策记录: {decision_path}")
        else:
            self.console.print(f"\n✅ Documents exported successfully!", style="green")
            self.console.print(f"  - PRD: {prd_path}")
            self.console.print(f"  - Tech Spec: {tech_path}")
            self.console.print(f"  - Decision History: {decision_path}")

    def _save_session(self):
        """Save current session"""
        session = self.session_manager.get_current_session()
        if session:
            self.session_manager.save_session(session.session_id)
            if self.language == "zh":
                self.console.print("✅ 会话已保存！", style="green")
            else:
                self.console.print("✅ Session saved!", style="green")
        else:
            if self.language == "zh":
                self.console.print("❌ 没有活动会话可保存", style="red")
            else:
                self.console.print("❌ No active session to save", style="red")

    def _show_help(self):
        """Show help information"""
        if self.language == "zh":
            help_text = """
可用命令:
  /help, h          - 显示此帮助信息
  /agents, a        - 列出所有可用智能体
  /preview, p       - 预览当前文档进度
  /export, e        - 导出需求文档、技术设计和决策记录
  /save, s          - 保存当前会话
  /exit, quit       - 退出 CWord

提示:
  - 具体描述您的产品想法
  - 让不同的智能体发言以获得多角度的建议
  - 定期使用 /preview 跟踪进度
  - 使用 /export 生成最终文档
            """
            title = "帮助"
        else:
            help_text = """
Available Commands:
  /help, h          - Show this help message
  /agents, a        - List all available agents
  /preview, p       - Preview current document progress
  /export, e        - Export PRD, Tech Spec, and Decision History
  /save, s          - Save current session
  /exit, quit       - Exit CWord

Tips:
  - Be specific about your product idea
  - Let different agents speak to get diverse perspectives
  - Use /preview regularly to track progress
  - Use /export to generate final documents
            """
            title = "Help"

        self.console.print(Panel(help_text, title=title, style="blue"))

    def _show_goodbye(self):
        """Show goodbye message"""
        if self.language == "zh":
            goodbye = """
感谢使用 CWord！🎉

您的文档已保存到: ~/.cword/output/

继续构建精彩的产品！🚀
            """
        else:
            goodbye = """
Thank you for using CWord! 🎉

Your documents have been saved to: ~/.cword/output/

Keep building amazing products! 🚀
            """

        self.console.print(Panel(goodbye, style="bold green"))
