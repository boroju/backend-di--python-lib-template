"""
The module `environment` contains an `Environment` enum class that defines all possible environments available in
the platform.
"""

from __future__ import annotations

import os
from enum import Enum, unique


@unique
class Environment(Enum):
    """
    Define available environments.

    ```python
    pro = Environment.PRO
    pro == Environment.PRO # True

    Environment.parse("Dev") == Environment.DEV # True
    ```
    """

    NONE = "none"
    TEST = "test"
    LOCAL = "local"
    LAB = "lab"
    DEV = "dev"
    INT = "int"
    PRE = "pre"
    PRO = "pro"

    @classmethod
    def from_env(cls, raise_exception=False) -> Environment:
        """
        Get Environment using environment variable _ENVIRONMENT_.

        - `raise_exception: bool`: Raises an `EnvironmentError` if the environment variables is
        not provided. (default: True)
        """
        try:
            return cls.parse(os.environ["ENVIRONMENT"])
        except KeyError:
            if raise_exception:
                raise EnvironmentError("Environment variable 'ENVIRONMENT' must be provided.")
            else:
                return Environment.NONE

    @classmethod
    def parse(cls, env: str) -> Environment:
        """
        Parse environment from str.

        Example:
        ```python
        Environment.parse("dev")
        ```
        """
        try:
            return cls[env.upper()]
        except Exception as e:
            raise TypeError(f"Invalid environment: {env}. {e}")
