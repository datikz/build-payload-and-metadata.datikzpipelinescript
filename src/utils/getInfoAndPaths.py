"""Implementation of function that performs recursive search in a given folder"""
import os


def getInfoAndPaths(directory_path):
    """Gets information about files or other things in a certain directory.

    Parameters
    ----------
    directory_path: str
        Path of the folder in which to perform the search

    Returns
    -------
    buffer_data: list[dict]
        Information researched in a list with dictionaries
        dict:
            file: str
            path: str
    """
    buffer_data = []
    for path, _, filenames in os.walk(directory_path):
        buffer_data += [{"file": filename, "path": path} for filename in filenames]
    return buffer_data
