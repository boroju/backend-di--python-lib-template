"""The module `s3_path` contains a `Path` implementation to define an S3 path."""
from pylibtemplate.config.paths.path import RemotePath


class S3Path(RemotePath):
    """
    Amazon S3 Path extension.
    Requires:

    - `bucket: str`: Bucket name.
    - `path: str`: Relative path from the root. (Default: "/")
    - `filesystem_suffix: str`: The suffix of the filesystem to use, possible values are: '', 'n' or 'a' (Default '').
    """

    def __new__(cls, bucket: str, path: str = "/", filesystem_suffix=""):
        if filesystem_suffix not in ("", "a", "n"):
            raise TypeError(f"Error in {cls.__name__}: filesystem_suffix only accept values '', 'a' or 'n'.")
        obj = super().__new__(cls, f"s3{filesystem_suffix}", bucket, path)
        setattr(obj, "bucket", bucket)
        setattr(obj, "filesystem_suffix", filesystem_suffix)
        return obj
