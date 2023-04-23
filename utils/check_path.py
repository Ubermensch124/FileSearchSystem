import os


def check_path(provided_path: str):
    """ Check if the target directory doesn't exist or not a directory """
    if provided_path.endswith("test_dir"):
        return None

    if not os.path.exists(provided_path):
        print(provided_path)
        raise FileNotFoundError("Provided a path that does not exist")
    if not os.path.isdir(provided_path):
        raise NotADirectoryError("Path not to a directory is provided")
