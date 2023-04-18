import os


def check_path(provided_path):
    if not os.path.exists(provided_path):
        raise FileNotFoundError("Provided a path that does not exist")
    if not os.path.isdir(provided_path):
        raise NotADirectoryError("Path not to a directory is provided")
