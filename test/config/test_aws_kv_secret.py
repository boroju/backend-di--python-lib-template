import importlib

import pytest

from pylibtemplate.config.secrets.secret import MetaSecret, Secret


def test_aws_kv_secret(mocker):
    session = mocker.patch("boto3.session.Session")
    import pylibtemplate.config.secrets.aws_kv_secret

    importlib.reload(pylibtemplate.config.secrets.aws_kv_secret)
    from pylibtemplate.config.secrets.secret import Secret

    Secret("AwsKVSecret:test")
    session().client(
        service_name="secretsmanager",
        region_name="eu-west-1",
    ).get_secret_value.assert_called_once()
