"""EEGbase NIX converter

For more information, see https://gitlab.com/honza.seda/eegbase-nix-converter

EEGbase -> NIX converter converts BranVision/odML dataset to a NIX container file

Usage:
    eegbase_nix_converter DATASET [--output=<path>] [-m] [-t|--mapping=<path>] [-v] [-y]
    eegbase_nix_converter -h | --help

Arguments:
    DATASET         Path to the directory with the dataset.
                    Path is expected to be relative from the script execution directory.

                    By default, the script expects the directory to contain a single dataset
                    and will create a single NIX file.
                    If you want to change this behaviour and convert multiple datasets at a time,
                    you can do so by passing the --multiple (-m) option, which will interpret the DATASET as
                    parent directory and expect every immediate subfolder to be a dataset folder (will run
                    the conversion on every subfolder in the passed directory).

                    The tool will attempt by default to convert the odML (.xml) metadata to use the odML terminology.
                    The mapping to the odML terminologies uses a predefined mapping JSON file.
                    To use custom mapping, pass the path to a JSON file with the --mapping=<path> option.
                    The mapping file can be generated using the mapping_generator.py script.
                    To prevent this and use the original terminologies or not add any terminologies at all,
                    pass the --keep-terminologies (-t) option with the script


Options:
    -v --verbose                Output detailed logging information to console
    -m --multiple               Will handle the passed path as a folder containing
                                multiple datasets in separate directories
    --output=<path>             Specify the output directory for the converted files. If the path does not exist,
                                it will be created
    -t --keep-terminologies     Keep the terminologies from the original odML metadata
    -mapping=<path>             Path to a JSON mapping file
    -y                          Always replaces already existing files
    -h --help                   Show this screen.
"""
import logging
import os
import sys
from shutil import copy2 as copy
from docopt import docopt
import nixio as nix
import mne

from nixconverter.utils import conf
from nixconverter.utils import utils
from nixconverter.brainvisionconverter import converter as brainvision_converter
from nixconverter.odmlconverter import converter as odml_converter


class EEGBaseNixConverter:
    """
    Class handling the parsing of the dataset and conversion of the EEGbase BrainVision/odML files to NIX
    """

    found_datasets = 0
    console_output = False
    multiple_conversions = False
    keep_terminologies = False
    custom_mapping = None
    overwrite_existing = False
    output_dir = conf.NIX_FILE_OUTPUT_DIR
    skipped_files = list()

    def __init__(self, docopt_parser):
        self.datasets = []
        try:
            self.parse_params(docopt_parser)
        except utils.MissingFileException as ex:
            print(ex.message)
            sys.exit(ex.exit_code)
        self.brainvision_converter = brainvision_converter.BrainVisionConverter(console_output=self.console_output)
        self.odml_converter = odml_converter.OdmlConverter(
            keep_terminologies=self.keep_terminologies,
            custom_mapping=self.custom_mapping,
            console_output=self.console_output
        )

    def parse_params(self, parser):
        """
        Parses the docopt script parameters and options and saves them to class properties

        :param parser: docopt parameters
        :type parser: dict

        :raises MissingFileException if dataset path is not valid
        """
        self.console_output = parser['--verbose']
        if not self.console_output:
            logger = logging.getLogger('mne')
            logger.setLevel('ERROR')

        self.multiple_conversions = parser['--multiple']
        self.keep_terminologies = parser['--keep-terminologies']
        self.overwrite_existing = parser['-y']
        if parser['--output']:
            self.output_dir = utils.parse_path(parser['--output'])
            if not self.output_dir.endswith(os.sep):
                self.output_dir += os.sep
        if parser['--mapping']:
            mapping_path = utils.parse_path(parser['--mapping'], False)
            if not os.path.exists(mapping_path):
                raise utils.MissingFileException("The mapping file path does not exist.")
            self.custom_mapping = mapping_path
        dataset_arg = parser['DATASET']
        self.parse_input_path(dataset_arg)

    def parse_input_path(self, dataset_dir):
        """
        Parses the user given path representing the dataset directory.

        If the --multiple option is used, the path is scanned for immediate subdirectories and treats every directory
        as a dataset on which the conversion will be attempted

        :param dataset_dir: path from the script argument
        :type dataset_dir: str

        :raises MissingFileException if path is not valid
        """
        if not os.path.exists(dataset_dir):
            raise utils.MissingFileException("Given path does not exist! Aborting the conversion.")

        dataset_dir = utils.parse_path(dataset_dir)

        if self.multiple_conversions:
            if self.multiple_conversions:
                experiment_name = utils.get_experiment_name(dataset_dir)
                self.output_dir += experiment_name + os.sep
            for dataset in os.listdir(dataset_dir):
                if os.path.isdir(os.path.join(dataset_dir, dataset)):
                    dataset_path = dataset_dir + os.sep + dataset
                    self.datasets.append(dataset_path)
            self.found_datasets = len(self.datasets)
            if self.found_datasets == 0:
                raise utils.MissingFileException(
                    "No immediate subdirectories found in given path! When using the -m option, "
                    "make sure to pass a directory that contains dataset subfolders."
                )

            utils.console_output_text(
                f"Found {self.found_datasets} dataset directories in given path.",
                console_output=self.console_output
            )
        else:
            self.datasets.append(dataset_dir)
            self.found_datasets = 1

    def convert(self):
        """
        The entry point method to start the conversion on passed dataset(s).
        Converts every dataset to NIX and adds any other files that are in the original dataset folder
        """
        for idx, dataset_dir in enumerate(self.datasets):
            if self.multiple_conversions:
                print(f"Converting dataset {idx + 1} out of {self.found_datasets} found...")
            try:
                cwd = os.getcwd()
                if dataset_dir[0] == os.sep:
                    full_search_path = dataset_dir
                else:
                    full_search_path = cwd + os.sep + dataset_dir

                bv_header_files = self.walk_directory_for_extension(full_search_path, ".vhdr", True)
                metadata_files = self.walk_directory_for_extension(full_search_path, ".xml", True)

                file_path = self.output_dir + utils.get_experiment_name(dataset_dir) + os.sep
                nix_file_path = file_path + utils.get_experiment_name(
                    dataset_dir) + conf.NIX_FILE_EXTENSION

                # if the output directory is not created yet, create it
                if not os.path.exists(file_path):
                    os.makedirs(file_path)

                # create the NIX file from BrainVision and odML files
                self.create_nix_file(nix_file_path, bv_header_files, metadata_files[0])

                # copy any remaining files to the converted dataset
                self.add_remaining_files(file_path, metadata_files[0], bv_header_files)
            except utils.MissingFileException as ex:
                print(ex.message)
                continue
            except utils.ExistingFileException as ex:
                print(ex.message)
                continue

    def convert_data(self, nix_file, bv_files, metadata_file):
        """
        Creates a 'Block' that represents a grouping object, the recording session.
        # compresses the entire block data with nix.Compression.DeflateNormal

        Iterates all the BrainVision header files and converts the data and metadata,
        each header file is separated into its own group

        :param nix_file: the NIX file resource
        :type nix_file: nix.File
        :param bv_files: all the BrainVision header files found
        :type bv_files: list
        :param metadata_file: path to the .xml file containing odML metadata about the experiment
        :type metadata_file: str
        """
        block = nix_file.create_block(
            conf.NIX_BLOCK_NAME,
            conf.NIX_BLOCK_TYPE,
            compression=nix.Compression.DeflateNormal
        )

        for header_file in bv_files:
            try:
                print(f"Converting BrainVision header and its data from {os.path.basename(header_file)}")
                # Default scale is 1 for V, for unit=uV and resolution=0.1 set scale to scale=100000
                raw_bv = mne.io.brainvision.read_raw_brainvision(header_file, verbose=None)
                header_props = utils.HeaderProperties(
                    header_file=header_file,
                    file_path=raw_bv.filenames[0]
                )
                self.brainvision_converter.register_data_blocks(block, raw_bv, header_props)
                self.brainvision_converter.append_data_info(nix_file, raw_bv, header_props)
            except FileNotFoundError as missing_file:
                self.skipped_files.append((header_file, missing_file))
            except nix.exceptions.exceptions.DuplicateName as duplicate_data_array:
                self.skipped_files.append((header_file, duplicate_data_array))

        print(f"Converting the odML metadata from {os.path.basename(metadata_file)}")
        self.odml_converter.append_experiment_metadata(nix_file, metadata_file)

    def create_nix_file(self, nix_file_path, bv_header_files, metadata_file):
        """
        The main handler for creating the nix file from the given dataset directory

        :param nix_file_path: path to the output NIX file
        :type nix_file_path: str
        :param bv_header_files: lsit of paths to the BranVision recording files
        :type bv_header_files: list
        :param metadata_file: path to the .xml file containing odML metadata about the experiment
        :type metadata_file: str
        :raises ExistingFileException raised if file already exists and user does not wish to replace it
        """

        # find the necessary files in dataset directory
        utils.console_output_text(
            "Starting the dataset conversion",
            console_output=self.console_output
        )

        utils.console_output_text(
            f"Creating the NIX file in '{nix_file_path}'",
            console_output=self.console_output
        )
        if os.path.exists(nix_file_path):
            if self.overwrite_existing:
                utils.console_output_text(
                    f"File {os.path.basename(nix_file_path)} already exists. Overwriting the existing file.",
                    console_output=self.console_output
                )
            else:
                # if the output file already exists, confirm replacement
                replace_existing = input(f"File {os.path.basename(nix_file_path)} already exists. Replace (y/n)? ")
                if replace_existing.lower() not in ("y", "yes"):
                    raise utils.ExistingFileException(
                        "File will not be replaced, skipping the conversion for this directory.")

            os.remove(nix_file_path)

        # create a new NIX file overwriting any existing content
        nix_file = nix.File.open(nix_file_path, nix.FileMode.ReadWrite)
        self.skipped_files = []
        self.convert_data(nix_file, bv_header_files, metadata_file)
        nix_file.close()
        print(f"Conversion of file {os.path.basename(nix_file_path)} completed.")
        if len(self.skipped_files) != 0:
            print("WARNING: The following files were not included in the conversion due to the following errors:")
            for skipped in self.skipped_files:
                print(f"Header file '{skipped[0]}': {skipped[1]}")
        print("===============================")

    def walk_directory_for_extension(self, full_search_path, ext, required=True):
        """
        Walks the given directory and returns a list of files (full paths) ending with specified file extension

        :param full_search_path: full path to walk
        :type full_search_path: str
        :param ext: str file extension to search for
        :type ext: str
        :param required: if set to True, the script will raise exception if no files are found
        :type required: bool

        :raises MissingFileException when no file is found and the `required` param is set to True

        :returns a list of absolute paths to every file found in directory with specified file extension
        :rtype list
        """
        files = []

        utils.console_output_text(
            f"Searching for {ext} dataset files in directory '{full_search_path}'",
            console_output=self.console_output
        )
        for filenames in os.walk(full_search_path):
            for file_list in filenames:
                for file_name in file_list:
                    if file_name.endswith(ext):
                        files.append(filenames[0] + os.sep + file_name)
        if required and not files:
            raise utils.MissingFileException(
                f"Error! No files with extension {ext} found in directory  '{full_search_path}'")

        found_files = '\n'.join(files)
        utils.console_output_text(
            f"Found following {ext} files:\n" + found_files,
            console_output=self.console_output
        )

        return files

    def add_remaining_files(self, output_path, metadata_path, bv_header_files):
        """
        Adds any remaining file from the dataset folder to the output folder

        :param output_path: output folder
        :type output_path: str
        :param metadata_path: path to the odML metadata file
        :type metadata_path: str
        :param bv_header_files: list of the BrainVision header files
        :type bv_header_files: list
        """
        utils.console_output_text("Adding remaining dataset files to the output path", self.console_output)
        skip_files = {metadata_path}
        for header in bv_header_files:
            try:
                # pylint: disable=protected-access
                raw_vhdr_info = mne.io.brainvision.brainvision._get_vhdr_info(header, [], 'auto', 1)
                skip_files.add(header)
                # Data filename
                skip_files.add(raw_vhdr_info[1])
                # Marker filename
                skip_files.add(raw_vhdr_info[5])
            except FileNotFoundError:
                utils.console_output_text(
                    f"Missing files! Original BrainVision files will be copied for header {header}",
                    self.console_output
                )

        experiment_root_path = os.path.dirname(metadata_path)
        for root, _, files in os.walk(experiment_root_path):
            for file in files:
                full_file_path = root + os.sep + file
                if full_file_path in skip_files:
                    continue
                file_path = full_file_path[len(experiment_root_path):] if full_file_path.startswith(
                    experiment_root_path) else file
                copy_path = output_path.rstrip(os.sep) + file_path
                if not os.path.exists(os.path.dirname(copy_path)):
                    os.makedirs(os.path.dirname(copy_path))
                copy(full_file_path, copy_path)


def main(args=None):
    """
    The script entrypoint function

    :param args: script arguments
    """
    parser = docopt(__doc__, argv=args)
    converter = EEGBaseNixConverter(docopt_parser=parser)
    converter.convert()
    print("Conversion done.")


if __name__ == "__main__":
    main(sys.argv[1:])
