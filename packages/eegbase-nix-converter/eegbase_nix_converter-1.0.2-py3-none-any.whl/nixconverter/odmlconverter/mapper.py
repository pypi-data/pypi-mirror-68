"""
Functions that map the data/metadata properties from EEGbase to an odML terminology.

Default Terminologies URL: https://portal.g-node.org/odml/terminologies/v1.1/terminologies.xml
"""
import json
import os
import re
from datetime import datetime
import numpy as np
import odml

from nixconverter.utils import conf
from nixconverter.utils import utils


class OdmlMapper:
    """
    Class for mapping the sections/properties according to a JSON mapping file
    """
    def __init__(self, custom_mapping=None, console_output=None):
        self.console_output = console_output
        self.custom_mapping = custom_mapping
        self.skipped_properties = 0
        self.skipped_sections = 0

    def convert_odml_terminology(self, orig_odml_doc):
        """
        Creates the root section with the basic odML properties and
        then recursively walks the sections and their properties from the passed odML and maps them
        to a new odML structure using the JSON mapping file.

        :param orig_odml_doc: the original odML document to convert
        :type orig_odml_doc: odml.doc.BaseDocument
        :returns the odML document mapped by the JSON file
        :rtype odml.doc.BaseDocument
        """
        converted_odml_doc = odml.Document()
        if orig_odml_doc.author:
            converted_odml_doc.author = orig_odml_doc.author
        if orig_odml_doc.date:
            converted_odml_doc.date = orig_odml_doc.date
        if orig_odml_doc.version:
            converted_odml_doc.version = orig_odml_doc.version
        converted_odml_doc.repository = conf.NIX_ODML_BASE_REPOSITORY

        mapping = self.get_mapping()

        self.map_sections(converted_odml_doc, mapping, orig_odml_doc)
        utils.console_output_text(
            f"odML Mapper - skipped sections: {self.skipped_sections}, skipped properties: {self.skipped_properties}",
            self.console_output
        )
        return converted_odml_doc

    def get_mapping(self):
        """
        Loads the mapping file

        :returns the JSON List with the section/property mapping
        :rtype dict
        """
        mapping_path = os.path.join(os.path.dirname(__file__), conf.DEFAULT_ODML_MAPPING)
        if self.custom_mapping:
            mapping_path = self.custom_mapping

        with open(mapping_path) as mapping_json:
            return json.load(mapping_json)

    def map_sections(self, converted_odml_doc, mapping, odml_sec):
        """
        Method that iterates through the sections and properties in the original odML document and converts them
        according to the mapping file to a new odML

        :param converted_odml_doc: remapped odML document
        :type converted_odml_doc: odml.doc.BaseDocument
        :param mapping: the JSON List with the section/property mapping
        :type mapping dict
        :param odml_sec: Section in the original odML document
        :type odml_sec: odml.section.BaseSection
        """
        for section in odml_sec.sections:
            mapping_section_name = f"{section.type}__{section.name}".lower()
            if mapping_section_name in mapping \
                    and mapping[mapping_section_name] \
                    and mapping[mapping_section_name]["corresponding_term"]:
                sec_section = self.get_section(
                    converted_odml_doc,
                    mapping[mapping_section_name]["corresponding_term"]["parent_sections"]
                )
                if mapping[mapping_section_name]["corresponding_term"]["name"] not in sec_section.sections:
                    self.map_section(
                        converted_odml_doc,
                        mapping[mapping_section_name]
                    )

                for odml_prop in odml_sec[section.name].properties:
                    mapping_prop_name = f"{odml_prop.name}".lower()
                    if mapping_prop_name in mapping[mapping_section_name]["props"]:
                        self.map_property(
                            converted_odml_doc,
                            odml_prop,
                            mapping[mapping_section_name]["props"][mapping_prop_name]
                        )
                    else:
                        utils.console_output_text(
                            f"odML Mapper - Skipping prop {mapping_prop_name}. No mapping found",
                            self.console_output
                        )
                        self.skipped_properties += 1
            else:
                utils.console_output_text(
                    f"odML Mapper - Skipping section {mapping_section_name}. No mapping found",
                    self.console_output
                )
                self.skipped_sections += 1

            if section.sections:
                self.map_sections(converted_odml_doc, mapping, section)

    def map_section(self, converted_odml_doc, section_mapping):
        """
        Maps an odML section accordingly to its mapping

        :param converted_odml_doc: the odML document containing the already converted sections
        :type converted_odml_doc: odml.doc.BaseDocument
        :param section_mapping: the dict of the section mapping from the JSON mapping file
        :type section_mapping: dict
        """
        try:
            if section_mapping["corresponding_term"]["type"]:
                sec = odml.Section(
                    name=section_mapping["corresponding_term"]["name"],
                    type=section_mapping["corresponding_term"]["type"],
                    repository=conf.NIX_ODML_BASE_REPOSITORY
                )
                if "add_props" in section_mapping:
                    for additional_prop in section_mapping["add_props"]:
                        prop = odml.Property(
                            name=additional_prop["name"],
                            dtype=additional_prop["type"],
                            values=additional_prop["value"]
                        )
                        if "definition" in additional_prop:
                            prop.definition = additional_prop["definition"]
                        sec.append(prop)
                self.append_section(
                    converted_odml_doc,
                    sec,
                    section_mapping["corresponding_term"]["parent_sections"]
                )
                if "section_reference" in section_mapping:
                    for ref in section_mapping["section_reference"]:
                        self.append_reference(converted_odml_doc, sec, ref)
        except KeyError:
            print(f"section {section_mapping['corresponding_term']['name']} already exists")

    def map_property(self, converted_odml_doc, odml_prop, property_mapping):
        """
        Maps an odML property accordingly to its mapping

        :param converted_odml_doc: the odML document containing the already converted sections
        :type converted_odml_doc: odml.doc.BaseDocument
        :param odml_prop: the original odML property
        :type odml_prop: odml.property.BaseProperty
        :param property_mapping: the dict of the property mapping from the JSON mapping file
        :type property_mapping: dict
        """
        if property_mapping:
            if property_mapping["corresponding_term"]["name"]:
                prop = odml.Property(
                    name=property_mapping["corresponding_term"]["name"],
                    dtype=property_mapping["corresponding_term"]["type"],
                )
                if "unit" in property_mapping["corresponding_term"]:
                    prop.unit = property_mapping["corresponding_term"]["unit"]
                if "definition" in property_mapping["corresponding_term"]:
                    prop.definition = property_mapping["corresponding_term"][
                        "definition"]

                prop.values = self.convert_property_type(odml_prop, property_mapping["corresponding_term"])

                prop_section = self.get_section(
                    converted_odml_doc,
                    property_mapping["corresponding_term"]["parent_sections"]
                )
                prop_section.append(prop)
                if "add_props" in property_mapping["corresponding_term"]:
                    for additional_prop in property_mapping["corresponding_term"]["add_props"]:
                        prop = odml.Property(
                            name=additional_prop["name"],
                            dtype=additional_prop["type"],
                            values=additional_prop["value"]
                        )
                        prop_section.append(prop)
                if "section_reference" in property_mapping["corresponding_term"]:
                    for ref in property_mapping["corresponding_term"]["section_reference"]:
                        self.append_reference(converted_odml_doc, prop_section, ref)
            if "use_as_reference" in property_mapping:
                prop_section = self.get_section(
                    converted_odml_doc,
                    property_mapping["use_as_reference"]
                )
                prop_section.reference = str(odml_prop.values[0])

    @staticmethod
    def convert_property_type(odml_prop, prop_mapping):
        """
        Converting the value if the mapping type is different from the original one

        :param odml_prop: the original odML property
        :type odml_prop: odml.property.BaseProperty
        :param prop_mapping: property in the mapping
        :type prop_mapping: dict
        :returns the converted property values
        """
        prop_values = odml_prop.values

        if str(odml_prop.dtype).lower() == "string" \
                and prop_mapping["type"] == "datetime":
            date_format = prop_mapping["format"] if "format" in prop_mapping else "%d.%m.%Y, %H:%M:%S"
            prop_values = [datetime.strptime(value, date_format) for value in prop_values]
        if prop_mapping["type"] == 'float':
            if str(odml_prop.dtype).lower() == "string":
                prop_values = [re.findall(r"[-+]?\d*\.\d+|\d+", value)[0] for value in prop_values]
            # prop.dtype = odml.DType.float
            prop_values = [np.float32(value) for value in prop_values]
        elif prop_mapping["type"] == 'int':
            if str(odml_prop.dtype).lower() == "string":
                prop_values = [re.findall(r"\d+", value)[0] for value in prop_values]
            prop_values = [int(value) for value in prop_values]
        elif prop_mapping["type"] == 'string':
            prop_values = [str(value) for value in prop_values]

        return prop_values

    def append_section(self, converted_odml_doc, sec, parent_sections):
        """
        Appends a new Section to a parent section

        :param converted_odml_doc: remapped odML document
        :type converted_odml_doc: odml.doc.BaseDocument
        :param sec: section to be appended
        :type sec: odml.section.BaseSection
        :param parent_sections: sections sequence of the parent sections
        :type parent_sections: str
        """
        section = self.get_section(converted_odml_doc, parent_sections)
        section.append(sec)

    @staticmethod
    def get_section(converted_odml_doc, parent_sections):
        """
        Retrieves a section from the odML document
        If the section does not exist, it is created according to the parent sections sequence

        :param converted_odml_doc: the root of the converted odML document
        :type converted_odml_doc: odml.doc.BaseDocument
        :param parent_sections: the sequence of the sections
        The format of the sequence is retrieved from the mapping file and follows a format where each section contains
        a type and then its name, separated by a double underscore '__'
        nested sections are separated by a triple underscore '___'
        e.g.:
        sectype__secname1___sectype__secname2
        If empty, the root of the odML document is returned
        :type parent_sections: str
        :returns the passed section, or odML root if passed section name is empty
        :rtype odml.section.BaseSection
        """
        if parent_sections:
            sections = parent_sections.split("___")
            target_section = converted_odml_doc
            for section in sections:
                section = section.split("__")
                if section[1] not in target_section.sections:
                    new_section = odml.Section(
                        name=section[1],
                        type=section[0],
                        repository=conf.NIX_ODML_BASE_REPOSITORY
                    )
                    target_section.append(new_section)
                target_section = target_section[section[1]]

            return target_section

        return converted_odml_doc

    def append_reference(self, converted_odml_doc, section, ref):
        """
        Append a reference to the section by a mapping file

        :param converted_odml_doc: the root of the converted odML document
        :type converted_odml_doc: odml.doc.BaseDocument
        :param ref: the reference properties from the mapping file
        :type ref: dict
        :param section: section to be referred
        :type section: odml.section.BaseSection
        """
        referring_section = self.get_section(converted_odml_doc, ref["section"])
        if ref["prop"] in referring_section.properties:
            current_val = referring_section.properties[ref["prop"]].values
            current_val.append(section.oid)
            referring_section.properties[ref["prop"]].values = current_val
        else:
            prop = odml.Property(
                name=ref["prop"],
                values=section.oid,
                dtype="string"
            )
            if "definition" in ref:
                prop.definition = ref["definition"]
            referring_section.append(prop)
