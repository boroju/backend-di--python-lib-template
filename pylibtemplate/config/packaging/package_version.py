"""
The module `package_version` implements `PackageVersion` class that extends the definition of
`Version` in order to contain information of the package.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

from pylibtemplate.config.versioning.version import Version


@dataclass(frozen=True)
class PackageVersion(Version):
    """
    Extends the `Version` dataclass in order to provide package information.
    """

    branch: str = "master"
    """The branch of the git repository (default: master)."""
    description: str = ""
    """Description of the package version."""
    labels: Dict[str, str] = field(default_factory=dict)
    """Extra labels linked to the version."""

    def __add__(self, other: int):
        v: Version = super().__add__(other)
        return PackageVersion(
            v.major, v.medium, v.minor, self.branch, self.description, self.labels
        )

    def __hash__(self):
        return super().__hash__()
