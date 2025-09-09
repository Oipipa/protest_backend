from loguru import logger
import sys, os
from app.core.config import settings

def setup_logging():
    logger.remove()
    os.makedirs("logs", exist_ok=True)
    level = "DEBUG" if settings.env != "prod" else "INFO"
    logger.add(sys.stdout, level=level, enqueue=True, backtrace=False, diagnose=False)
    logger.add("logs/app_{time}.log", level=level, rotation="10 MB", retention="7 days", enqueue=True)

setup_logging()
