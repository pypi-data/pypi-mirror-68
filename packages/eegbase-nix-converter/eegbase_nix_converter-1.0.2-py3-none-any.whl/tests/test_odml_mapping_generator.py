"""
Unit tests covering the mapping_generator.py script
"""

import unittest
from unittest import mock
from odml.tools import ODMLReader

from nixconverter.odmlconverter import mapping_generator
from tests.data.odml import odml_test_data


class TestOdmlMappingGenerator(unittest.TestCase):
    def setUp(self):
        self.odml_input = ODMLReader().from_string(bytes(odml_test_data.TEST_ODML_FILE, 'utf-8'))
        self.mapping_generator = mapping_generator.OdmlMappingGenerator()

    def test_build_parent_string_root_section(self):
        """
        Tests if an input section has the document root as a parent section
        """
        test_section = self.odml_input.sections['Experiment'].parent
        actual = self.mapping_generator.build_parent_string(test_section)
        expected = ""
        self.assertEqual(expected, actual)

    def test_build_parent_string_single_section(self):
        """
        Tests if an input section has a single parent section
        """
        test_section = self.odml_input.sections['Experiment']
        actual = self.mapping_generator.build_parent_string(test_section)
        expected = "experiment__Experiment"
        self.assertEqual(expected, actual)

    def test_build_parent_string_nested_section(self):
        """
        Tests if an input section has nested parent section
        """
        test_section = self.odml_input.sections['Devices'].sections['Response button']
        actual = self.mapping_generator.build_parent_string(test_section)
        expected = "collection__Devices___hardware__Response button"
        self.assertEqual(expected, actual)

    def test_odml_recurse(self):
        expected = odml_test_data.GENERATED_STRUCTURE
        actual = dict()
        self.mapping_generator.odml_recurse(self.odml_input, actual)

        self.assertTrue(len(actual) != 0)
        self.assertDictEqual(expected, actual)

    def test_generate(self):
        with mock.patch('os.walk') as mock_walk, \
                mock.patch('os.path.exists') as mock_path_exists, \
                mock.patch('odml.load') as mock_odml_load:
            mock_walk.return_value = [
                ('/Experiment_01', ('data',), ('metadata.xml',)),
                ('/Experiment_01/data', (), ('Experiment_01.vhdr', 'Experiment_01.eeg', 'Experiment_01.vmrk')),
            ]
            mock_path_exists.return_value = True
            mock_odml_load.return_value = self.odml_input

            actual = self.mapping_generator.generate('input.xml')
            expected = odml_test_data.GENERATED_STRUCTURE
            self.assertDictEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
