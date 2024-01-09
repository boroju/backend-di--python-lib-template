"""
The module `base_pvp` implements a basic `PackageVersionProvider`.
"""

from pylibtemplate.config.versioning.version import Version
from pylibtemplate.config.packaging import git
from pylibtemplate.config.packaging.package_version import PackageVersion
from pylibtemplate.config.packaging.package_version_providers.package_version_provider import (
    PackageVersionProvider,
)


class BasePVP(PackageVersionProvider):
    """
    Basic Package Version Provider.

    This version provider implements a basic functionality to provide version information.

    Example:

        - Version(1,0,0) -> "v1.0.0"
        - Version(1,2,3) -> "v1.2.3"
    """

    @staticmethod
    def provide(version: Version) -> PackageVersion:
        """
        Provide the basic PackageVersion object.
        """
        return PackageVersion(
            version.major,
            version.medium,
            version.minor,
            git.repo.active_branch.name,
            f"v{version}",
            dict(),
        )
