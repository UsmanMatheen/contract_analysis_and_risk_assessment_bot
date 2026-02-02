"""Logging configuration and utilities."""

import sys
from pathlib import Path
from loguru import logger
from config.settings import get_settings


def setup_logging():
    """Configure application logging."""
    settings = get_settings()
    
    # Remove default handler
    logger.remove()
    
    # Console handler with color
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=settings.LOG_LEVEL,
        colorize=True
    )
    
    # File handler
    log_file = Path(settings.LOG_FILE_PATH)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    logger.add(
        log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=settings.LOG_LEVEL,
        rotation="10 MB",
        retention="30 days",
        compression="zip"
    )
    
    logger.info(f"Logging initialized - Level: {settings.LOG_LEVEL}")
    return logger


def get_logger():
    """Get configured logger instance."""
    return logger
