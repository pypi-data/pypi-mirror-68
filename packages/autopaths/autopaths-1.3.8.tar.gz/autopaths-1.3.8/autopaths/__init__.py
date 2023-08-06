# Special variables #
__version__ = '1.3.8'

# Built in modules #
import os

# This is done to avoid circular import errors #
from autopaths import common
from autopaths import file_size
from autopaths import file_permissions
from autopaths import base_path
from autopaths import file_path
from autopaths import dir_path
from autopaths import tmp_path
from autopaths import auto_paths

###############################################################################
def Path(path):
    # Cast to string #
    path = str(path)
    # Return either a file or a directory path #
    if os.path.isdir(path) or path.endswith('/'):
        return dir_path.DirectoryPath(path)
    else:
        return file_path.FilePath(path)
