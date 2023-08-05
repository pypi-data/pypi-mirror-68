"""
Unit tests covering the mapper
"""
import datetime
import unittest
from unittest import mock

import numpy as np
import odml
from odml.tools import ODMLReader

from nixconverter.odmlconverter import mapper
from tests.data.odml import odml_test_data


class TestOdmlMapper(unittest.TestCase):
    @staticmethod
    def createDocumentWithSection(name, type):
        """
        Initializes odML document with a defined section
        :param name: Section name
        :type name: str
        :param type: Section type
        :type type: str
        :returns the initialized odML document
        :rtype odml.doc.BaseDocument
        """
        doc = odml.Document()
        doc.create_section(name, type)
        return doc

    @staticmethod
    def createDocumentProperty(name, value, dtype):
        """
        Initializes an odML property

        :param name: Prop name
        :param value: Prop value
        :param dtype: Prop data type
        :returns the odML property
        :rtype odml.property.BaseProperty
        """
        doc = odml.Document()
        section = doc.create_section("Section", "section")
        return section.create_property(name, value, dtype)

    def setUp(self):
        """
        Test Case setUp
        """
        self.mapper = mapper.OdmlMapper()

    def test_map_root_section(self):
        """
        Test Case for mapping a section to root of an odML document
        """
        converted_odml_doc = odml.Document()
        section_mapping = {
            "corresponding_term": {
                "type": "experiment",
                "name": "Experiment",
                "parent_sections": ""
            }
        }
        self.mapper.map_section(converted_odml_doc, section_mapping)
        self.assertIn("Experiment", converted_odml_doc.sections)
        self.assertEqual("experiment", converted_odml_doc.sections["Experiment"].type)

    def test_map_child_section(self):
        """
        Test Case for mapping a section to a single parent section
        """
        converted_odml_doc = odml.Document()
        section_mapping = {
            "corresponding_term": {
                "type": "person",
                "name": "Experimenter",
                "parent_sections": "experiment__Experiment"
            }
        }
        self.mapper.map_section(converted_odml_doc, section_mapping)
        self.assertIn("Experiment", converted_odml_doc.sections)
        self.assertEqual("experiment", converted_odml_doc.sections["Experiment"].type)
        self.assertIn("Experimenter", converted_odml_doc.sections["Experiment"].sections)
        self.assertEqual("person", converted_odml_doc.sections["Experiment"].sections["Experimenter"].type)

    def test_map_nested_sections(self):
        """
        Test Case for mapping a section to nested parent sections
        """
        converted_odml_doc = odml.Document()
        section_mapping = {
            "corresponding_term": {
                "type": "person",
                "name": "Experimenter #1",
                "parent_sections": "experiment__Experiment___collection__Experimenters"
            }
        }
        self.mapper.map_section(converted_odml_doc, section_mapping)
        self.assertIn("Experiment", converted_odml_doc.sections)
        self.assertEqual("experiment", converted_odml_doc.sections["Experiment"].type)
        self.assertIn("Experimenters", converted_odml_doc.sections["Experiment"].sections)
        self.assertEqual("collection", converted_odml_doc.sections["Experiment"].sections["Experimenters"].type)
        self.assertIn("Experimenter #1", converted_odml_doc.sections["Experiment"].sections["Experimenters"].sections)
        self.assertEqual("person", converted_odml_doc.sections["Experiment"].sections["Experimenters"].sections[
            "Experimenter #1"].type)

    def test_map_property_existing_section(self):
        """
        Test case for mapping a property to an already existing section
        """
        converted_odml_doc = self.createDocumentWithSection("Experiment", "experiment")
        property_mapping = {
            "type": "string",
            "example_value": "['P3 Numbers']",
            "corresponding_term": {
                "name": "ProjectName",
                "type": "string",
                "parent_sections": "experiment__Experiment"
            }
        }
        odml_prop = self.createDocumentProperty("start-time", "17.12.2013, 10:08:00", "string")
        self.mapper.map_property(converted_odml_doc, odml_prop, property_mapping)
        self.assertIn("ProjectName", converted_odml_doc.sections["Experiment"].properties)
        self.assertEqual("string", converted_odml_doc.sections["Experiment"].properties["ProjectName"].dtype)

    def test_map_property_new_section(self):
        """
        Test case for mapping a property to a section that does not exist yet
        """
        converted_odml_doc = odml.Document()
        property_mapping = {
            "type": "string",
            "example_value": "['P3 Numbers']",
            "corresponding_term": {
                "name": "ProjectName",
                "type": "string",
                "parent_sections": "experiment__Experiment"
            }
        }
        odml_prop = self.createDocumentProperty("start-time", "17.12.2013, 10:08:00", "string")
        self.mapper.map_property(converted_odml_doc, odml_prop, property_mapping)
        self.assertIn("ProjectName", converted_odml_doc.sections["Experiment"].properties)
        self.assertEqual("string", converted_odml_doc.sections["Experiment"].properties["ProjectName"].dtype)

    def test_map_property_new_section_retype(self):
        """
        Test case for mapping a property to a section that does not exist yet, with a different data type
        of the property from the original
        """
        converted_odml_doc = odml.Document()
        property_mapping = {
            "type": "string",
            "example_value": "['22']",
            "corresponding_term": {
                "name": "RoomTemperature",
                "type": "int",
                "parent_sections": "environment__Environment"
            }
        }
        odml_prop = self.createDocumentProperty("temperature", "23", "string")
        self.mapper.map_property(converted_odml_doc, odml_prop, property_mapping)
        self.assertIn("RoomTemperature", converted_odml_doc.sections["Environment"].properties)
        self.assertEqual("int", converted_odml_doc.sections["Environment"].properties["RoomTemperature"].dtype)

    def test_convert_property_type_string_to_int(self):
        """
        Test case for a property value conversion from string to int
        """
        odml_prop = self.createDocumentProperty("temperature", "23", "string")
        prop_mapping_type = {
            "name": "name",
            "type": "int"
        }
        actual = self.mapper.convert_property_type(odml_prop, prop_mapping_type)
        expected = [23]
        for value in actual:
            self.assertIsInstance(value, int)
        self.assertEqual(expected, actual)

    def test_convert_property_type_string_to_float(self):
        """
        Test case for a property value conversion from string to float
        """
        odml_prop = self.createDocumentProperty("temperature", "23", "string")
        prop_mapping_type = {
            "name": "name",
            "type": "float"
        }
        actual = self.mapper.convert_property_type(odml_prop, prop_mapping_type)
        expected = [23.0]
        for value in actual:
            self.assertIsInstance(value, np.float32)
        self.assertEqual(expected, actual)

    def test_convert_property_type_string_to_datetime(self):
        """
        Test case for a property value conversion from string to datetime
        """
        odml_prop = self.createDocumentProperty("start-time", "17.12.2013, 10:08:00", "string")
        prop_mapping_type = {
            "name": "name",
            "type": "datetime",
            "format": "%d.%m.%Y, %H:%M:%S",
        }
        actual = self.mapper.convert_property_type(odml_prop, prop_mapping_type)
        expected = [datetime.datetime(2013, 12, 17, 10, 8, 0)]
        for value in actual:
            self.assertIsInstance(value, datetime.datetime)
        self.assertEqual(expected, actual)

    def test_convert_property_type_to_string(self):
        """
        Test case for a property value conversion to a string
        """
        odml_prop = self.createDocumentProperty("temperature", 23, "int")
        prop_mapping_type = {
            "name": "name",
            "type": "string"
        }
        actual = self.mapper.convert_property_type(odml_prop, prop_mapping_type)
        expected = ["23"]
        for value in actual:
            self.assertIsInstance(value, str)
        self.assertEqual(expected, actual)

    def test_get_section_existing(self):
        """
        Test case for retrieving an existing section from the odML document
        """
        converted_odml_doc = self.createDocumentWithSection("Experiment", "experiment")
        parent_sections = "experiment__Experiment"
        actual = self.mapper.get_section(converted_odml_doc, parent_sections)
        self.assertIsInstance(actual, odml.section.BaseSection)
        self.assertEqual("Experiment", actual.name)

    def test_get_section_non_existing(self):
        """
        Test case for retrieving a non-existing section from the odML document - should create the section
        """
        converted_odml_doc = odml.Document()
        parent_sections = "experiment__Experiment"
        actual = self.mapper.get_section(converted_odml_doc, parent_sections)
        self.assertIsInstance(actual, odml.section.BaseSection)
        self.assertEqual("Experiment", actual.name)

    def test_append_section(self):
        """
        Test case for appending a new section to an already existing section
        """
        converted_odml_doc = self.createDocumentWithSection("Experiment", "experiment")
        sec = odml.Section(
            name="Experimenter",
            type="person"
        )
        parent_sections = "experiment__Experiment"
        self.mapper.append_section(converted_odml_doc, sec, parent_sections)
        self.assertIn("Experimenter", converted_odml_doc.sections["Experiment"].sections)
        self.assertEqual("person", converted_odml_doc.sections["Experiment"].sections["Experimenter"].type)

    def test_append_reference_new(self):
        """
        Test case for appending a new section to a non-existing section
        """
        converted_odml_doc = self.createDocumentWithSection("Experiment", "experiment")
        sec = odml.Section(
            name="Experimenter",
            type="person"
        )
        sec_reference = {
            "section": "experiment__Experiment",
            "prop": "Experimenter",
            "ref_type": "string",
            "definition": "Contains id references to Experimenters 'person' sections"
        }
        self.mapper.append_reference(converted_odml_doc, sec, sec_reference)
        self.assertIn("Experimenter", converted_odml_doc.sections["Experiment"].properties)
        self.assertTrue(len(converted_odml_doc.sections["Experiment"].properties["Experimenter"].values) == 1)
        self.assertIn(sec.oid, converted_odml_doc.sections["Experiment"].properties["Experimenter"].values)

    def test_append_reference_existing(self):
        """
        Test Case for appending a section reference to an existing property
        """
        converted_odml_doc = self.createDocumentWithSection("Experiment", "experiment")
        prop = converted_odml_doc.sections["Experiment"].create_property("Experimenter", "string")
        prop.values = ["ref-01-123-456"]
        sec = odml.Section(
            name="Experimenter",
            type="person"
        )
        sec_reference = {
            "section": "experiment__Experiment",
            "prop": "Experimenter",
            "ref_type": "string",
            "definition": "Contains id references to Experimenters 'person' sections"
        }
        self.mapper.append_reference(converted_odml_doc, sec, sec_reference)
        self.assertIn("Experimenter", converted_odml_doc.sections["Experiment"].properties)
        self.assertTrue(len(converted_odml_doc.sections["Experiment"].properties["Experimenter"].values) == 2)
        self.assertIn(sec.oid, converted_odml_doc.sections["Experiment"].properties["Experimenter"].values)
        self.assertIn("ref-01-123-456", converted_odml_doc.sections["Experiment"].properties["Experimenter"].values)

    def test_convert_odml_terminology(self):
        """
        Test Case for the complete mapping of an odML document
        """
        orig_odml_doc = ODMLReader().from_string(bytes(odml_test_data.TEST_ODML_FILE, 'utf-8'))
        with open('./tests/data/odml/odml_test_mapping.json') as mapping:
            with mock.patch('builtins.open', mock.mock_open(read_data=mapping.read())):
                odml_mapper = mapper.OdmlMapper()
                converted_odml_doc = odml_mapper.convert_odml_terminology(orig_odml_doc)
                self.assertIn("Experiment", converted_odml_doc.sections)
                self.assertEqual(
                    "experiment",
                    converted_odml_doc.sections["Experiment"].type
                )
                self.assertIn("ProjectName", converted_odml_doc.sections["Experiment"].properties)
                self.assertEqual(
                    ["AUDITORY ERP PROTOCOL IN CHILDREN WITH DEVELOPMENTAL COORDINATION DISORDER"],
                    converted_odml_doc.sections["Experiment"].properties["ProjectName"].values
                )
                self.assertIn("HardwareProperties", converted_odml_doc.sections)
                self.assertEqual(
                    "collection/hardware_properties",
                    converted_odml_doc.sections["HardwareProperties"].type
                )
                self.assertIn("Response Button", converted_odml_doc.sections["HardwareProperties"].sections)
                self.assertEqual(
                    "hardware",
                    converted_odml_doc.sections["HardwareProperties"].sections["Response Button"].type
                )
                self.assertIn(
                    "Description",
                    converted_odml_doc.sections["HardwareProperties"].sections["Response Button"].properties
                )
                self.assertIn("Recording", converted_odml_doc.sections)
                self.assertEqual(
                    "recording",
                    converted_odml_doc.sections["Recording"].type
                )
                self.assertIn("Environment", converted_odml_doc.sections)
                self.assertEqual(
                    "environment",
                    converted_odml_doc.sections["Environment"].type
                )
                self.assertIn("RoomTemperature", converted_odml_doc.sections["Environment"].properties)
                self.assertEqual(
                    ["23"],
                    converted_odml_doc.sections["Environment"].properties["RoomTemperature"].values
                )

    def test_map_section_additional_options(self):
        converted_odml_doc = self.createDocumentWithSection("Recording", "recording")
        section_mapping = {
            "corresponding_term": {
                "type": "person",
                "name": "Experimenter",
                "parent_sections": ""
            },
            "add_props": [
                {
                    "name": "Name",
                    "type": "string",
                    "value": "val",
                    "definition": "def"
                }
            ],
            "section_reference": [
                {
                    "section": "recording__Recording",
                    "prop": "Experimenters",
                    "ref_type": "string",
                    "definition": "Contains id references to Experimenters 'person' sections"
                }
            ]
        }
        self.mapper.map_section(converted_odml_doc, section_mapping)
        self.assertIn("Experimenter", converted_odml_doc.sections)
        self.assertIn("Name", converted_odml_doc.sections["Experimenter"].properties)
        self.assertEqual(["val"], converted_odml_doc.sections["Experimenter"].properties["Name"].values)
        self.assertIn("Recording", converted_odml_doc.sections)
        self.assertIn("Experimenters", converted_odml_doc.sections["Recording"].properties)
        self.assertIn(converted_odml_doc.sections["Experimenter"].id,
                      converted_odml_doc.sections["Recording"].properties["Experimenters"].values)

    def test_map_property_additional_options(self):
        converted_odml_doc = odml.Document()
        property_mapping = {
            "type": "string",
            "example_value": "['John Doe']",
            "corresponding_term": {
                "name": "FullName",
                "type": "string",
                "parent_sections": "person__Experimenter",
                "definition": "Def",
                "unit": "V",
                "add_props": [
                    {
                        "name": "Role",
                        "value": "Experimenter",
                        "type": "string"
                    }
                ],
                "section_reference": [
                    {
                        "section": "recording__Recording",
                        "prop": "Experimenter",
                        "ref_type": "string",
                        "definition": "Contains id references to Experimenters 'person' sections"
                    }
                ]
            }
        }
        odml_prop = self.createDocumentProperty("name", "John Doe", "string")
        self.mapper.map_property(converted_odml_doc, odml_prop, property_mapping)
        self.assertIn("FullName", converted_odml_doc.sections["Experimenter"].properties)
        self.assertEqual(["John Doe"], converted_odml_doc.sections["Experimenter"].properties["FullName"].values)
        self.assertEqual("Def", converted_odml_doc.sections["Experimenter"].properties["FullName"].definition)
        self.assertEqual("V", converted_odml_doc.sections["Experimenter"].properties["FullName"].unit)
        self.assertIn("Role", converted_odml_doc.sections["Experimenter"].properties)
        self.assertEqual(["Experimenter"], converted_odml_doc.sections["Experimenter"].properties["Role"].values)
        self.assertIn("Recording", converted_odml_doc.sections)
        self.assertIn("Experimenter", converted_odml_doc.sections["Recording"].properties)
        self.assertIn(converted_odml_doc.sections["Experimenter"].id,
                      converted_odml_doc.sections["Recording"].properties["Experimenter"].values)

    def test_map_property_as_reference(self):
        converted_odml_doc = self.createDocumentWithSection("Amplifier", "hardware")
        odml_prop = self.createDocumentProperty("Ref", "www.website.com/reference_link.html", "string")
        property_mapping = {
            "type": "string",
            "example_value": "['John Doe']",
            "use_as_reference": "hardware__Amplifier",
            "corresponding_term": {
                "name": "",
                "type": "",
                "parent_sections": ""
            }
        }
        self.mapper.map_property(converted_odml_doc, odml_prop, property_mapping)
        self.assertEqual("www.website.com/reference_link.html", converted_odml_doc.sections["Amplifier"].reference)


if __name__ == '__main__':
    unittest.main()
