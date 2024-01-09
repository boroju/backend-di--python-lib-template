"""Configuration package extension for common functionalities."""

import inspect
import logging
import pkgutil
from itertools import chain
from typing import List, Type


def _load_classes_in_module(info: pkgutil.ModuleInfo) -> List[Type]:
    """
    Load the classes of a module that are declared inside the module.
    The dependencies are excluded.
    """
    try:
        _module = info.module_finder.find_spec(info.name).loader.load_module(info.name)
        # List objects in the module.
        attrs = [getattr(_module, cls) for cls in dir(_module) if not cls.startswith("_")]
        # Filter classes and objects defined in the module.
        module_objs = filter(lambda obj: inspect.isclass(obj) and obj.__module__ == info.name, attrs)
        # Register classes on root package.
        return list(module_objs)
    except Exception as e:
        logging.debug(f"Impossible to load {info.name}.\n{e}")
        return list()


def import_module_classes(path: List[Type]):
    """
    Import module classes from a __path__.
    This is required to import classes foreach module in root package.

    Add this lines to __init__.py on package root.

    ```python
    __all__ = []
    for module in import_module_classes(__path__):
        __all__.append(module.__name__)
        globals()[module.__name__] = module
    ```
    """
    return chain(
        *[
            _load_classes_in_module(info)
            for info in pkgutil.walk_packages(path)
            if not info.ispkg and "." not in info.name
        ]
    )
