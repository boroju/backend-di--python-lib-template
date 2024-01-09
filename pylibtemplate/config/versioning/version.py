"""
The module `version` contains an `Version` data class that helps you to manage the versioning.
"""
from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Version:
    """
    Represents a version of anything.

    - `major`: Major changes. The changes breaks the previous version.
    - `medium`: Medium changes. Anything changes but it's compatible with previous version (contain deprecations).
    - `minor`: Minor changes. The changes no breaks anything.

    ```python
    version = Version(1,0,0)

    version + 1 # Increment minor version in 1.
    ```
    """

    major: int
    medium: int = 0
    minor: int = 0

    _reg_version = re.compile(r"v?(\d+).?(\d+)?.?(-?\d+)?")

    def __str__(self):
        return f"{self.major}.{self.medium}.{self.minor}"

    def __add__(self, other: int) -> Version:
        return Version(self.major, self.medium, self.minor + other)

    @staticmethod
    def parse(version: str) -> Version:
        """
        Parse a version string to Version object.

        ```python
        Version.parse("v1.0.0")
        Version.parse("1.0.0")
        Version.parse("v1.0")
        Version.parse("1.0")
        Version.parse("v1")
        Version.parse("1")
        ```
        """
        match = Version._reg_version.match(version)
        if not match:
            raise TypeError(f"Impossible to parse version {version}.")
        _maj, _med, _min = match.groups()
        return Version(int(_maj), int(_med) if _med else 0, int(_min) if _min else 0)
