import logging
import logging.config
from logging import Logger

from typing import Any

__LOGGING_CONFIG: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "style": "{",
            "format": "{levelname:<9} {message}",
        },
        "uvicorn": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(message)s",
            "use_colors": None,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(levelprefix)s %(client_addr)s "%(request_line)s" %(status_code)s',
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "uvicorn": {
            "formatter": "uvicorn",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "app": {"handlers": ["default"], "level": "DEBUG", "propagate": False},
        "uvicorn": {"handlers": ["uvicorn"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
    },
    "root": {"handlers": ["default"], "level": "INFO", "propagate": False},
}

logging.basicConfig()
logging.config.dictConfig(__LOGGING_CONFIG)

def get_logger(classname: str) -> Logger:
    return logging.getLogger(f"app.{classname}")