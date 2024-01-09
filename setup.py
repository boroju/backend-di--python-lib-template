from setuptools import setup, find_packages

requirements = [
    "aiohttp>=3.8,<4.0",
    "boto3>=1.33.2,<2.0",
]

extra_requirements = {
    "test": [
        "pytest>=7.2",
        "pytest-cov>=4.0",
        "coverage>=7.0",
        "pytest-mock>=3.10",
    ],
    "local": [
        "GitPython>=3.1,<4.0",
        "pre-commit>=3.3",
    ],
    "setup": ["wheel>=0.37", "mypy>=1.2"],
    "airflow": [
        "apache-airflow-providers-slack",
    ],
}


def _setup():
    """
    Prevents setup() execution when this module is loaded as a module.
    """
    from pylibtemplate.config.packaging import git
    from pylibtemplate.config.packaging.commands.increment_version import IncrementVersion
    from pylibtemplate.config.packaging.commands.skipci_git_commit import SkipCICommitAndRepointTag
    from pylibtemplate.config.packaging.package_version_providers.spacial_pokemon_pvp import (
        SPokemonPVProvider,
    )

    readme = open("docs/README.md", "r").read()

    setup(
        name="pylibtemplate",
        version=git.branch_version(),
        author="Data Enablers team",
        author_email="noreply.gp.boroju@gmail.com",
        long_description_content_type="text/markdown",
        long_description=readme,
        packages=find_packages(
            exclude=("test", "test.*", "integration_test", "integration_test.*")
        ),
        cmdclass={
            "increment_version": IncrementVersion.with_version_provider(
                SPokemonPVProvider
            ),
            "skip_ci_commit": SkipCICommitAndRepointTag,
        },
        install_requires=requirements,
        extras_require=extra_requirements,
        package_data={"": ["*.pyi", "**/*.pyi"]},
    )


if __name__ == "__main__":
    _setup()
