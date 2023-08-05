import logging.handlers

from limecore.core.configuration import Configuration


class HandlerFactory:
    def get(self, configuration: Configuration):
        if configuration.get_string("type") == "file":
            return self._get_file_handler(configuration)
        else:
            NotImplementedError(configuration.get_string("type"))

    def _get_file_handler(self, configuration: Configuration):
        return logging.handlers.RotatingFileHandler(
            configuration.get_string("filename"),
            maxBytes=configuration.get_int("max_bytes") or 10485760,
            backupCount=configuration.get_int("max_backup") or 10,
            encoding="utf-8",
        )
