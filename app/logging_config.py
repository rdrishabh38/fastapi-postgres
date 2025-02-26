from loguru import logger
import sys

# Remove default logger configuration
logger.remove()

# Add a new logger that outputs to stdout with a custom format.
logger.add(
    sys.stdout,
    level="INFO",
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)
