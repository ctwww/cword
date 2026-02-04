"""
Output Formatters - Format and Display Output
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown


class OutputFormatter:
    """Format and display various types of output"""

    def __init__(self):
        self.console = Console()

    def print_agent_message(self, agent_name: str, message: str, emoji: str = "🤖"):
        """Print agent message with formatting"""
        self.console.print(f"\n{emoji} {agent_name}:\n")
        self.console.print(Panel(message, style="cyan"))
        self.console.print("")

    def print_system_message(self, message: str, style: str = "yellow"):
        """Print system message"""
        self.console.print(f"⚠️  {message}", style=style)

    def print_success(self, message: str):
        """Print success message"""
        self.console.print(f"✅ {message}", style="bold green")

    def print_error(self, message: str):
        """Print error message"""
        self.console.print(f"❌ {message}", style="bold red")

    def print_info(self, message: str):
        """Print info message"""
        self.console.print(f"ℹ️  {message}", style="blue")

    def print_decision(self, decision_id: str, topic: str, decision: str):
        """Print decision record"""
        decision_text = f"""
[Decision {decision_id}] {topic}
Decision: {decision}
"""
        self.console.print(Panel(decision_text, style="green"))

    def print_progress(self, message: str):
        """Print progress indicator"""
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        )

    def print_markdown(self, content: str):
        """Print markdown content"""
        markdown = Markdown(content)
        self.console.print(markdown)

    def print_table(self, title: str, columns: list, rows: list):
        """Print table"""
        table = Table(title=title)
        for column in columns:
            table.add_column(column[0], style=column[1])

        for row in rows:
            table.add_row(*row)

        self.console.print(table)

    def print_preview(self, content: str, title: str = "Document Preview"):
        """Print document preview"""
        self.console.print(f"\n{'━' * 60}")
        self.console.print(f"📄 {title}")
        self.console.print(f"{'━' * 60}\n")
        self.console.print(Markdown(content))
        self.console.print(f"\n{'━' * 60}")
