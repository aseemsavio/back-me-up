from typer import Typer, Context

from backmeup.commands import register_commands

cli = Typer()


@cli.callback(invoke_without_command=True)
def features_callback(ctx: Context):
    # Execute this only if there is no sub command.
    # https://typer.tiangolo.com/tutorial/commands/context/#exclusive-executable-callback
    try:
        if ctx.invoked_subcommand is None:
            print("Backmeup CLI")
    except Exception:
        pass


register_commands(cli)
