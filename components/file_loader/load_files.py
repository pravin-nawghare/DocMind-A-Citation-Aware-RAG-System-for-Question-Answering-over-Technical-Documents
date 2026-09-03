import os


def load_files_from_directory(directory_path: str):
    """
    Load all files from the specified directory and return a list of file paths.

    Args:
        directory_path (str): The path to the directory containing files.

    Returns:
        list: A list of file paths.
    """
    file_paths = []
    for root, dirs, files in os.walk(directory_path):
        for filename in files:
            file_paths.append(os.path.join(root, filename))
    return file_paths