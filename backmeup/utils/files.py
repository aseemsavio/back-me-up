import os


def scan_directory(abs_path: str) -> dict:
    """
    Retrieves information about a directory, including the number of folders,
    total number of files, and the total size of all files.

    :param abs_path: The absolute path to the directory.
    :return: A dictionary with folder count, file count, total size, and more.
    """
    folder_count = 0
    file_count = 0
    total_size = 0

    for dirpath, dirnames, filenames in os.walk(abs_path):
        # Count folders
        folder_count += len(dirnames)

        # Count files and accumulate total size
        file_count += len(filenames)
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)

    return {
        'folder_count': folder_count,
        'file_count': file_count,
        'total_size_bytes': total_size,
        'total_size_gb': total_size / (1024 * 1024 * 1024),
        'absolute_path': abs_path
    }
