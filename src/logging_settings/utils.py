from logging import getLogger
from logging.config import dictConfig
from typing import Any
from warnings import warn

from logging_settings.settings import LoggingSettings

__all__ = ("setup_logging", "make_logging_settings")

logger = getLogger(__name__)


def setup_logging(logging_settings: LoggingSettings) -> None:
    if logging_settings.coloring_output:
        from colorama import init

        init(autoreset=True)

    handlers = get_handlers(logging_settings)
    formatters = get_formatters(logging_settings)
    dict_config = get_dict_config(logging_settings, handlers, formatters)

    dictConfig(dict_config)

    if logging_settings.loglevel == "DEBUG":
        msg = "Debug mode on"
        logger.warning(msg)
        warn(UserWarning(msg))


def make_logging_settings(**kwargs) -> LoggingSettings:
    return LoggingSettings(**kwargs)


def get_formatters(logging_settings: LoggingSettings) -> dict:
    return {
        "base": {
            "format": logging_settings.log_format,
            "datefmt": logging_settings.log_datetime_format,
        },
        "colour": {
            "()": "logging_settings.formatters.ColourFormatter",
            "fmt": logging_settings.log_format,
            "datefmt": logging_settings.log_datetime_format,
        },
    }


def get_handlers(logging_settings: LoggingSettings) -> dict:
    return {
        "console": {
            "class": "logging.StreamHandler",
            "level": logging_settings.loglevel,
            "formatter": "colour" if logging_settings.coloring_output else "base",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": logging_settings.loglevel,
            "mode": "a",
            "formatter": "base",
            "maxBytes": logging_settings.max_bytes,
            "backupCount": logging_settings.backup_count,
            "filename": logging_settings.filename,
            "encoding": logging_settings.encoding,
        },
    }


def get_dict_config(
    logging_settings: LoggingSettings,
    handlers: dict[str, str],
    formatters: dict[str, str],
) -> dict[str, Any]:
    handlers_names = [name for name in handlers.keys()]

    if not logging_settings.rotating_file_handler:
        handlers_names.remove("file")

    return {
        "version": logging_settings.version,
        "encoding": logging_settings.encoding,
        "disable_existing_loggers": logging_settings.disable_existing_loggers,
        "formatters": formatters,
        "handlers": handlers,
        "root": {
            "level": logging_settings.loglevel,
            "handlers": handlers_names,
        },
    }
