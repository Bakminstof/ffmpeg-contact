from logging import Formatter, LogRecord

from logging_settings.models import LOG_LINE_FORMATS

__all__ = ("ColourFormatter",)


class ColourFormatter(Formatter):
    def format(self, record: LogRecord) -> str:
        log_fmt = LOG_LINE_FORMATS[record.levelno] + self._fmt
        formatter = Formatter(fmt=log_fmt, datefmt=self.datefmt)
        return formatter.format(record)
