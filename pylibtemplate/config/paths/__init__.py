"""
The package `paths` contains functionalities and objects that help you to manage system or remote paths easily.
"""
import os

from pylibtemplate.config.paths.path import Path

_IS_WINDOWS_OS_ = os.name == "nt"
PROJECT_PATH: Path = Path(os.getcwd(), start_slash=not _IS_WINDOWS_OS_) / ""
"""The absolute base path of the project."""
