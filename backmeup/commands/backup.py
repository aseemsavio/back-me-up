from backmeup.services.sqlite import connect_to_db, Backup, create_new_backup_in_db, list_all_backups_from_db
from backmeup.utils.misc import current_timestamp_ms
from rich.console import Console
from rich.table import Table


def create_backup_set(
        description: str,
        path: str,
        target: str,
        mutable: bool
):
    connection = connect_to_db()
    now = current_timestamp_ms()
    backup = Backup(
        id=None,
        description=description,
        created_at=now,
        updated_at=now,
        source_absolute_path=path,
        target_location=target,
        mutable_backup=mutable
    )
    create_new_backup_in_db(connection=connection, backup=backup)


def list_all_backups():
    """

    :return:
    """
    connection = connect_to_db()
    backups = list_all_backups_from_db(connection)

    table = Table(title="Backup Sets", header_style="bold bright_white", border_style="dim")

    table.add_column("ID", style="dim")
    table.add_column("Description")
    table.add_column("Path")
    table.add_column("Target")

    for b in backups:
        table.add_row(str(b.id), b.description, b.source_absolute_path, b.target_location)

    console = Console()
    console.print(table)
