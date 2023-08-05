import json
import os
import unittest
from unittest import mock
import shutil

import docopt
import nixio as nix

from nixconverter import eegbase_nix_converter
from nixconverter.utils import utils, conf

# importing the doc string from the eegbase_nix_converter
DOCOPT = eegbase_nix_converter.__doc__


class TestInputFileParsing(unittest.TestCase):
    def init_converter(self, docopt_params):
        with open('nixconverter/brainvisionconverter/brainvision_mapping.json') as mapping:
            with mock.patch('os.walk', return_value=[
                ('/foo', ('data',), ('metadata.xml',)),
                ('/foo/data', (), ('Experiment_01.vhdr', 'Experiment_01.eeg', 'Experiment_01.vmrk')),
            ]), \
                 mock.patch('nixconverter.eegbase_nix_converter.EEGBaseNixConverter.parse_input_path', return_value=0), \
                 mock.patch('builtins.open', mock.mock_open(read_data=mapping.read())):
                self.docopt = docopt.docopt(DOCOPT, docopt_params)
                self.converter = eegbase_nix_converter.EEGBaseNixConverter(
                    docopt_parser=self.docopt
                )

    def setUp(self):
        self.init_converter(['DATASET'])

    def test_convert(self):
        """
        This Test Case covers the whole conversion process, using the test data and testing the actual output file
        """
        self.init_converter(['tests/data/eegbase/Experiment_P3_Numbers', "--output=tests/data/nix"])
        with mock.patch.object(self.converter, "datasets", ['tests/data/eegbase/Experiment_P3_Numbers']), \
                mock.patch('builtins.input', return_value='y'):
            with open('tests/data/odml/odml_test_mapping.json') as mapping:
                with mock.patch('nixconverter.odmlconverter.mapper.OdmlMapper.get_mapping', return_value=json.load(mapping)):
                    self.converter.convert()
                    self.assertTrue(
                        os.path.exists('tests/data/nix/Experiment_P3_Numbers/Experiment_P3_Numbers.nix'))
                    actual = nix.File.open('tests/data/nix/Experiment_P3_Numbers/Experiment_P3_Numbers.nix')
                    self.assertTrue(
                        os.path.exists('tests/data/nix/Experiment_P3_Numbers/Experiment_P3_Numbers.nix'))
                    self.assertIn("P3Numbers_20150618_f_11_001 Metadata", actual.sections)
                    self.assertIn("Session metadata", actual.sections)
                    self.assertIn("P3Numbers_20150618_f_11_001", actual.blocks[conf.NIX_BLOCK_NAME].groups)
                    self.assertIn("P3Numbers_20150618_f_11_001",
                                  actual.blocks[conf.NIX_BLOCK_NAME].groups["P3Numbers_20150618_f_11_001"].data_arrays)
                    self.assertEqual(
                        (4, 273267),
                        actual.blocks[conf.NIX_BLOCK_NAME].groups["P3Numbers_20150618_f_11_001"].data_arrays[
                            "P3Numbers_20150618_f_11_001"].data_extent
                    )
                    self.assertTrue(os.path.exists(
                        'tests/data/nix/Experiment_P3_Numbers/Data/P3Numbers_20150618_f_11_001.txt'))
                    self.assertTrue(os.path.exists(
                        'tests/data/nix/Experiment_P3_Numbers/Scenario/numbers.zip'))
                    shutil.rmtree('tests/data/nix')

    def test_missing_extension_file(self):
        with mock.patch('os.walk') as mock_walk:
            mock_walk.return_value = [
                ('/Experiment_01', ('data',), ('metadata.xml',)),
                ('/Experiment_01/data', (), ('Experiment_01.eeg', 'Experiment_01.vmrk')),
            ]
            with self.assertRaises(utils.MissingFileException):
                self.converter.walk_directory_for_extension('/Experiment_01', '.vhdr', True)

    def test_create_nix_file_exists(self):
        with mock.patch('os.path.exists', return_value=True), \
                mock.patch('builtins.input', return_value='n'):
            with self.assertRaises(utils.ExistingFileException):
                self.converter.create_nix_file('nix_file_path', ['Experiment_01.vmrk'], 'metadata.xml')

    def test_walking_directory(self):
        with mock.patch('os.walk') as mockwalk:
            mockwalk.return_value = [
                ('/Experiment_01', ('data',), ('metadata.xml',)),
                ('/Experiment_01/data', (), ('Experiment_01.vhdr', 'Experiment_01_A.vhdr')),
            ]

            actual = self.converter.walk_directory_for_extension('/Experiment_01', '.vhdr', True)
            expected = ['/Experiment_01/data/Experiment_01.vhdr', '/Experiment_01/data/Experiment_01_A.vhdr']

            self.assertCountEqual(expected, actual)
            self.assertEqual(expected, actual)

    def test_get_experiment_name(self):
        actual = utils.get_experiment_name('/Experiment_01/data/Experiment_01_A.vhdr')
        expected = 'Experiment_01_A.vhdr'
        self.assertEqual(expected, actual)

    def test_parse_params(self):
        with mock.patch('os.path.exists', return_value=True):
            with mock.patch('os.listdir', return_value=['Experiment_01', 'Experiment_02']):
                self.init_converter(['DATASET', "-m"])
                self.converter.parse_params(self.docopt)
                self.assertEqual(True, self.converter.multiple_conversions)
                self.assertEqual(False, self.converter.console_output)
                self.assertEqual(False, self.converter.keep_terminologies)
                expected_output_dir = conf.NIX_FILE_OUTPUT_DIR + "DATASET/"
                self.assertEqual(expected_output_dir, self.converter.output_dir)
                self.assertEqual(2, self.converter.found_datasets)

    def test_parse_params_custom_mapping(self):
        with mock.patch('os.path.exists', return_value=True), \
                mock.patch('os.getcwd', return_value='/path/to'):
            self.init_converter(['DATASET', "--mapping=file.json", "-v"])
            self.converter.parse_params(self.docopt)
            self.assertEqual(False, self.converter.multiple_conversions)
            self.assertEqual(True, self.converter.console_output)
            self.assertEqual('/path/to/file.json', self.converter.custom_mapping)

    def test_parse_input_path_single(self):
        with mock.patch('os.path.exists', return_value=True), \
                mock.patch.object(self.converter, "multiple_conversions", False):
            self.converter.parse_input_path('/path/to/dataset')
            expected = ['/path/to/dataset']
            self.assertEqual(expected, self.converter.datasets)
            self.assertEqual(1, self.converter.found_datasets)

    def test_parse_input_path_multiple(self):
        with mock.patch('os.path.exists', return_value=True), \
                mock.patch.object(self.converter, "multiple_conversions", True), \
                mock.patch('os.listdir', return_value=['Experiment_01', 'Experiment_02']):
            self.converter.parse_input_path('/path/to/dataset')
            expected = ['/path/to/dataset/Experiment_01', '/path/to/dataset/Experiment_02']
            self.assertEqual(expected, self.converter.datasets)
            self.assertEqual(2, self.converter.found_datasets)

    def test_parse_input_path_multiple_no_subdirectories(self):
        with mock.patch('os.path.exists', return_value=True), \
                mock.patch.object(self.converter, "multiple_conversions", True), \
                mock.patch('os.listdir', return_value=[]):
            with self.assertRaises(utils.MissingFileException):
                self.converter.parse_input_path('/path/to/dataset')

    def test_parse_input_path_incorrect_path(self):
        with mock.patch('os.path.exists', return_value=False):
            with self.assertRaises(utils.MissingFileException):
                self.converter.parse_input_path('/path/to/dataset')


if __name__ == '__main__':
    unittest.main()
