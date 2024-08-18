from typer import Typer
from rich import print


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
    def setup():
        """

        :return:
        """

    @cli.command(
        name="create",
        help="Creates a new backup set."
    )
    def create():
        """

        :return:
        """
        print("Hello World")
