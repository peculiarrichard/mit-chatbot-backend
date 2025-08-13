import logging
import sys
from pythonjsonlogger import jsonlogger
from src.config import settings
from src.constants import Environment


def setup_logging():
    """
    Configures the application's logger.
    - For development: Human-readable format.
    - For production/staging: JSON format for structured logging.
    """
    logger = logging.getLogger()
    logger.setLevel(settings.LOG_LEVEL.upper())

    # Remove any existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)

    if settings.ENVIRONMENT == Environment.DEVELOPMENT:
        # Human-readable format for local development
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    else:
        # Structured JSON format for production
        formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(name)s %(levelname)s %(message)s"
        )

    handler.setFormatter(formatter)
    logger.addHandler(handler)