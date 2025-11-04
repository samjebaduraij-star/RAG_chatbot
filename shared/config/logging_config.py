# logging_config.py
# Description: Logger setup for entire application
# Dependencies: logging, os
# Author: AI Generated Code
# Created: August 15, 2025

import logging
import os

def setup_logging():
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    log_format = "[%(asctime)s] %(levelname)s %(name)s: %(message)s"
    logging.basicConfig(
        format=log_format,
        level=getattr(logging, log_level, logging.INFO),
        handlers=[logging.StreamHandler(), logging.FileHandler("logs/app.log", encoding="utf-8")]
    )