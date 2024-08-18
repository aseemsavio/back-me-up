import boto3
import keyring
from botocore.client import BaseClient

from backmeup.utils.constants import KEYRING_SERVICE_NAME, KEYRING_AWS_ACCESS_KEY, KEYRING_AWS_SECRET_KEY


def s3_client() -> BaseClient:
    access_key = keyring.get_password(KEYRING_SERVICE_NAME, KEYRING_AWS_ACCESS_KEY)
    secret_key = keyring.get_password(KEYRING_SERVICE_NAME, KEYRING_AWS_SECRET_KEY)

    return boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )


def check_s3_connection() -> bool:
    client = s3_client()
    try:
        client.list_buckets()
        return True
    except Exception:
        return False
