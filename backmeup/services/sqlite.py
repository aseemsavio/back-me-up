from dataclasses import dataclass
from pathlib import Path
import sqlite3
from sqlite3 import Connection
from typing import Optional

from backmeup.utils.misc import get_data_base_path_for_os


@dataclass
class Backup:
    id: Optional[int]
    description: str
    created_at: int
    updated_at: int
    source_absolute_path: str
    target_location: str
    mutable_backup: bool


def get_database_path() -> Path:
    base_dir = get_data_base_path_for_os()
    # Ensure the directory exists
    base_dir.mkdir(parents=True, exist_ok=True)

    # Create the full path to the database file
    return base_dir / 'backmeup.db'


def create_backups_table_if_not_exists(connection: Connection):
    cursor = connection.cursor()

    # Create a table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Backup (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            created_at INTEGER NOT NULL,
            updated_at INTEGER NOT NULL,
            source_absolute_path TEXT NOT NULL,
            target_location TEXT NOT NULL,
            mutable_backup BOOLEAN NOT NULL
        );
    ''')

    connection.commit()


def connect_to_db() -> Connection:
    # Connect to the SQLite database
    db_path = get_database_path()
    conn = sqlite3.connect(str(db_path))

    # create all the tables here.
    create_backups_table_if_not_exists(connection=conn)
    return conn


def create_new_backup_in_db(connection: Connection, backup: Backup):
    cursor = connection.cursor()
    insert_query = '''
    INSERT INTO Backup (description, created_at, updated_at, source_absolute_path, target_location, mutable_backup)
    VALUES (?, ?, ?, ?, ?, ?);
    '''
    cursor.execute(
        insert_query, (
            backup.description,
            backup.created_at,
            backup.updated_at,
            backup.source_absolute_path,
            backup.target_location,
            backup.mutable_backup
        )
    )
    connection.commit()
    connection.close()


def list_all_backups_from_db(connection: Connection) -> [Backup]:
    """

    :param connection:
    :return:
    """
    cursor = connection.cursor()
    cursor.execute(
        'SELECT id, description, created_at, updated_at, source_absolute_path, target_location, mutable_backup FROM Backup'
    )
    rows = cursor.fetchall()
    connection.close()
    return [Backup(*row) for row in rows]


def delete_backup_by_id(connection: Connection, backup_id: int):
    cursor = connection.cursor()
    cursor.execute('''
        DELETE FROM Backup
        WHERE id = ?
    ''', (backup_id,))

    connection.commit()
    connection.close()


def get_backup_by_id_from_db(connection: Connection, backup_id: int) -> Optional[Backup]:
    cursor = connection.cursor()
    cursor.execute(
        'SELECT id, description, created_at, updated_at, source_absolute_path, target_location, mutable_backup FROM Backup WHERE id = ?',
        (backup_id,)
    )
    row = cursor.fetchone()
    connection.close()

    if row:
        return Backup(*row)
    else:
        return None
