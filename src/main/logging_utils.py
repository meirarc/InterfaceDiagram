"""
This module is used to create a standard logging procedures using @decorator function
"""
import functools
import logging
from typing import Callable, Any


def configure_logging(log_level=logging.ERROR):
    """
    This function configure the initial state of the logging
    """
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )


def debug_logging(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    This function is used to provide the logging for each method that use the decorator 
    @debug_logging
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logging.debug("Calling %s with arguments: %s", func.__name__, args[1:])

        value = func(*args, **kwargs)

        logging.debug("Finished %s with return value: %s",
                      func.__name__, value)
        return value
    return wrapper
