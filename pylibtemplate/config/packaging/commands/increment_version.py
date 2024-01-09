from __future__ import annotations

import logging
from typing import Type

from setuptools import Command

from pylibtemplate.config.packaging import git
from pylibtemplate.config.packaging.package_version_providers.base_pvp import BasePVP
from pylibtemplate.config.packaging.package_version_providers.package_version_provider import (
    PackageVersionProvider,
)


class IncrementVersion(Command):
    description = "Increment the version of the package."
    user_options = []
    provider: PackageVersionProvider = BasePVP
    """Use `BasePVP` by default."""

    @classmethod
    def with_version_provider(cls, package_version_provider) -> Type:
        return type(cls.__name__, (cls,), dict(provider=package_version_provider))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        new_version = self.provider.provide(git.last_version() + 1)
        logging.warning(
            f"""Creating new git tag: {new_version} ({new_version.description}).
                            """
        )
        git.create_tag(new_version)
