# import dataclasses

import keyring
from backmeup.utils.constants import KEYRING_SERVICE_NAME, KEYRING_BACKUP_LOCATION_KEY, KEYRING_AWS_REGION_KEY, \
    KEYRING_AWS_ACCESS_KEY, KEYRING_AWS_SECRET_KEY


# @dataclasses
# class Vault:
#     location: str
#     access_key: str
#     secret_key: str
#     region: str


def setup_vault(
        location: str,
        access_key: str,
        secret_key: str,
        region: str
):
    keyring.set_password(KEYRING_SERVICE_NAME, KEYRING_BACKUP_LOCATION_KEY, location)
    keyring.set_password(KEYRING_SERVICE_NAME, KEYRING_AWS_REGION_KEY, region)
    keyring.set_password(KEYRING_SERVICE_NAME, KEYRING_AWS_ACCESS_KEY, access_key)
    keyring.set_password(KEYRING_SERVICE_NAME, KEYRING_AWS_SECRET_KEY, secret_key)


def clear_vault():
    try:
        keyring.delete_password(KEYRING_SERVICE_NAME, KEYRING_BACKUP_LOCATION_KEY)
        keyring.delete_password(KEYRING_SERVICE_NAME, KEYRING_AWS_REGION_KEY)
        keyring.delete_password(KEYRING_SERVICE_NAME, KEYRING_AWS_ACCESS_KEY)
        keyring.delete_password(KEYRING_SERVICE_NAME, KEYRING_AWS_SECRET_KEY)
    except Exception:
        return
