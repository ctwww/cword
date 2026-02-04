"""
CWord Main Entry Point
"""

import asyncio
from pathlib import Path
from rich.console import Console

from cli.interface import CLIInterface
from utils.logger import setup_logger
from utils.config import load_config


def main():
    """Main entry point for CWord"""
    # Setup logging
    setup_logger()

    # Initialize console
    console = Console()

    # Load configuration
    config = load_config()

    # Start CLI interface
    interface = CLIInterface(config)
    interface.run()


if __name__ == "__main__":
    main()
