"""
Module containing helper functions, classes and exceptions used across the conversion script
"""
import os
from nixconverter.utils import conf


# ===============================
# Helper functions

def console_output_text(text, console_output=False):
    """
    Prints passed text to console only ff the script was called with the output option.

    :param text: String to be printed out to console
    :type text: str
    :param console_output: Flag if console text can be outputted
    :type console_output: bool
    """
    if console_output:
        print(text)


def parse_path(path, is_dir=True):
    """
    Parses the path from the script arguments. (Makes the path the full search path if a relative path is passed)

    :param path: path string to parse
    :type path: str
    :param is_dir: sets if the last name should be treated as a directory instead of a file
    :type is_dir: bool
    :returns the full search path
    :rtype str
    """
    if is_dir:
        path = path.rstrip('/')

    if path[0] == os.sep:
        full_search_path = path
    else:
        cwd = os.getcwd()
        full_search_path = cwd + os.sep + path.lstrip('./')

    return full_search_path


def get_experiment_name(dataset_dir):
    """
    Creates the experiment name from the most nested directory name

    :arg dataset_dir: Path to the directory containing the dataset, relative path from the script location
    :type dataset_dir: str

    :returns the experiment name
    :rtype str
    """
    dir_list = dataset_dir.split(os.sep)
    return dir_list[-1]


# ===============================
# Helper classes

class HeaderProperties:
    """
    Class for storing needed properties to create necessary NIX names and types for a BrainVision header file
    """
    def __init__(self, header_file, file_path):
        """
        Takes the header file full path and creates the necessary properties from the header file name

        :param file_path: full path to a header file
        :type file_path: str
        """
        self.header_file = header_file
        self.data_file = os.path.basename(file_path)
        split_data_file = os.path.splitext(self.data_file)
        self.data_file_name = split_data_file[0]
        self.data_file_ext = split_data_file[1]

    def get_block_data_type(self):
        """
        :returns the name for a data_array NIX entity of a header file
        :rtype str
        """
        return f"{conf.NIX_DATA_TYPE}.{self.data_file_ext[1:]}"

    def get_metadata_data_type(self):
        """
        :returns the name for a NIX metadata section of a header file
        :rtype str
        """
        return f"{conf.NIX_METADATA_TYPE}.{self.data_file_ext[1:]}"


# ===============================
# Exceptions

class MissingFileException(Exception):
    """
    Exception for missing files needed for conversion
    """
    def __init__(self, message=None):
        super(MissingFileException, self).__init__(message)
        self.exit_code = 2
        self.message = message


class ExistingFileException(Exception):
    """
    Exception for trying to convert to existing file
    """
    def __init__(self, message=None):
        super(ExistingFileException, self).__init__(message)
        self.exit_code = 3
        self.message = message
