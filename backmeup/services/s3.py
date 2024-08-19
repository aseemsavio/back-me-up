import boto3
import keyring
from botocore.client import BaseClient
from rich import print

from backmeup.services.sqlite import check_if_file_is_backed_up, connect_to_db, Backup, create_file_record_after_backup, \
    create_individual_backup_table_if_not_exists
from backmeup.utils.constants import KEYRING_SERVICE_NAME, KEYRING_AWS_ACCESS_KEY, KEYRING_AWS_SECRET_KEY

import os
from botocore.exceptions import ClientError


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


def create_s3_bucket_if_not_exists(bucket_name: str, region: str) -> str:
    client = s3_client()

    # Check if the bucket already exists
    try:
        client.head_bucket(Bucket=bucket_name)
        return "bucket-exists"
    except ClientError as e:
        # If a 404 error is thrown, the bucket does not exist
        error_code = e.response['Error']['Code']
        if error_code == '404':
            # Create the bucket
            client.create_bucket(
                Bucket=bucket_name.lower(),
                CreateBucketConfiguration={'LocationConstraint': region}
            )
            return "bucket-created"
        else:
            print(e)
            return "bucket-creation-error"


def upload_directory_to_s3(bucket_name: str, directory_path: str, backup: Backup):
    client = boto3.client('s3')
    connection = connect_to_db()
    create_individual_backup_table_if_not_exists(connection=connection, backup_id=backup.id)
    uploads = 0

    for root, dirs, files in os.walk(directory_path):
        for filename in files:
            # Construct the full local path
            local_path = os.path.join(root, filename)

            # Construct the S3 path (relative to the directory_path)
            relative_path = os.path.relpath(local_path, directory_path)
            s3_path = relative_path.replace("\\", "/")  # Ensure correct S3 path format

            try:
                # Upload the file to S3 with Glacier Deep Archive storage class
                backed_up = check_if_file_is_backed_up(connection=connection, backup_id=backup.id, file=s3_path)

                if not backed_up:
                    client.upload_file(
                        local_path,
                        bucket_name,
                        s3_path,
                        ExtraArgs={'StorageClass': 'DEEP_ARCHIVE'}
                    )
                    create_file_record_after_backup(connection=connection, backup_id=backup.id, file=s3_path)
                    uploads += 1
                    print(f"Uploaded {s3_path} to {bucket_name} with storage class DEEP_ARCHIVE")
            except ClientError as e:
                print(f"Error uploading {s3_path}: {e}")
    print(f"Total files uploaded: {uploads}")
