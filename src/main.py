"""
CWord Main Entry Point
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent
sys.path.insert(0, str(src_dir))

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

import asyncio
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
