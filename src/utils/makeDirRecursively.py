"""Implementation of recursive directory creation function"""
from os import mkdir, path


def mkdirR(path_folder):
    """Creates the folders in the path if they do not exist to satisfy the requirement

    Parameters
    ----------
    path_folder: str
        Path separated by '/' indicating the folders you require to be created

    Returns
    -------
    None"""
    print("Creating", path_folder)
    path_folder = [i for i in path_folder.split("/") if i]
    for i in range(1, len(path_folder) + 1):
        to_create = "/".join(path_folder[:i])
        if not path.isdir(to_create) and to_create:
            mkdir(to_create)
