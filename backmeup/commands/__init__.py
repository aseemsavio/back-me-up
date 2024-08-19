from typing import Optional

from typer import Typer, Option

from backmeup.commands.backup import create_backup_set, list_all_backups
from backmeup.commands.configuration import configure_cli, reset_cli
from rich.table import Table


def register_commands(cli: Typer):
    """
    This function contains the logic to register the commands in this CLI.

    :param cli:
    :return:
    """

    @cli.command(
        name="setup",
        help="Sets up the backmeup CLI."
    )
    def setup(
            location: Optional[str] = Option(
                "s3",
                "--location",
                "-l",
                help="Backs up your files to AWS S3 Glacier Deep Archive."
            ),
            access_key: Optional[str] = Option(None, "--access", "-a", help="Access Key to AWS S3"),
            secret_key: Optional[str] = Option(None, "--secret", "-s", help="Secret Key to AWS S3"),
            region: Optional[str] = Option(None, "--region", "-r", help="Default region for AWS S3")
    ):
        configure_cli(
            location=location,
            access_key=access_key,
            secret_key=secret_key,
            region=region
        )

    @cli.command(
        name="reset",
        help="Resets the backmeup CLI."
    )
    def reset():
        reset_cli()

    @cli.command(
        name="create",
        help="Creates a new backup set. This set can be accessed by their id while doing your backup."
    )
    def create(
            description: str = Option(..., "--description", "-d", help="Description for the new backup"),
            path: str = Option(...,
                               "--path",
                               "-p",
                               help="Absolute path of the directory you wish to backup"
                               ),
            target: str = Option(..., "--target", "-t", help="Where you want the backup to be stored in"),
            mutable: bool = Option(False, "--mutable", "-m", help="A boolean flag to make the backup mutable.")
    ):
        create_backup_set(
            description=description,
            path=path,
            target=target,
            mutable=mutable
        )

    @cli.command(
        name="list",
        help="List all the backups configured."
    )
    def list_backups():
        list_all_backups()
