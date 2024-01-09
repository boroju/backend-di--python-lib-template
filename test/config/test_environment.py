import pytest

from pylibtemplate.config.envs.environment import Environment


def test_environment_parser():
    assert Environment.parse("int") == Environment.INT
    assert Environment.parse("Int") == Environment.INT
    assert Environment.parse("prO") == Environment.PRO
    assert Environment.parse("DEV") == Environment.DEV
    assert Environment.parse("local") == Environment.LOCAL
    with pytest.raises(TypeError):
        Environment.parse("Fake Env")


def test_environment_raises():
    assert Environment.from_env() == Environment.NONE
    with pytest.raises(EnvironmentError):
        Environment.from_env(raise_exception=True)
