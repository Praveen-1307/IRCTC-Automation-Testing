"""Custom logger module for IRCTC automation framework."""
import logging
import sys
from utils.config import PROJECT_ROOT


def setup_logger(name: str = "IRCTC_Automation") -> logging.Logger:
    """Set up and configure a structured logger instance.

    Args:
        name: Name of the logger.

    Returns:
        Configured logging.Logger instance.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        log_format = logging.Formatter(
            fmt="%(asctime)s [%(levelname)8s] (%(name)s) %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_format)
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)

        # File handler
        log_file = PROJECT_ROOT / "reports" / "automation.log"
        file_handler = logging.FileHandler(log_file, encoding="utf-8", mode="a")
        file_handler.setFormatter(log_format)
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)

    return logger


logger = setup_logger()
