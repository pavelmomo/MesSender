from config import LOG_LEVEL

LOGGING_CONFIG = {
    "version": 1,
    "formatters": {
        "default_formatter": {
            "format": "%(asctime)s: %(levelname)s: [%(filename)s] %(message)s",
            "datefmt": "%d-%m-%y %I:%M:%S",
        },
        "access": {
            "format": "%(asctime)s: %(levelname)s: %(message)s",
            "datefmt": "%d-%m-%y %I:%M:%S",
        },
    },
    "handlers": {
        "default_handler": {
            "class": "logging.StreamHandler",
            "formatter": "default_formatter",
            "stream": "ext://sys.stdout",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "": {
            "handlers": ["default_handler"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "uvicorn.error": {
            "level": LOG_LEVEL,
            "handlers": ["default_handler"],
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["access"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
}
