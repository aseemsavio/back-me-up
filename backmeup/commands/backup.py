from rich.panel import Panel
from rich.text import Text

from backmeup.services.sqlite import connect_to_db, Backup, create_new_backup_in_db, list_all_backups_from_db, \
    delete_backup_by_id, get_backup_by_id_from_db
from backmeup.utils import print_error
from backmeup.utils.files import scan_directory
from backmeup.utils.misc import current_timestamp_ms
from rich.console import Console
from rich.table import Table
from rich import print


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


def delete_backup(backup_id: int):
    connection = connect_to_db()
    delete_backup_by_id(connection=connection, backup_id=backup_id)


def scan_backup_location(backup_id: int):
    connection = connect_to_db()
    backup = get_backup_by_id_from_db(connection=connection, backup_id=backup_id)

    if backup:
        path = backup.source_absolute_path
        info = scan_directory(path)

        console = Console()

        # Creating styled text for each key-value pair
        folder_count = Text(f"Folder Count: {info['folder_count']}", style="bold cyan")
        file_count = Text(f"File Count: {info['file_count']}", style="bold cyan")
        total_size_bytes = Text(f"Total Size (Bytes): {info['total_size_bytes']}", style="bold green")
        total_size_gb = Text(f"Total Size (GB): {info['total_size_gb']:.6f}", style="bold green")
        absolute_path = Text(f"Absolute Path: {info['absolute_path']}", style="bold magenta")

        # Adding the text to a panel
        panel_content = '\n'.join(
            [str(folder_count), str(file_count), str(total_size_bytes), str(total_size_gb), str(absolute_path)])
        panel = Panel(panel_content, title="Directory Information", title_align="left", border_style="bold yellow")

        # Print the panel
        console.print(panel)
    else:
        print_error("Could not find the provided backup set.")
