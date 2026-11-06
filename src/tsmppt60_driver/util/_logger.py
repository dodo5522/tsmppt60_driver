import logging
import sys
from logging import (  # noqa: F401
    CRITICAL,
    DEBUG,
    ERROR,
    FATAL,
    INFO,
    NOTSET,
    WARNING,
)
from pathlib import Path


class Logger(logging.Logger):
    """Configure console and optional file logging for the module."""

    _FORMAT_LOG_MSG_ONLY = "%(message)s"
    _FORMAT_LOG_MSG_FULL = "%(asctime)s %(name)s %(levelname)s: %(message)s"
    _FORMAT_LOG_DATE = "%Y/%m/%d %p %l:%M:%S"

    def __init__(
        self,
        name: str,
        level=INFO,
        *,
        stream=sys.stdout,
        out_path: Path | None = None,
        full_log: bool = False,
    ):
        """Initialize a logger.

        Args:
            name: Name of the logger.
            level: Logging level.
            out_path: Optional path to the log file.
            full_log: Output log with full logging information.
        """
        super().__init__(name, level)

        handler = logging.StreamHandler(stream)
        formatter = logging.Formatter(
            fmt=self._FORMAT_LOG_MSG_FULL if full_log else self._FORMAT_LOG_MSG_ONLY,
            datefmt=self._FORMAT_LOG_DATE if full_log else None,
        )
        handler.setFormatter(formatter)
        self.addHandler(handler)

        if out_path:
            handler = logging.FileHandler(out_path, mode="a")
            handler.setFormatter(formatter)
            self.addHandler(handler)
