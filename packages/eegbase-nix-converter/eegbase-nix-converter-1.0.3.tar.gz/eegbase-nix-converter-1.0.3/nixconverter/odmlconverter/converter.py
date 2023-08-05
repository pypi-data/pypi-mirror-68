"""
Module for converting the odML experiment metadata into the NIX sections and properties
"""

import os
import sys

import odml
from odml.tools import ODMLReader
from odml.tools.parser_utils import InvalidVersionException
from nixodmlconverter import convert as nix_odml_converter

from nixconverter.utils import conf
from nixconverter.utils import utils
from nixconverter.odmlconverter import mapper


class OdmlConverter:
    """
    Class for converting the odML experiment metadata into the NIX sections and properties
    """
    def __init__(self, keep_terminologies=False, custom_mapping=None, console_output=False):
        self.keep_terminologies = keep_terminologies
        self.custom_mapping = custom_mapping
        self.console_output = console_output

    def append_experiment_metadata(self, nix_file, odml_file):
        """
        Takes the odML file containing the experiment and session metadata and converts it
        to NIX sections and properties

        :param nix_file: the NIX file containing the block with the recording session
        :type nix_file: nix.File
        :param odml_file: path to the .xml file containing odML metadata about the experiment
        :type odml_file: str
        """
        utils.console_output_text(
            "Creating sections and properties from the experiment odML metadata",
            console_output=self.console_output
        )
        with open(os.devnull, "w") as stdout_redirect:
            try:
                odml_doc = odml.load(odml_file)
            except InvalidVersionException:
                utils.console_output_text(
                    "The version of the passed odML is invalid. Converting to latest version.",
                    console_output=self.console_output
                )
                # suppress console output from VersionConverter if --verbose option is False
                if not self.console_output:
                    sys.stdout = stdout_redirect
                xml_string = nix_odml_converter.VersionConverter(odml_file).convert()
                if not self.console_output:
                    sys.stdout = sys.__stdout__
                odml_doc = ODMLReader().from_string(xml_string)

            if not self.keep_terminologies:
                odml_mapper = mapper.OdmlMapper(self.custom_mapping, self.console_output)
                odml_doc = odml_mapper.convert_odml_terminology(odml_doc)

            nix_document_section = self.write_odml_doc(odml_doc, nix_file)

            # suppress console output from nix-odml-converter if --verbose option is False
            if not self.console_output:
                sys.stdout = stdout_redirect
            nix_odml_converter.odml_to_nix_recurse(odml_doc.sections, nix_document_section)
            utils.console_output_text("\n", self.console_output)
            if not self.console_output:
                sys.stdout = sys.__stdout__

            utils.console_output_text(
                "Experiment odML metadata appended to NIX container",
                console_output=self.console_output
            )

    def write_odml_doc(self, odml_doc, nix_file):
        """
        Writes the basic odML terms to the NIX experiment metadata section

        :param odml_doc: the root of the odML document
        :type odml_doc: odml.doc.BaseDocument
        :param nix_file: the NIX file containing the block with the recording session
        :type nix_file: nix.File
        :returns the newly created NIX section for the experiment metadata
        """
        nix_section = nix_file.create_section(
            conf.NIX_ODML_NAME,
            f"{conf.NIX_METADATA_TYPE}.session",
            oid=odml_doc.id
        )
        if odml_doc.author:
            nix_section.create_property('odML author', [odml_doc.author])
        if odml_doc.date:
            nix_section.create_property('odML date', [odml_doc.date.isoformat()])
        if odml_doc.version:
            nix_section.create_property('odML version', [odml_doc.version])

        if not self.keep_terminologies:
            nix_section.repository = conf.NIX_ODML_BASE_REPOSITORY
        elif odml_doc.repository:
            nix_section.repository = odml_doc.repository

        nix_section.create_property(
            'Description',
            "Converted to NIX from EEGbase dataset using the python converter available from: "
            "https://gitlab.com/honza.seda/eegbase-nix-converter"
        )

        return nix_section
