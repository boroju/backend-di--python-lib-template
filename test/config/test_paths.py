import pytest

from pylibtemplate.config.paths.path import Path, RemotePath


def test_s3_path():
    from pylibtemplate.config.paths.s3_paths import S3Path

    path = S3Path("nobucket", "/test/path")
    assert path.protocol == "s3"
    assert path.host == "nobucket"
    assert path.path == "/test/path"
    assert path == "s3://nobucket/test/path"
    assert path / "new_path" == "s3://nobucket/test/path/new_path"
    assert path / "/new_path" == "s3://nobucket/test/path/new_path"
    path = S3Path("nobucket", "/test/path", filesystem_suffix="a")
    assert path == "s3a://nobucket/test/path"
    path = S3Path("nobucket", "/test/path", filesystem_suffix="n")
    assert path == "s3n://nobucket/test/path"

    with pytest.raises(TypeError):
        (S3Path("nobucket", "/test/path", filesystem_suffix="sakjmsia"),)


def test_remote_path():
    path = RemotePath("file", "/test/mypath", "relative")
    assert path / "test" == "file:///test/mypath/relative/test"


def test_path():
    path = Path("root")
    relative = Path("subpath")
    assert Path("C://Users", start_slash=False) / "windows" == "C://Users/windows"
    assert path / "" == "/root/"
    assert path / "file.test" == "/root/file.test"
    assert path / "file//test" == "/root/file/test"
    assert (path / "file.test").parent == "/root"
    assert path / relative == "/root/subpath"
    assert path / relative / relative == "/root/subpath/subpath"
    assert Path("C:\\Users\\windows", start_slash=False) == "C:/Users/windows"
    assert Path("C:\\Users\\windows", start_slash=False) / "another_path" == "C:/Users/windows/another_path"

