"""
Unit tests covering the utils module utils.py
"""
import unittest
from unittest import mock

from nixconverter.utils import conf
from nixconverter.utils import utils


class TestConverterUtils(unittest.TestCase):
    def test_parse_path_file_full(self):
        actual = utils.parse_path('/full/path/to/file.txt', False)
        expected = '/full/path/to/file.txt'
        self.assertEqual(expected, actual)

    def test_parse_path_file_relative(self):
        with mock.patch('os.getcwd') as mock_cwd:
            mock_cwd.return_value = '/cwd/path'
            actual = utils.parse_path('./relative/path/to/file.txt', False)
            expected = '/cwd/path/relative/path/to/file.txt'
            self.assertEqual(expected, actual)

    def test_parse_path_file_relative_alt(self):
        with mock.patch('os.getcwd') as mock_cwd:
            mock_cwd.return_value = '/cwd/path'
            actual = utils.parse_path('relative/path/to/file.txt', False)
            expected = '/cwd/path/relative/path/to/file.txt'
            self.assertEqual(expected, actual)

    def test_parse_path_dir_full(self):
        actual = utils.parse_path('/full/path/to/dir')
        expected = '/full/path/to/dir'
        self.assertEqual(expected, actual)

    def test_parse_path_dir_relative(self):
        with mock.patch('os.getcwd') as mock_cwd:
            mock_cwd.return_value = '/cwd/path'
            actual = utils.parse_path('./relative/path/to/dir')
            expected = '/cwd/path/relative/path/to/dir'
            self.assertEqual(expected, actual)

    def test_parse_path_dir_relative_alt(self):
        with mock.patch('os.getcwd') as mock_cwd:
            mock_cwd.return_value = '/cwd/path'
            actual = utils.parse_path('relative/path/to/dir')
            expected = '/cwd/path/relative/path/to/dir'
            self.assertEqual(expected, actual)

    def test_get_experiment_name(self):
        actual = utils.get_experiment_name('/path/to/experiment/ExperimentName')
        expected = 'ExperimentName'
        self.assertEqual(expected, actual)

    def test_header_properties_get_block_data_type(self):
        header_props = utils.HeaderProperties(
            header_file='/path/to/experiment/ExperimentName/data/Experiment-01.vhdr',
            file_path='Experiment-01.eeg'
        )
        actual = header_props.get_block_data_type()
        expected = f"{conf.NIX_DATA_TYPE}.eeg"
        self.assertEqual(expected, actual)

    def test_header_properties_get_metadata_data_type(self):
        header_props = utils.HeaderProperties(
            header_file='/path/to/experiment/ExperimentName/data/Experiment-01.vhdr',
            file_path='Experiment-01.eeg'
        )
        actual = header_props.get_metadata_data_type()
        expected = f"{conf.NIX_METADATA_TYPE}.eeg"
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()