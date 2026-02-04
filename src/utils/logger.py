"""
Logger Configuration
"""

import sys
from pathlib import Path
from loguru import logger


def setup_logger(log_level: str = "INFO"):
    """Setup loguru logger"""

    # Remove default handler
    logger.remove()

    # Create logs directory
    log_dir = Path.home() / ".cword" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    # Add console handler with colors
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        level=log_level,
        colorize=True
    )

    # Add file handler for all logs
    logger.add(
        log_dir / "cword_{time:YYYY-MM-DD}.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        level="DEBUG",
        rotation="10 MB",
        retention="30 days",
        compression="zip"
    )

    # Add file handler for errors only
    logger.add(
        log_dir / "errors.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        level="ERROR",
        rotation="10 MB",
        retention="90 days"
    )

    logger.info("CWord logger initialized")
    return logger


def get_logger(name: str = None):
    """Get logger instance"""
    if name:
        return logger.bind(name=name)
    return logger
