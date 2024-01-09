"""
The module `setup` implements functions to use in setup.py fto automate some tasks.
"""
import importlib
import inspect
import os
import re
from logging import Logger
from types import ModuleType
from typing import Type, Union

from pylibtemplate.config.log.logger import log
from pylibtemplate.config.paths import PROJECT_PATH
from pylibtemplate.config.packaging.executable import Executable

_extra_requirement_match = re.compile(r"^([^[]*)\[?(\w+)?\]?(.*)$")


@log
def _import_module(name: str, log: Logger) -> Union[ModuleType, None]:
    try:
        return importlib.import_module(name)
    except Exception as e:
        """Dependencies not installed yet."""
        log.warning(f"Error importing {name} module.\n{e}")
        return


def create_entry_points_from_package(base_package: str, epclz: Type[Executable]):
    """
    Generate entry_points foreach class that implements a superclass `Executable`.
    The classes are iterated inside the package `base_package` and compared with class
    `epclz` that could be the same `Executable` class or derived.

    For example, if you have 3 modules in a package with 4 classes that implements `Executable`:

    ```python
    package_executables
    |- module1 ------------ class1(Executable):
            |  ------------ class2(Executable):
    |- module 2 ----------- class3(Executable):
    |- module 3 ----------- class4(Executable):
    ```

    you can do:
    ```python
    create_entrypoints_from_package("package_executables", Executable)

    [
    "class1 = package_executables.module1:class1.execute",
    "class2 = package_executables.module1:class2.execute",
    "class3 = package_executables.module2:class3.execute",
    "class4 = package_executables.module3:class4.execute",
    ]
    ```

    Now, you can add this function to your setup.py in entrypoint definition.
    When you have installed the package, you would execute:
    ```python
    > class1
    > class2
    > class3
    > class4
    ```
    """
    return [
        f"{clz.__name__} = {clz.__module__}:{clz.__name__}.execute"
        for clz in set(
            _type
            for mod in [
                _import_module(
                    f"{folder.replace(PROJECT_PATH.path, '').replace('/', '.')}.{file.replace('.py', '')}"
                )
                for folder, packages, files in os.walk(PROJECT_PATH.path + base_package)
                for file in files
                if file.endswith(".py")
            ]
            if mod
            for name, _type in inspect.getmembers(mod)
            if inspect.isclass(_type)
            and _type.__module__ == mod.__name__
            and _type != epclz
            and issubclass(_type, epclz)
        )
    ]
