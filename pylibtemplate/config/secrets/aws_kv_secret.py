"""The module `aws_kv_secret` contains a `Secret` implementation to get the secrets from AWS Secret Manager backend."""

from boto3.session import Session
import json

from pylibtemplate.config.secrets.secret import Secret


class AwsKVSecret(Secret):
    """
    `Secret` implementation to get the secret from AWS Secret Manager backend.

    Requires the Environment variables:

    - `AWS_ACCESS_KEY_ID`.
    - `AWS_SECRET_ACCESS_KEY`.
    - `AWS_SESSION_TOKEN`.

    ```
    Secret("AwsKVSecret:my_secret")
    ```
    """

    @staticmethod
    def resolve(key: str):
        session = Session()

        secret_response = session.client(
            service_name="secretsmanager",
            region_name="eu-west-1",
        ).get_secret_value(SecretId=key)

        # Only returning SecretString.
        try:
            return json.loads(secret_response["SecretString"])
        # Allow getting string secrets
        except ValueError:
            return secret_response["SecretString"]
