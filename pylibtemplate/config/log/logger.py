"""
The module `logger` contains functionalities to manage logs.
"""
import inspect
import logging
from typing import Callable, Union, Type


def log(level: Union[int, Callable, Type]) -> Union[Callable, Type]:
    """
    Decorator that injects an independent log with our stream and log level (INFO by default).
    This helps to prevent change the log level of other libraries.

    - In case of a `function`, the log will be provided like a key parameter named `log`.
    - In case of a `Class`, the log will be provided `log` like a class attribute.

    ```
    @log
    def my_function(...,log:Logger);
        log.info("My logger in my function")

    @log(level=logging.DEBUG)
    def my_function(...,log:Logger);
        log.debug("My debug logger in my function")

    @log
    class MyClass:

        def __init__(self):
            self.log.info("My logger in my class")
    ```
    """

    def wrapper(
        obj: Union[Callable, Type], level: int = logging.INFO
    ) -> Union[Callable, Type]:
        _log = get_logger(obj.__name__, level)
        if inspect.isfunction(obj):
            return lambda *args, **kwargs: obj(*args, **kwargs, log=_log)
        else:
            setattr(obj, "log", _log)
            return obj

    if isinstance(level, int):
        return lambda func: wrapper(func, level)
    else:
        func: Union[Callable, Type] = level
        return wrapper(func)


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Create an independent log with our stream and log level (INFO by default).
    This helps to prevent change the log level of other libraries.
    """
    log = logging.getLogger(name)
    if name in [h.name for h in log.handlers]:
        log.handlers.clear()
    handler = logging.StreamHandler()
    handler.set_name(name)
    handler.setFormatter(
        logging.Formatter("%(asctime)s:%(name)s:%(levelname)s: %(message)s")
    )
    log.addHandler(handler)
    log.setLevel(level)
    return log
