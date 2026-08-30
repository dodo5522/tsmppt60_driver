import logging


class Logger:
    """Configure console and optional file logging for the module."""

    _FORMAT_LOG_MSG = "%(asctime)s %(name)s %(levelname)s: %(message)s"
    _FORMAT_LOG_DATE = "%Y/%m/%d %p %l:%M:%S"

    def __init__(self, log_file_path=None, debug=False):
        """Initialize a logger.

        Args:
            log_file_path: Optional path to the log file.
            debug: Set the logger to debug level when ``True``.
        """
        self.logger = logging.getLogger(type(self).__name__)

        handler = logging.StreamHandler()
        formatter = logging.Formatter(fmt=self._FORMAT_LOG_MSG, datefmt=self._FORMAT_LOG_DATE)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        if log_file_path:
            handler = logging.FileHandler(log_file_path, mode="a")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        if debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
