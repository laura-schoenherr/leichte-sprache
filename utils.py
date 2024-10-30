import os


def get_new_file_path(
    file_path: str, suffix: str = '_modified', extension: str | None = None
) -> str:
    """
    Generates a new file path with an optional suffix and/or extension.

    Args:
        file_path (str): The original file path.
        suffix (str, optional): The suffix to add to the file name. Defaults to '_modified'.
        extension (str | None, optional): The desired new file extension. If not provided, it will use the original extension.

    Returns:
        str: The new file path with the specified suffix and/or extension.
    """
    dir_name, file_base = os.path.split(file_path)
    file_name, orig_ext = os.path.splitext(file_base)
    ext = extension if extension else orig_ext
    return os.path.join(dir_name, file_name + suffix + ext)
