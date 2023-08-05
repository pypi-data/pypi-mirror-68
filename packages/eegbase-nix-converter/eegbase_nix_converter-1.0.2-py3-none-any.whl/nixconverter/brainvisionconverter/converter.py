"""
Module for the conversion of BrainVision files to a NIX file
"""

import json
import os
from datetime import datetime
from collections.abc import Iterable, Mapping
import re
import mne
import numpy as np

from nixconverter.utils import conf
from nixconverter.utils import utils


class BrainVisionConverter:
    """
    Class for converting the BrainVision recording data and metadata into the NIX entities
    """
    def __init__(self, console_output=False):
        self.console_output = console_output
        mapping_path = os.path.join(os.path.dirname(__file__), conf.DEFAULT_BRAINVISION_MAPPING)
        with open(mapping_path) as mapping_json:
            self.mapping = json.load(mapping_json)

    def register_data_blocks(self, block, raw_bv, header_props):
        """
        Creates the default session block in the NIX file and data arrays for the according BranVision data

        :param block: the NIX block representing the recording session
        :type block: nix.Block
        :param raw_bv: raw BrainVision data parsed from the mne tool
        :type raw_bv: mne.io.brainvision.brainvision.RawBrainVision
        :param header_props: the header properties for the passed BrainVision data
        :type header_props: utils.HeaderProperties
        """
        bv_data = raw_bv.get_data()
        time = raw_bv.times
        num_channels = raw_bv.info["nchan"]
        utils.console_output_text(
            f"{header_props.data_file}: Found {num_channels} channels with {raw_bv.n_times} samples per channel",
            console_output=self.console_output
        )

        # create the data_array and put it into its group
        data = block.create_data_array(header_props.data_file_name, header_props.get_block_data_type(), data=bv_data,
                                       dtype=bv_data.dtype)
        block.create_group(header_props.data_file_name, header_props.get_block_data_type())
        if raw_bv.info["chs"][0]["unit"] == mne.io.constants.FIFF.FIFF_UNIT_V:
            data.unit = "V"
        else:
            data.unit = raw_bv.info["chs"][0]["unit"]

        block.groups[header_props.data_file_name].data_arrays.append(data)
        utils.console_output_text(
            f"The {header_props.data_file_name} data_array and group were created in the NIX block",
            console_output=self.console_output
        )

        # set data_array dimensions and labels
        for dim_len in data.shape:
            if dim_len == num_channels:
                # channel labels: SetDimension
                data.append_set_dimension(labels=raw_bv.ch_names)
            elif dim_len == raw_bv.n_times:
                # times: RangeDimension
                data.append_range_dimension(ticks=time, label="time", unit="s")

        self.append_data_stimuli(block, raw_bv.annotations, header_props)

    def append_data_stimuli(self, block, stimuli, header_props):
        """
        Appends stimuli data to the raw data and the appropriate group

        :param block: the NIX block representing the recording session
        :type block: nix.Block
        :param stimuli: Stimuli for the raw data
        :type stimuli: mne.Annotations
        :param header_props: the header properties for the passed BrainVision data
        :type header_props: utils.HeaderProperties
        """
        # pylint: disable=too-many-locals
        if stimuli:
            stimuli_tuples = []
            for label, onset, duration in zip(
                    stimuli.description,
                    stimuli.onset,
                    stimuli.duration
            ):
                stimuli_tuples.append((label, onset, duration))

            utils.console_output_text(
                f"Found {len(stimuli_tuples)} annotations in the BrainVision data. Adding them  as multi_tags into "
                f"the NIX file",
                console_output=self.console_output
            )

            labels = [stimuli[0] for stimuli in stimuli_tuples]
            onsets = [stimuli[1] for stimuli in stimuli_tuples]
            durations = [stimuli[2] for stimuli in stimuli_tuples]

            data_shape = block.groups[header_props.data_file_name].data_arrays[0].shape
            num_channels = data_shape[0]
            data_dimension = len(data_shape)
            if data_dimension == 1:
                positions = onsets
                extents = durations
            else:
                positions = [(0, p) for p in onsets]
                extents = [(num_channels - 1, e) for e in durations]

            positions_data_array = block.create_data_array(
                f"STIMULUS_{header_props.data_file_name}_positions",
                f"{conf.NIX_ANNOTATION_TYPE}.positions",
                data=positions
            )
            positions_data_array.units = {"s"}
            positions_data_array.append_set_dimension(labels=labels)

            extents_data_array = block.create_data_array(
                f"STIMULUS_{header_props.data_file_name}_extents",
                f"{conf.NIX_ANNOTATION_TYPE}.extents",
                data=extents
            )
            extents_data_array.units = {"s"}
            extents_data_array.append_set_dimension(labels=labels)

            for _ in range(data_dimension - 1):
                # extra set dimensions for any extra data dimensions (beyond the first)
                positions_data_array.append_set_dimension()
                extents_data_array.append_set_dimension()

            stimulus_multi_tag = block.create_multi_tag(
                header_props.data_file_name,
                f"{conf.NIX_ANNOTATION_TYPE}",
                positions=positions_data_array
            )
            stimulus_multi_tag.extents = extents_data_array
            multi_tag_units = list("s")
            for _ in range(data_dimension - 1):
                multi_tag_units.append("")
            stimulus_multi_tag.units = set(multi_tag_units)

            block.groups[header_props.data_file_name].multi_tags.append(stimulus_multi_tag)

            for data_array in block.groups[header_props.data_file_name].data_arrays:
                if data_array.type == header_props.get_block_data_type():
                    stimulus_multi_tag.references.append(data_array)
            utils.console_output_text(
                "All multi_tags were added into the NIX file",
                console_output=self.console_output
            )

    def append_data_info(self, nix_file, raw_bv, header_props):
        """
        Creates NIX sections from raw BrainVision metadata

        :param nix_file: the NIX file containing the block with the recording session
        :type nix_file: nix.File
        :param raw_bv: raw BrainVision data parsed from the mne tool
        :type raw_bv: mne.io.brainvision.brainvision.RawBrainVision
        :param header_props: the header properties for the passed BrainVision data
        :type header_props: utils.HeaderProperties
        """
        utils.console_output_text(
            "Creating sections and properties from the BrainVision metadata",
            console_output=self.console_output
        )
        metadata_section = nix_file.create_section(
            header_props.data_file_name + " Metadata",
            header_props.get_metadata_data_type()
        )

        self.add_custom_settings(raw_bv.info, header_props)

        self.create_bv_metadata_tree(
            metadata_section,
            raw_bv.info,
            nix_file.blocks[conf.NIX_BLOCK_NAME],
            header_props
        )

        test = nix_file.blocks[conf.NIX_BLOCK_NAME].groups[header_props.data_file_name].data_arrays[0]
        test.metadata = metadata_section
        utils.console_output_text(
            "Metadata were appended and linked to the data_array",
            console_output=self.console_output
        )

    def add_custom_settings(self, bv_info, header_props):
        """
        Parses the BrainVision header file for additional information, typically stored in the settings part,
        that the mne.io.brainvision reader does not parse.
        If possible, tries to match the additional settings to already existing BrainVision info,
        (e.g. channel impedance)

        :param bv_info: the bv_info dict parsed from the BrainVision header
        :type bv_info: dict
        :param header_props: the header properties for the passed BrainVision data
        :type header_props: utils.HeaderProperties
        """
        # pylint: disable=protected-access
        settings, cfg, cinfo, _ = mne.io.brainvision.brainvision._aux_vhdr_info(header_props.header_file)

        settings = settings.splitlines()

        for channel in bv_info['chs']:
            channel['nchan'] = bv_info['nchan']

        self.parse_impedance(settings, bv_info)

        if 'S e g m e n t a t i o n  /  A v e r a g i n g' in settings:
            bv_info['segmentation'] = self.parse_segmentation(settings, cfg, cinfo)

    def parse_impedance(self, settings, bv_info):
        """
        Parses impedances from the header file

        :param settings: header settings lines
        :type settings: list
        :param bv_info: BrainVision info parsed from the original parser
        :type bv_info: dict
        """
        electrode_imp_ranges = self.parse_impedance_ranges(settings)
        impedance = next((item for item in settings if item.startswith('Impedance')), None)
        if impedance:
            idx = settings.index(impedance)
            impedance = impedance.split()
            impedance_unit = impedance[1].lstrip('[').rstrip(']')
            impedance_time = impedance[3]
            for setting in settings[idx + 1:]:
                # Parse channel impedances until a line that doesn't start with a word (channel name) is found
                if re.match(r'\w+:', setting):
                    channel_impedance = setting.split()
                    channel_name = channel_impedance[0].rstrip(':')
                    channel = next((item for item in bv_info['chs'] if item['ch_name'] == channel_name), None)
                    if channel is None:
                        continue
                    imp_as_number = re.findall(r"[-+]?\d*\.\d+|\d+", channel_impedance[1])
                    channel.update({
                        'imp': float(imp_as_number[0] if imp_as_number else 0),
                        'imp_unit': impedance_unit,
                        'imp_meas_time': datetime.strptime(impedance_time, "%H:%M:%S")
                    })

                    if channel['ch_name'] == 'Ref' and 'Reference' in electrode_imp_ranges:
                        channel.update(electrode_imp_ranges['Reference'])
                    elif channel['ch_name'] == 'Gnd' and 'Ground' in electrode_imp_ranges:
                        channel.update(electrode_imp_ranges['Ground'])
                    elif 'Data' in electrode_imp_ranges:
                        channel.update(electrode_imp_ranges['Data'])
                else:
                    break

    @staticmethod
    def parse_impedance_ranges(settings):
        """
        Parses the selected electrode impedance ranges from the BrainVision header

        :param settings: header settings lines
        :type settings: list
        :returns parsed electrode impedances
        :rtype dict
        """
        impedance_ranges = [item for item in settings if "Selected Impedance Measurement Range" in item]
        electrode_imp_ranges = dict()
        if impedance_ranges:
            if len(impedance_ranges) == 1:
                img_range = impedance_ranges[0].split()
                for electrode_type in ['Data', 'Reference', 'Ground']:
                    electrode_imp_ranges[electrode_type] = {
                        "imp_lower_bound": float(img_range[-4]),
                        "imp_upper_bound": float(img_range[-2]),
                        "imp_range_unit": img_range[-1]
                    }
            else:
                for electrode_range in impedance_ranges:
                    electrode_range = electrode_range.split()
                    electrode_imp_ranges[electrode_range[0]] = {
                        "imp_lower_bound": float(electrode_range[6]),
                        "imp_upper_bound": float(electrode_range[8]),
                        "imp_range_unit": electrode_range[9]
                    }
        return electrode_imp_ranges

    def parse_segmentation(self, settings, cfg, common_info):
        """
        Parses the segmentation/averaging section of the BrainVision header

        :param settings: header settings lines
        :type settings: list
        :param cfg: cfg of the header file returned by mne.io.brainvision.brainvision._aux_vhdr_info
        :type cfg: ConfigParser
        :param common_info: cinfo from the BrainVision header parser
        :type common_info: str
        :returns the parsed segmentation as a dict
        :rtype dict
        """
        idx = settings.index('S e g m e n t a t i o n  /  A v e r a g i n g')
        segmentation_settings = settings[idx:]
        segmentation = self.parse_basic_segmentation(cfg, common_info)

        if "Markers" in segmentation_settings:
            idx = segmentation_settings.index("Markers")
            markers = list()
            for setting in segmentation_settings[idx + 2:]:
                if re.match(r'(\t)?\w', setting):
                    markers.append(setting.strip())
                else:
                    break
            segmentation["artifact_rejection"] = markers

        if "Interval" in segmentation_settings:
            idx = segmentation_settings.index("Interval")
            intervals = dict()
            for setting in segmentation_settings[idx + 2:]:
                if re.match(r'(\t)?\w', setting):
                    interval_setting = setting.split()
                    intervals[interval_setting[0]] = {
                        "unit": interval_setting[1].lstrip('[').rstrip(']:'),
                        "duration": interval_setting[2]
                    }
                else:
                    break
            segmentation["intervals"] = intervals

        if "Averaging" in segmentation_settings:
            segmentation["averaging"] = self.get_segmentation_key_values(
                segmentation_settings,
                segmentation_settings.index("Averaging"),
                " is "
            )

        if "Artifact Rejection" in segmentation_settings:
            segmentation["artifact_rejection"] = self.get_segmentation_key_values(
                segmentation_settings,
                segmentation_settings.index("Artifact Rejection")
            )

        if "Miscellaneous" in segmentation_settings:
            segmentation["miscellaneous"] = self.get_segmentation_key_values(
                segmentation_settings,
                segmentation_settings.index("Miscellaneous")
            )

        return segmentation

    @staticmethod
    def parse_basic_segmentation(cfg, common_info):
        """
        Parses the segmentation info from the Common Infos using the ConfgiParser

        :param cfg: the ConfigParser from the BrainVision header parser
        :type cfg: ConfigParser
        :param common_info: the BrainVision header common infos section
        :type common_info: str
        :return:
        """
        segmentation = dict()

        seg_type = cfg.get(common_info, "SegmentationType")
        if seg_type:
            segmentation["type"] = seg_type
        seg_data_points = cfg.getint(common_info, "SegmentDataPoints")
        if seg_data_points:
            segmentation["data_points"] = seg_data_points
        seg_averaged = cfg.get(common_info, "Averaged")
        if seg_averaged:
            segmentation["averaged"] = seg_averaged
        seg_averaged_segments = cfg.getint(common_info, "AveragedSegments")
        if seg_averaged_segments:
            segmentation["averaged_segments"] = seg_averaged_segments

        return segmentation

    @staticmethod
    def get_segmentation_key_values(segmentation_settings, idx, delimiter=":"):
        """
        Parses the key value pairs from the Segmentation / Averaging section of the BrainVision header
        Default delimiter is ':' where left side is considered the key, and right side is the value.
        Values are parsed into arrays, elements can be split with a comma ','
        Stops the parsing when the first empty setting line is found

        :param segmentation: the parsed segmentation dict
        :type segmentation: dict
        :param segmentation_settings: the list of settings lines
        :type segmentation_settings: list
        :param idx: starting index
        :type idx: int
        :param delimiter: delimiter to split the key and value
        :type delimiter: str
        :returns dict of the parsed key and values
        :rtype dict
        """
        key_name = None
        values = dict()
        for setting in segmentation_settings[idx + 2:]:
            if re.match(r'(\t)?\w', setting):
                setting = setting.split(delimiter)
                key_name = setting[0].strip()
                key_values = setting[1].strip().split(',')
                values[key_name] = key_values if key_values[0] != '' else []
            elif re.match(r'\t\t\w', setting) and key_name is not None:
                key_values = setting.strip().split(',')
                for val in key_values:
                    if val != '':
                        values[key_name].append(val)
            else:
                break
        return values

    # pylint: disable=too-many-arguments
    def create_bv_metadata_tree(
            self,
            root_section,
            values,
            block,
            header_props,
            subsection=None,
            subsubsection=None
    ):
        """
        Creates a tree structure of sections and properties containing metadata of the BrainVision data
        Applies the BrainVision mapping to create the sections and properties in NIX.
        This is a modified version of a function from https://github.com/G-Node/nix-mne

        :param root_section: the root metadata section in NIX file where the metadata will be written
        :type root_section: nix.Section
        :param values: the info from raw BrainVision
        :type values: dict
        :param block: the NIX block representing the recording session
        :type block: nix.Block
        :param header_props: the header properties for the passed BrainVision data
        :type header_props: utils.HeaderProperties
        :param subsection: current subsection in the NIX file
        :type subsection: nix.Section
        :param subsubsection: current subsection of a subsection in the NIX file
        :type subsubsection: nix.Section
        """
        # pylint: disable=too-many-nested-blocks, too-many-branches, too-many-locals
        if values is None:
            return
        for key, value in values.items():
            # Skip empty values
            if value is None:
                continue

            mapping_key = key
            if subsection is not None:
                mapping_key = f"{subsection.name}__{key}"
            # If the bv_info property is mapped, save the value according to the mapping
            if mapping_key in self.mapping and self.mapping[mapping_key]["name"]:
                prop_subsection = subsubsection if subsubsection is not None else subsection
                section = self.get_section(root_section, self.mapping[mapping_key]["parent_section"], prop_subsection)
                if isinstance(value, Iterable):
                    # skipping metadata properties with empty values
                    if len(value) == 0:
                        continue

                    # if the value is multidimensional, we need to create a data_array for it
                    ndim = np.ndim(value)
                    if ndim > 1:
                        block_name = self.mapping[mapping_key]["name"]
                        data_array = block.create_data_array(
                            f"{header_props.data_file_name}_{block_name}",
                            f"{conf.NIX_METADATA_TYPE}.multidimensional",
                            data=value
                        )
                        for _ in range(ndim):
                            data_array.append_set_dimension()
                        prop = section.create_property(self.mapping[mapping_key]["name"], data_array.id)
                        prop.type = str(value.__class__.__name__)
                        data_array.metadata = section
                        continue
                    # check element type
                    if isinstance(value, Mapping):
                        # Create a new Section to hold the metadata found in the dictionary
                        subsec = section.create_section(
                            self.mapping[mapping_key]["name"],
                            self.mapping[mapping_key]["type"]
                        )
                        self.create_bv_metadata_tree(
                            root_section,
                            value,
                            block,
                            header_props,
                            subsec
                        )
                        continue
                    if isinstance(value[0], Mapping):
                        # Create a new subsection to hold each nested dictionary as sub-subsections
                        subsec = section.create_section(
                            self.mapping[mapping_key]["name"],
                            self.mapping[mapping_key]["type"]
                        )
                        if "subsection" in self.mapping[mapping_key]:
                            for idx, subd in enumerate(value):
                                if "prefix" in self.mapping[mapping_key]["subsection"]:
                                    name = f"{self.mapping[mapping_key]['subsection']['prefix']}-{idx}"
                                else:
                                    name = f"{key}-{idx}"
                                subsubsec = subsec.create_section(name,
                                                                  self.mapping[mapping_key]["subsection"]["type"])
                                self.create_bv_metadata_tree(
                                    root_section,
                                    subd,
                                    block,
                                    header_props,
                                    subsec,
                                    subsubsec
                                )
                        continue

                self.create_prop(section, value, self.mapping[mapping_key], values)
                if "add_props" in self.mapping[mapping_key]:
                    for add in self.mapping[mapping_key]["add_props"]:
                        self.create_prop(section, value, add, values)

    @staticmethod
    def create_prop(section, value, mapping, raw_values):
        """
        Creates a NIX property for the passed section

        :param section: Section where to create the propery
        :type section: nix.Section
        :param value: the BrainVision value of the property
        :param mapping: The BrainVision Mapping
        :type mapping: dict
        :param raw_values: the Raw BrainVision values
        :type raw_values: dict
        """
        try:
            if mapping["type"] == "float":
                value = float(value)
            elif mapping["type"] == "int":
                value = int(value)
            # elif mapping["type"] == "datetime":
            #     value = value
            elif mapping["type"] == "date":
                value = str(datetime.date(value))
            elif mapping["type"] == "time":
                value = str(datetime.time(value).strftime('%H:%M:%S'))
            else:
                value = str(value)
            prop = section.create_property(
                mapping["name"],
                value
            )
        except TypeError:
            # inconsistent iterable types: upgrade to floats
            prop = section.create_property(mapping["name"], [float(vi) for vi in value])
        if "unit_field" in mapping and mapping["unit_field"] in raw_values:
            prop.unit = raw_values[mapping["unit_field"]]
        elif "unit" in mapping:
            prop.unit = mapping["unit"]
        # prop.type = str(v.__class__.__name__)
        prop.type = mapping["type"]

    @staticmethod
    def get_section(nix_root_section, parent_sections, subsection=None):
        """
        Retrieves a section from the NIX metadata
        If the section does not exist, it is created according to the parent sections sequence

        :param nix_root_section: the root of the converted odML document
        :type nix_root_section: nix.Section
        :param parent_sections: the sequence of the sections
        The format of the sequence is retrieved from the mapping file and follows a format where each section contains
        a type and then its name, separated by a double underscore '__'
        nested sections are separated by a triple underscore '___'
        e.g.:
        sectype__secname1___sectype__secname2
        If empty, the root section is returned
        :type parent_sections: str
        :param subsection: if passed, returns the subsection instead of a root section of parent_sections is None
        :type subsection: nix.Section
        :returns the passed section, or odML root if passed section name is empty
        :rtype nix.Section
        """
        if parent_sections:
            sections = parent_sections.split("___")
            target_section = nix_root_section
            for section in sections:
                section = section.split("__")
                if section[1] not in target_section.sections:
                    sec = target_section.create_section(
                        name=section[1],
                        type_=section[0]
                    )
                    sec.repository = conf.NIX_ODML_BASE_REPOSITORY
                target_section = target_section[section[1]]

            return target_section

        if subsection is not None:
            return subsection

        return nix_root_section
