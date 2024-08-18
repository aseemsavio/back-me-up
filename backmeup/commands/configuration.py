from typing import Optional
from rich import print
import keyring

from backmeup.utils import print_error
from backmeup.utils.constants import KEYRING_SERVICE_NAME, KEYRING_BACKUP_LOCATION_KEY, KEYRING_AWS_REGION_KEY, \
    KEYRING_AWS_ACCESS_KEY, KEYRING_AWS_SECRET_KEY


def configure_cli(
        location: Optional[str],
        access_key: Optional[str],
        secret_key: Optional[str],
        region: Optional[str]
):
    """

    :return:
    """
    if location not in {"s3"}:
        print_error('Only "S3" is supported for --location or -l.')
        exit()

    if region not in {
        "us-east-1", "us-east-2", "us-west-1", "us-west-2", "af-south-1", "ap-east-1",
        "ap-south-1", "ap-northeast-1", "ap-northeast-2", "ap-northeast-3", "ap-southeast-1",
        "ap-southeast-2", "ap-southeast-3", "ca-central-1", "eu-central-1", "eu-west-1",
        "eu-west-2", "eu-west-3", "eu-north-1", "eu-south-1", "eu-south-2", "me-south-1",
        "me-central-1", "sa-east-1", "cn-north-1", "cn-northwest-1", "us-gov-west-1",
        "us-gov-east-1"
    }:
        print_error("Invalid AWS region")
        exit()

    if access_key is None:
        print_error('"--access" or "-a" should be provided.')
        exit()

    if secret_key is None:
        print_error('"--secret" or "-s" should be provided.')
        exit()

    keyring.set_password(KEYRING_SERVICE_NAME, KEYRING_BACKUP_LOCATION_KEY, location)
    keyring.set_password(KEYRING_SERVICE_NAME, KEYRING_AWS_REGION_KEY, region)
    keyring.set_password(KEYRING_SERVICE_NAME, KEYRING_AWS_ACCESS_KEY, access_key)
    keyring.set_password(KEYRING_SERVICE_NAME, KEYRING_AWS_SECRET_KEY, secret_key)

    print("Successfully configured your backmeup CLI")
