from __future__ import annotations

import logging

from setuptools import Command

from pylibtemplate.config.packaging import git


class SkipCICommitAndRepointTag(Command):
    description = """
    Create an amend commit with latest changes (normally update the docs or package version).
    The last tag will be repointed to this commit.
    Finally, mark the commit to skip the ci.
    """
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        git.repo.git.add(all=True)

        logging.warning("Modifying last commit to skip CI.")
        message = git.repo.commit().message
        if "[skip ci]" not in message:
            message = f"[skip ci] {message}"
        git.repo.git.commit(m=message, amend=True)

        logging.warning(f"Repointing last tag {git.last_version()}")
        last_version = git.last_version()
        git.repo.git.tag("-d", str(last_version))
        git.create_tag(last_version)
