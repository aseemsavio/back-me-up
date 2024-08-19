from dataclasses import dataclass
from typing import Optional

import keyring
from backmeup.utils.constants import KEYRING_SERVICE_NAME, KEYRING_BACKUP_LOCATION_KEY, KEYRING_AWS_REGION_KEY, \
    KEYRING_AWS_ACCESS_KEY, KEYRING_AWS_SECRET_KEY


@dataclass
class Vault:
    location: str
    access_key: str
    secret_key: str
    region: str


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


def get_vault_data() -> Optional[Vault]:
    try:
        location = keyring.get_password(KEYRING_SERVICE_NAME, KEYRING_BACKUP_LOCATION_KEY)
        region = keyring.get_password(KEYRING_SERVICE_NAME, KEYRING_AWS_REGION_KEY)
        access_key = keyring.get_password(KEYRING_SERVICE_NAME, KEYRING_AWS_ACCESS_KEY)
        secret_key = keyring.get_password(KEYRING_SERVICE_NAME, KEYRING_AWS_SECRET_KEY)

        if (location is not None) and (region is not None) and (access_key is not None) and (secret_key is not None):
            return Vault(
                location=location,
                region=region,
                access_key=access_key,
                secret_key=secret_key
            )
        else:
            return None
    except Exception:
        return None
