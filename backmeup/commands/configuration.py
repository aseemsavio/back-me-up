from typing import Optional

from backmeup.services.s3 import check_s3_connection
from backmeup.services.vault import setup_vault, clear_vault
from backmeup.utils import print_error


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
        print_error('Only "S3" is supported for [red bold]--location[/] or [red bold]-l[/].')
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
        print_error('[red bold]--access[/] or [red bold]-a[/] should be provided.')
        exit()

    if secret_key is None:
        print_error('[red bold]--secret[/] or [red bold]-s[/] should be provided.')
        exit()

    setup_vault(location=location, access_key=access_key, secret_key=secret_key, region=region)
    connected = check_s3_connection()
    if not connected:
        clear_vault()
        print_error("S3 is not configured. Please check your credentials and retry again.")
        exit()


def reset_cli():
    clear_vault()
