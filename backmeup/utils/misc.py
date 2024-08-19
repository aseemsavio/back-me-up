import sys
from pathlib import Path
import os
import time


def get_data_base_path_for_os() -> Path:
    # Determine the base directory based on the operating system
    if os.name == 'nt':  # Windows
        return Path(os.getenv('APPDATA')) / 'Backmeup'
    elif os.name == 'posix':  # macOS or Linux
        if sys.platform == 'darwin':  # macOS
            return Path.home() / 'Library' / 'Application Support' / 'Backmeup'
        else:  # Linux
            return Path.home() / '.local' / 'share' / 'Backmeup'
    else:
        raise OSError("Unsupported operating system")


def current_timestamp_ms() -> int:
    # Get the current time in milliseconds
    return int(time.time() * 1000)
