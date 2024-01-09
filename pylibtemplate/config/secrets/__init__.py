"""
The package `secrets` contains functionalities and objects that help you to get secret values (like credentials)
in python code.
"""

__all__ = []

from pylibtemplate.config import import_module_classes

for module in import_module_classes(__path__):
    __all__.append(module.__name__)
    globals()[module.__name__] = module
