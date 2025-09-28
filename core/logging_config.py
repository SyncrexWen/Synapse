import logging
import sys
from logging.handlers import RotatingFileHandler
from typing import Literal
from pathlib import Path


def setup_logging(log_path: str, log_level: Literal["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"] = "INFO"):
    '''Config global logging settings'''

    # Make sure log dir exists
    path = Path(log_path)
    path.mkdir(parents=True, exist_ok=True)

    # Get root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # ---- Console Handler ----
    mapper = {
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(mapper[log_level])
    console_formatter = logging.Formatter("%(levelname)s - %(message)s")
    console_handler.setFormatter(console_formatter)

    # ---- File Handler ----
    file_handler = RotatingFileHandler(path, maxBytes=1024*1025*5, backupCount=2, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelnam)s - %(message)s")
    file_handler.setFormatter(file_formatter)

    # Add handlers to root logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)