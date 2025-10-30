"""Module for logging."""

import logging
from typing import Union

from rich.logging import RichHandler


def setup_logger(logger_name: str = None) -> logging.Logger:
    """
    Setup the logger.

    Parameters
    ----------
    logger_name: :obj:`str`
        Name of the logger to return, if None, the root logger is returned.

    Returns
    -------
    Logger
        A logger object.
    """
    logger = logging.getLogger(logger_name)
    if not has_handler(logger):
        logger = add_default_handler(logger)

    return logger


def has_handler(logger):
    """
    Check if a handler is present.

    Checks the root logger and module logger.

    logger: :obj:`Logger`
        A logging object.

    Returns
    -------
    bool
        True if a handler is present and False if no handler is present
    """
    root_handler = logging.getLogger().hasHandlers()
    module_handler = logger.handlers

    return True if (root_handler or module_handler) else False


def add_default_handler(logger: logging.Logger, format: Union[str, None] = None):
    """
    Add a default and format handler. Uses ``RichHandler`` as the default logger.

    Parameters
    ----------
    logger: :obj:`Logger`
        A logging object.

    format: :obj:`str`
        String specifying the format of the logged message.

    Returns
    -------
    Logger
        A logger object.
    """

    format = format if format else "%(asctime)s %(name)s [%(levelname)s] %(message)s"

    handler = RichHandler()
    handler.setFormatter(logging.Formatter(format))
    logger.addHandler(handler)

    return logger
