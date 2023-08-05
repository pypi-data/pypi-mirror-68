"""
Unit test cases covering the BrainVision conversion
"""
import unittest
from io import StringIO
from configparser import ConfigParser
from datetime import datetime
from unittest import mock

from nixconverter.brainvisionconverter import converter


class TestBrainVisionConverter(unittest.TestCase):
    def setUp(self):
        """
        Test Case setUp
        """
        with open('nixconverter/brainvisionconverter/brainvision_mapping.json') as mapping:
            with mock.patch('builtins.open', mock.mock_open(read_data=mapping.read())):
                self.brainvision_converter = converter.BrainVisionConverter()

    def test_parse_impedance(self):
        input_settings = [
            '', '====================================',
            'Data Electrodes Selected Impedance Measurement Range: 0 - 5 kOhm',
            'Ground Electrode Selected Impedance Measurement Range: 0 - 10 kOhm',
            'Reference Electrode Selected Impedance Measurement Range: 0 - 10 kOhm', 'Impedance [kOhm] at 17:25:01 :',
            'Fp1:         10', 'Fp2:         7', 'F3:           1', 'F4:           9', 'C3:           1',
            'Gnd:           1',
            ''
        ]
        output_bv_info = {
            "chs": [
                {"ch_name": "Fp1"},
                {"ch_name": "Fp2"},
                {"ch_name": "F3"},
                {"ch_name": "C3"},
                {"ch_name": "Gnd"},
            ]
        }
        with mock.patch('nixconverter.brainvisionconverter.converter.BrainVisionConverter.parse_impedance_ranges',
                        return_value={
                            'Data': {'imp_lower_bound': 0.0, 'imp_upper_bound': 5.0, 'imp_range_unit': 'kOhm'},
                            'Ground': {'imp_lower_bound': 0.0, 'imp_upper_bound': 10.0, 'imp_range_unit': 'kOhm'},
                            'Reference': {'imp_lower_bound': 0.0, 'imp_upper_bound': 10.0, 'imp_range_unit': 'kOhm'}
                        }):
            self.brainvision_converter.parse_impedance(input_settings, output_bv_info)
            self.assertIn("imp", output_bv_info["chs"][0])
            self.assertEqual(10.0, output_bv_info["chs"][0]["imp"])
            self.assertEqual("kOhm", output_bv_info["chs"][0]["imp_unit"])
            self.assertEqual(datetime.strptime("17:25:01", "%H:%M:%S"), output_bv_info["chs"][0]["imp_meas_time"])
            self.assertEqual(0.0, output_bv_info["chs"][0]["imp_lower_bound"])
            self.assertEqual(5.0, output_bv_info["chs"][0]["imp_upper_bound"])
            self.assertEqual(1.0, output_bv_info["chs"][4]["imp"])
            self.assertEqual("kOhm", output_bv_info["chs"][4]["imp_unit"])
            self.assertEqual(datetime.strptime("17:25:01", "%H:%M:%S"), output_bv_info["chs"][4]["imp_meas_time"])
            self.assertEqual(0.0, output_bv_info["chs"][4]["imp_lower_bound"])
            self.assertEqual(10.0, output_bv_info["chs"][4]["imp_upper_bound"])

    def test_parse_impedance_ranges(self):
        input_settings = [
            '', '====================================',
            'Data Electrodes Selected Impedance Measurement Range: 0 - 5 kOhm',
            'Ground Electrode Selected Impedance Measurement Range: 0 - 10 kOhm',
            'Reference Electrode Selected Impedance Measurement Range: 0 - 10 kOhm',
            'Impedance [kOhm] at 17:25:01 :'
        ]
        expected = {
            'Data': {'imp_lower_bound': 0.0, 'imp_upper_bound': 5.0, 'imp_range_unit': 'kOhm'},
            'Ground': {'imp_lower_bound': 0.0, 'imp_upper_bound': 10.0, 'imp_range_unit': 'kOhm'},
            'Reference': {'imp_lower_bound': 0.0, 'imp_upper_bound': 10.0, 'imp_range_unit': 'kOhm'}
        }
        actual = self.brainvision_converter.parse_impedance_ranges(input_settings)
        self.assertDictEqual(expected, actual)

    def test_parse_impedance_ranges_alternative(self):
        input_settings = [
            '', '====================================',
            'Data / Gnd / Ref Electrodes Selected Impedance Measurement Range: 0 - 5 kOhm',
            'Impedance [kOhm] at 17:25:01 :'
        ]
        expected = {
            'Data': {'imp_lower_bound': 0.0, 'imp_upper_bound': 5.0, 'imp_range_unit': 'kOhm'},
            'Ground': {'imp_lower_bound': 0.0, 'imp_upper_bound': 5.0, 'imp_range_unit': 'kOhm'},
            'Reference': {'imp_lower_bound': 0.0, 'imp_upper_bound': 5.0, 'imp_range_unit': 'kOhm'}
        }
        actual = self.brainvision_converter.parse_impedance_ranges(input_settings)
        self.assertDictEqual(expected, actual)

    def test_parse_segmentation(self):
        input_settings = [
            '', 'S e g m e n t a t i o n  /  A v e r a g i n g', '=============================================',
            'Markers', '-------', 'Stimulus    S  2        ', '', 'Interval', '--------', 'Prestimulus [ms]: 100',
            'Poststimulus [ms]: 1000', '', 'Artifact Rejection', '------------------', '\tGradient:        Disabled',
            '\tMax. Difference: Disabled', '\tAmplitude:       Disabled', '\tLow Activity:    Disabled',
            '\tTest Interval:   Whole Segment', '\tUntested Channels:',
            '\t\tC3, C4, F3, F4, F7, F8, Fp1, Fp2, O1, O2, P3, P4, T3, T4, T5, ', '\t\tT6', '', 'Averaging',
            '---------', '\tAveraging is On', '\tBaseline Correction is On', '', 'Miscellaneous', '-------------',
            '\tMax. Segments: unlimited', ''
        ]
        basic_segmentation = {
            'type': 'MARKERBASED', 'data_points': 1100, 'averaged': 'YES', 'averaged_segments': 80
        }
        expected = {'type': 'MARKERBASED', 'data_points': 1100, 'averaged': 'YES', 'averaged_segments': 80,
                    'artifact_rejection': {'Gradient': ['Disabled'], 'Max. Difference': ['Disabled'],
                                           'Amplitude': ['Disabled'], 'Low Activity': ['Disabled'],
                                           'Test Interval': ['Whole Segment'],
                                           'Untested Channels': ['C3', ' C4', ' F3', ' F4', ' F7', ' F8', ' Fp1',
                                                                 ' Fp2', ' O1', ' O2', ' P3', ' P4', ' T3', ' T4',
                                                                 ' T5', 'T6']},
                    'intervals': {'Prestimulus': {'unit': 'ms', 'duration': '100'},
                                  'Poststimulus': {'unit': 'ms', 'duration': '1000'}},
                    'averaging': {'Averaging': ['On'], 'Baseline Correction': ['On']},
                    'miscellaneous': {'Max. Segments': ['unlimited']}}
        with mock.patch('nixconverter.brainvisionconverter.converter.BrainVisionConverter.parse_basic_segmentation',
                        return_value=basic_segmentation):
            actual = self.brainvision_converter.parse_segmentation(input_settings, ConfigParser(), "Common Infos")
            self.assertDictEqual(expected, actual)

    def test_get_segmentation_key_values(self):
        input_settings = [
            'S e g m e n t a t i o n  /  A v e r a g i n g', '=============================================',
            'Markers', '-------', 'Stimulus    S  2        ', '', 'Interval', '--------', 'Prestimulus [ms]: 100',
            'Poststimulus [ms]: 1000', '', 'Artifact Rejection', '------------------', '\tGradient:        Disabled',
            '\tMax. Difference: Disabled', '\tAmplitude:       Disabled', '\tLow Activity:    Disabled',
            '\tTest Interval:   Whole Segment', '\tUntested Channels:',
            '\t\tC3, C4, F3, F4, F7, F8, Fp1, Fp2, O1, O2, P3, P4, T3, T4, T5, ', '\t\tT6', '', 'Averaging',
            '---------', '\tAveraging is On', '\tBaseline Correction is On', '', 'Miscellaneous', '-------------',
            '\tMax. Segments: unlimited', ''
        ]
        expected = {'Gradient': ['Disabled'], 'Max. Difference': ['Disabled'],
                    'Amplitude': ['Disabled'], 'Low Activity': ['Disabled'],
                    'Test Interval': ['Whole Segment'],
                    'Untested Channels': ['C3', ' C4', ' F3', ' F4', ' F7', ' F8', ' Fp1',
                                          ' Fp2', ' O1', ' O2', ' P3', ' P4', ' T3', ' T4',
                                          ' T5', 'T6']}
        actual = self.brainvision_converter.get_segmentation_key_values(input_settings, 11)
        self.assertDictEqual(expected, actual)

    def test_parse_basic_segmentation(self):
        params = '; Data created by the Vision Recorder\n\n[Common Infos]\nCodepage=UTF-8\n' \
                 'DataFile=LED_10_05_2012_76-T.avg\nMarkerFile=LED_10_05_2012_76-T.vmrk\nDataFormat=BINARY\n; ' \
                 'Data orientation: MULTIPLEXED=ch1,pt1, ch2,pt1 ...\nDataOrientation=MULTIPLEXED\n' \
                 'NumberOfChannels=19\n; Sampling interval in microseconds\nSamplingInterval=1000\n' \
                 'SegmentationType=MARKERBASED\nSegmentDataPoints=1100\nAveraged=YES\nAveragedSegments=80\n\n' \
                 '[Binary Infos]\nBinaryFormat=IEEE_FLOAT_32\n'
        cfg = ConfigParser()
        cfg.read_file(StringIO(params))
        expected = {'type': 'MARKERBASED', 'data_points': 1100, 'averaged': 'YES', 'averaged_segments': 80}
        actual = self.brainvision_converter.parse_basic_segmentation(cfg, 'Common Infos')
        self.assertDictEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
