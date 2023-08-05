import logging

from injector import Module as _Module, provider, singleton
from limecore.core.configuration import Configuration
from typing import Optional

from .handler_factory import HandlerFactory
from .logger_factory import LoggerFactory


class Module(_Module):
    @singleton
    @provider
    def provider_logger_factory(
        self, configuration: Configuration, handler_factory: HandlerFactory
    ) -> LoggerFactory:
        logging_configuration = configuration.section("limecore", "logging")

        default_format = self._format(logging_configuration.get_string("format"))
        default_level = self._level(logging_configuration.get_string("level"))

        root_logger = logging.getLogger()
        root_logger.setLevel(default_level)

        for sink in logging_configuration.get_list("sinks"):
            handler = handler_factory.get(sink)
            handler.setFormatter(
                self._format(sink.get_string("format"), default_format=default_format)
            )
            handler.setLevel(
                self._level(sink.get_string("level"), default_level=default_level)
            )

            root_logger.addHandler(handler)

        if logging_configuration.get_bool("console"):
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(default_format)
            console_handler.setLevel(default_level)

            root_logger.addHandler(console_handler)

        return root_logger.getChild

    def _format(
        self,
        format: Optional[str],
        default_format: logging.Formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(levelname)s - %(message)s"
        ),
    ) -> logging.Formatter:
        if format is None:
            return default_format
        else:
            return logging.Formatter(format)

    def _level(
        self, level_name: Optional[str], default_level: int = logging.INFO
    ) -> int:
        if level_name is None:
            return default_level

        return {
            "critical": logging.CRITICAL,
            "debug": logging.DEBUG,
            "error": logging.ERROR,
            "fatal": logging.FATAL,
            "info": logging.INFO,
            "warn": logging.WARN,
        }[level_name.lower()]
