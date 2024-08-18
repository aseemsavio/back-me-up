from typing import Optional

from typer import Typer, Option
from rich import print

from backmeup.commands.configuration import configure_cli


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
        name="create",
        help="Creates a new backup set."
    )
    def create():
        """

        :return:
        """
        print("Hello World")
