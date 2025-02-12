import os
import sys
import logging
import json


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage()
        }
        return json.dumps(log)


def setup_logging():
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "DEBUG")
    LOG_FORMAT = os.environ.get("LOG_FORMAT", "TEXT")

    logger = logging.getLogger("myapp")
    logger.setLevel(LOG_LEVEL)
    stdout_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler("log.txt")

    if LOG_FORMAT == "JSON":
        formatter = JsonFormatter()
    else:
        formatter = logging.Formatter(
            "%(asctime)s:%(name)s:%(levelname)s:%(module)s:%(lineno)d:%(funcName)s:%(message)s")

    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
