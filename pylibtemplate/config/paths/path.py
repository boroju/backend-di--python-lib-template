"""
To define and manage system or remote paths easily.
"""
from __future__ import annotations

import re
from inspect import signature
from typing import Union


class Path(str):
    """
    A Path wrapper that extends string and manages the paths operations. If you set `start_slash` to `False` the Path
    must not be normalized with a '/' at first.

    ```python
    path = Path("/sub_folder")
    path_ns = Path("sub_folder", start_slash=False))
    path2 = Path("/sub_folder2")

    print(path)
    /subfolder
    print(path_ns)
    subfolder
    print(path / "new_subfolder")
    /subfolder/new_subfolder
    print(path / path2)
    /subfolder/subfolder_2
    ```
    """

    start_slash_regex = re.compile(r"(?:^(/)/+)|([^:/]/)/")

    def __new__(cls, path: str = "/", start_slash=True):
        simplify_slashes = Path.start_slash_regex.sub(
            r"\g<1>\g<2>", path if path.startswith("/") else f"/{path}"
        )
        path = simplify_slashes[1:] if not start_slash else simplify_slashes
        path = path.replace("\\", "/")  # Normalize windows paths.
        obj = super().__new__(cls, path)
        setattr(obj, "path", path)
        setattr(obj, "start_slash", start_slash)
        return obj

    def _new_path(self, path: str):
        """Clone and modify `path` for current Path object."""
        params = list(signature(self.__new__).parameters.keys())[1:]  # Remove cls
        new_params = {
            param: getattr(self, param) for param in params if not hasattr(getattr(self, param), "__call__")
        }
        new_params["path"] = path
        return self.__new__(self.__class__, **new_params)

    def __truediv__(self, other: Union[str, Path]):
        current = self.path[:-1] if self.path.endswith("/") else self.path
        if isinstance(other, Path):
            return self._new_path(f"{current}{other.path}")
        else:
            other = "/" + Path.start_slash_regex.sub(r"\g<1>\g<2>", other)
            return self._new_path(f"{current}{other}")

    @property
    def parent(self) -> Path:
        """Get the parent `Path` of the current `Path`."""
        return self._new_path("/".join(self.path.split("/")[:-1]))


class RemotePath(Path):
    """
    Relative Path definition that requires `protocol` and `host`.
    ```python
    path = Path("file","","/sub_folder")
    path2 = Path("file","","/sub_folder2")

    print(path)
    file:///subfolder
    print(path / "new_subfolder")
    file:///subfolder/new_subfolder
    print(path / path2)
    file:///subfolder/subfolder_2
    ```
    """

    def __new__(cls, protocol: str, host: str, path: str = "/"):
        url = f"{protocol}://{host}/"
        obj = super().__new__(cls, f"{url}{path}", start_slash=False)
        setattr(obj, "path", path)
        setattr(obj, "protocol", protocol)
        setattr(obj, "host", host)
        return obj
