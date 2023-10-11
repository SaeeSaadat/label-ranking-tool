import logging
import sys
from logging.handlers import TimedRotatingFileHandler


def setup_logging():
    LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s"
    LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        datefmt=LOG_DATE_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),
            TimedRotatingFileHandler(
                "logs/app.log",
                when="H",
                interval=1,
                backupCount=72,
                encoding="utf-8",
            ),
        ],
    )

    # Disable uvicorn's default logger
    loggers = ["uvicorn", "uvicorn.error", "fastapi"]
    for logger_name in loggers:
        logger = logging.getLogger(logger_name)
        logger.handlers = []
        logger.propagate = False
