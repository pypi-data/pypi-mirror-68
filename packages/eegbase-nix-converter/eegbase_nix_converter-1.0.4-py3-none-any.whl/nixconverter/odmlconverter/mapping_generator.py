"""odML mapping generator

For advanced script and mapping options, see https://gitlab.com/honza.seda/eegbase-nix-converter

Script for generating the mapping file from the odML .xml metadata
Mapping is used for the conversion of the odML files to the NIX sections and properties

The mapping is a JSON file containing all the sections and its properties of the odML .xml files in a folder.
Every section is in the root level of the JSON.

Sections are represented with a key in a format of type_name. The properties of the section are stored in the
"props" field of the section.
The mapping of a section or a property is defined in the "corresponding_term" field. By default, the generator fills
the corresponding term values by its original (Although the sections are not nested!).
The "corresponding_term" field must consist of the "name" (Section/property name), "type" and "parent_sections" fields.

Example of the "corresponding_term":
    "corresponding_term": {
      "name": "FirstName",
      "type": "string",
      "parent_sections": "collection__Experimenters___person__Person 2"
    }

If the "name" or "type" field is empty, the section/property will be skipped during the conversion to the NIX file.

Parent sections is a string sequence of sections.
Each section is represented by a type_Name combination (separated by a double underscore '__' character).
Nested sections are separated by a triple underscore '___'. Empty "parent_sections" means the root section of
the odML document.
For "parent_sections" of a property, the last section is the section where the property will be appended.
If the mapped property type is of type date/datetime, a format field is required that specifies the format used
to parse the values, e.g.: "format": "%d.%m.%Y, %H:%M:%S",

Apart from the "corresponding_term", Props in the mapping contain the fields "type" (type in the original odML)
and "example_value" (an example of a value stored in the property). These fields have solely an  informational purpose


Usage:
    odml_mapping_generator ODML OUTPUT
    odml_mapping_generator -h | --help

Arguments:
    ODML                        Folder (and all the nested folders) that will be searched for .xml files.
                                If multiple .xml files are found, the mapping will merge all the sections and properties
                                together into a single mapping file.
    OUTPUT                      Name of the file to output the mapping into.

Options:
    -h --help                   Show this screen.
"""

import os
import sys

import json
import odml
from docopt import docopt
from odml.tools import ODMLReader
from odml.tools.parser_utils import InvalidVersionException
from nixodmlconverter import convert as nix_odml_converter

from nixconverter.utils import utils


class OdmlMappingGenerator:
    """
    Class for generating the odML -> NIX Mapping file
    """
    def generate(self, input_path):
        """
        Generates the mapping JSON file from the odML .xml files in the input path

        :param input_path: path to the odML Document
        :type input_path: str
        """
        if not os.path.exists(input_path):
            raise utils.MissingFileException("Given path does not exist!")
        files = []
        full_search_path = input_path

        for filenames in os.walk(full_search_path):
            for file_list in filenames:
                for file_name in file_list:
                    if file_name.endswith('.xml'):
                        files.append(filenames[0] + os.sep + file_name)

        odml_structure = dict()
        for odml_file in files:
            try:
                odml_doc = odml.load(odml_file)
            except InvalidVersionException:
                xml_string = nix_odml_converter.VersionConverter(odml_file).convert()
                odml_doc = ODMLReader().from_string(xml_string)

            self.odml_recurse(odml_doc, odml_structure)

        return odml_structure

    def odml_recurse(self, section, odml_structure):
        """
        Iterates through all the sections and its properties and saves the parsed information into the mapping

        :param section: the odML section that will be parsed
        :type section: odml.section.BaseSection
        :param odml_structure: the parsed structure that will be dumped into the JSON file
        :type odml_structure: dict
        :return:
        """
        for odmlsec in section:
            props = dict()
            for odmlprop in odmlsec.properties:
                prop_name = odmlprop.name.lower()
                props[f"{prop_name}"] = dict({
                    'type': odmlprop.dtype,
                    'example_value': str(odmlprop.values),
                    'corresponding_term': dict({
                        'name': odmlprop.name,
                        'type': odmlprop.dtype,
                        'parent_sections': self.build_parent_string(odmlsec)
                    })
                })

            sec_name = f"{odmlsec.type}__{odmlsec.name}".lower()
            if sec_name not in odml_structure:
                odml_structure[sec_name] = dict()

            odml_structure[sec_name]['corresponding_term'] = dict({
                'name': odmlsec.name,
                'type': odmlsec.type,
                'parent_sections': self.build_parent_string(odmlsec.parent) if odmlsec.parent else ""
            })

            if 'props' not in odml_structure[sec_name]:
                odml_structure[sec_name]['props'] = dict()
            for prop, val in props.items():
                odml_structure[sec_name]['props'][prop] = val

            if odmlsec.sections:
                self.odml_recurse(odmlsec.sections, odml_structure)

    def build_parent_string(self, section):
        """
        Builds the parent sequence string of a passed section
        :param section: an odML section
        :type section: odml.section.BaseSection
        :returns the built parent sequence
        :rtype str
        """
        if section.parent:
            section_sequence = f"{section.type}__{section.name}"
            parent = self.build_parent_string(section.parent)
            if parent:
                section_sequence = f"{parent}___{section_sequence}"
        else:
            section_sequence = ""
        return section_sequence


def main(args=None):
    """
    Main function

    :param args: cli arguments
    """
    parser = docopt(__doc__, argv=args)
    generator = OdmlMappingGenerator()
    output_file = parser['OUTPUT']
    if not output_file.lower().endswith('.json'):
        output_file += ".json"
    with open(f"{output_file}", 'w') as json_output:
        json.dump(generator.generate(parser['ODML']), json_output)


if __name__ == "__main__":
    main(sys.argv[1:])
