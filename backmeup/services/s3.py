from datetime import datetime

import boto3
import keyring
from botocore.client import BaseClient
from rich import print
from rich.console import Console

from backmeup.services.sqlite import check_if_file_is_backed_up, connect_to_db, Backup, create_file_record_after_backup, \
    create_individual_backup_table_if_not_exists, get_total_files_backed_up_in_backup_set
from backmeup.utils.constants import KEYRING_SERVICE_NAME, KEYRING_AWS_ACCESS_KEY, KEYRING_AWS_SECRET_KEY

import os
from botocore.exceptions import ClientError

from backmeup.utils.files import scan_directory


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


def upload_mutable_directory_to_s3(bucket_name: str, directory_path: str, backup: Backup):
    client = s3_client()
    connection = connect_to_db()
    create_individual_backup_table_if_not_exists(connection=connection, backup_id=backup.id)
    backed_up_files_count = get_total_files_backed_up_in_backup_set(connection=connection, backup_id=backup.id)
    total_files_in_directory = scan_directory(abs_path=backup.source_absolute_path)["file_count"]
    files_to_be_uploaded = total_files_in_directory - backed_up_files_count
    uploads = 0

    console = Console()
    with console.status("[green]Initializing mutable backup...[/green]") as status:
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
                        status.update(
                            status=f'[{uploads}/{files_to_be_uploaded}] Uploading [gold1]"{s3_path}"[/] -> [orange1]"{bucket_name}"[/]...')
                        client.upload_file(
                            local_path,
                            bucket_name,
                            s3_path,
                            ExtraArgs={'StorageClass': 'DEEP_ARCHIVE'}
                        )
                        create_file_record_after_backup(connection=connection, backup_id=backup.id, file=s3_path)
                        uploads += 1
                except ClientError as e:
                    print(f"[red]Error uploading {s3_path}: {e}[/]")
        print(f"Total files uploaded: {uploads}")

    connection.close()


def create_bucket_with_timestamp(bucket_name: str) -> str:
    s3 = s3_client()

    # Create a new folder with the current date and time in YYYY-MM-DD-HHMMSS format
    timestamp = datetime.now().strftime('%Y-%m-%d-%H%M%S')
    new_folder_name = f"{timestamp}/"

    # Create the folder by uploading an empty object with the folder name
    s3.put_object(Bucket=bucket_name, Key=new_folder_name)

    return new_folder_name


def upload_immutable_directory_to_s3(local_directory: str, bucket_name: str, s3_folder: str):
    s3 = s3_client()

    uploads = 0
    console = Console()
    with console.status("[green]Initializing immutable backup...[/green]") as status:
        for root, dirs, files in os.walk(local_directory):
            for filename in files:
                try:
                    local_path = os.path.join(root, filename)
                    relative_path = os.path.relpath(local_path, local_directory)
                    s3_key = os.path.join(s3_folder, relative_path)
                    status.update(status=f'Uploading [gold1]"{s3_key}"[/] -> [orange1]"{bucket_name}"[/]...')
                    # Upload the file
                    s3.upload_file(local_path, bucket_name, s3_key, ExtraArgs={'StorageClass': 'DEEP_ARCHIVE'})
                    uploads += 1
                except Exception as e:
                    print(f"[red]Error uploading {s3_key}: {e}[/]")
    print(f"Total files uploaded: {uploads}")
