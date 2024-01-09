"""
The module `package_version_provider` defines an Abstract class to use by Package Version Providers.
"""
from typing import Union

from pylibtemplate.config.versioning.version import Version
from pylibtemplate.config.packaging.package_version import PackageVersion


class PackageVersionProvider:
    """
    Abstract Class that provides custom PackageVersions in function of base `Version` object.
    The child classes must implement the staticmethod (or classmethod) `provide(version: Version) -> PackageVersion`.
    """

    @staticmethod
    def provide(version: Union[PackageVersion, Version]) -> PackageVersion:
        raise NotImplementedError("Method 'provide' must be implemented by a child.")
