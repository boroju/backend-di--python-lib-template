"""
The module `git` implements functionalities to manage the versioning in the python code.
"""
import re

from git import Repo

from pylibtemplate.config.paths import PROJECT_PATH
from pylibtemplate.config.paths.path import Path
from pylibtemplate.config.versioning.version import Version
from pylibtemplate.config.packaging.package_version import PackageVersion


def _find_repo(path: Path) -> Repo:
    """
    Find the git repository on specific folder or subfolder of a project.
    """
    if path == "/":
        return None
    else:
        try:
            print(path)
            return Repo(path)
        except Exception:
            return _find_repo(path.parent)


repo = _find_repo(PROJECT_PATH)
"""Repo object pointing to root project directory"""


def last_version() -> PackageVersion:
    """
    Get last Version using last Git tag available in the repository.
    If it doesn't exist create a default PackageVersion(1), create the tag in git and return it.
    """
    try:
        last_tag = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)[-1]
        version = Version.parse(last_tag.name)
        return PackageVersion(
            version.major,
            version.medium,
            version.minor,
            repo.active_branch.name,
            last_tag.tag.message,
            labels=dict(),
        )
    except IndexError:
        version = PackageVersion(
            major=1,
            medium=0,
            minor=-1,
            branch=repo.active_branch.name,
            description="v1.0.-1",
            labels=dict(),
        )
        repo.create_tag(str(version), message=version.description)
        return version


def branch_version() -> str:
    """
    Get version naming composed by the branch. If branch is `master` no branch suffix
    will be set. The special characters on branch will be replaced by underscore '_'.

    Example:

    ```
    # master
    branch_version() # 1.0.0

    # feature/DI-34444
    branch_version() # feature_DI_34444_1.0.0
    ```
    """
    lv = last_version()
    normalized_branch = re.sub(r"[^\w]", r"_", lv.branch)
    branch_number = re.sub(r"[^\d]", r"", normalized_branch)
    return str(lv) if normalized_branch == "master" else f"{lv}.dev{branch_number}"


def create_tag(version: PackageVersion) -> None:
    """
    Create a new tag from `PackageVersion`.

    Example:

    ```
    create_tag(PackageVersion(1, 0, 0, description="test tag")) # tag: 1.0.0 message: test tag
    ```
    """
    repo.create_tag(str(version), message=version.description)
