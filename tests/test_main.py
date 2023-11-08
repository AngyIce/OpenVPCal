import shutil
from argparse import ArgumentTypeError
import json
import os
import tempfile
from json import JSONDecodeError

from open_vp_cal.main import validate_file_path, validate_folder_path, validate_project_settings, generate_patterns
from test_utils import TestBase, TestProject


class TestArgparseFunctions(TestBase):
    def test_validate_file_path_valid(self):
        with tempfile.NamedTemporaryFile() as temp:
            self.assertEqual(temp.name, validate_file_path(temp.name))

    def test_validate_file_path_invalid(self):
        with self.assertRaises(ArgumentTypeError):
            validate_file_path("nonexistentfile")

    def test_validate_folder_path_valid(self):
        with tempfile.TemporaryDirectory() as tempdir:
            self.assertEqual(tempdir, validate_folder_path(tempdir))

    def test_validate_folder_path_invalid(self):
        with self.assertRaises(ArgumentTypeError):
            validate_folder_path("nonexistentfolder")

    def test_validate_project_settings_valid(self):
        with tempfile.NamedTemporaryFile(suffix=".json", mode='w') as temp:
            json.dump({"key": "value"}, temp)
            temp.seek(0)
            self.assertEqual(temp.name, validate_project_settings(temp.name))

    def test_validate_project_settings_invalid(self):
        with tempfile.NamedTemporaryFile(suffix=".json") as temp:
            with self.assertRaises(JSONDecodeError):
                validate_project_settings(temp.name)

    def test_validate_project_settings_nonjson(self):
        with tempfile.NamedTemporaryFile(suffix=".txt", mode='w') as temp:
            temp.write("not a json file")
            temp.seek(0)
            with self.assertRaises(JSONDecodeError):
                validate_project_settings(temp.name)


class TestProjectCli(TestProject):

    def test_run_cli(self):
        expected_file = self.get_results_file(self.led_wall)

        # Override the roi so we have to run the auto detection
        self.project_settings.led_walls[0].roi = None

        results = self.run_cli(self.project_settings)

        with open(expected_file, "r", encoding="utf-8") as handle:
            expected_results = json.load(handle)

        for led_wall_name, result in results.items():
            led_wall = self.project_settings.get_led_wall(led_wall_name)
            if led_wall.is_verification_wall:
                continue

            self.assertTrue(os.path.exists(result.ocio_config_output_file))
            self.assertTrue(os.path.exists(result.lut_output_file))
            self.assertTrue(os.path.exists(result.calibration_results_file))
            self.assertEqual(expected_results, result.calibration_results)

    def test_run_cli_multi_wall(self):
        # Add A Second Wall
        self.project_settings.copy_led_wall(self.project_settings.led_walls[0].name, "LedWall2")

        # Override the roi so we have to run the auto detection
        self.project_settings.led_walls[0].roi = None
        self.project_settings.led_walls[1].roi = None

        # Set the new wall to the same sequence as the first wall for testing
        original_sequence = self.project_settings.led_walls[0].input_sequence_folder
        self.project_settings.led_walls[1].input_sequence_folder = original_sequence

        # Set the second wall as a reference wall for execution testing
        self.project_settings.led_walls[1].reference_wall = self.led_wall
        self.project_settings.led_walls[1].match_reference_wall = True
        self.project_settings.led_walls[1].auto_wb_source = False

        results = self.run_cli(self.project_settings)
        for led_wall_name, result in results.items():
            led_wall = self.project_settings.get_led_wall(led_wall_name)
            if led_wall.is_verification_wall:
                continue

            expected_file = self.get_results_file(led_wall)
            with open(expected_file, "r", encoding="utf-8") as handle:
                expected_results = json.load(handle)

            self.assertTrue(os.path.exists(result.ocio_config_output_file))
            self.assertTrue(os.path.exists(result.lut_output_file))
            self.assertTrue(os.path.exists(result.calibration_results_file))
            self.assertEqual(expected_results, result.calibration_results)


class TestProjectExternalWhite(TestProject):
    project_name = "SampleProject2_External_White_NoLens"

    def test_external_white_no_lens(self):
        results = self.run_cli(self.project_settings)
        for led_wall_name, result in results.items():
            led_wall = self.project_settings.get_led_wall(led_wall_name)
            if led_wall.is_verification_wall:
                continue

            expected_file = self.get_results_file(led_wall)
            with open(expected_file, "r", encoding="utf-8") as handle:
                expected_results = json.load(handle)

            self.assertTrue(os.path.exists(result.ocio_config_output_file))
            self.assertTrue(os.path.exists(result.lut_output_file))
            self.assertTrue(os.path.exists(result.calibration_results_file))
            self.assertEqual(expected_results, result.calibration_results)

    def get_sample_project_plates(self):
        result = super().get_sample_project_plates()
        return os.path.join(result, "A102_C015_1027M2_001.R3D")


class TestCLIGeneratePatterns(TestProject):
    project_name = "SampleProject2_External_White_NoLens"

    def test_cli_pattern_generation(self):
        temp_project_settings = tempfile.NamedTemporaryFile(suffix=".json", mode='w', delete=False).name
        self.project_settings.to_json(temp_project_settings)
        result = generate_patterns(
            temp_project_settings,
            self.project_settings.output_folder
        )
        os.remove(temp_project_settings)

        patches_folder = os.path.join(self.project_settings.output_folder, "patches")
        files = os.listdir(patches_folder)
        self.assertTrue(len(files), 1)
        images = os.listdir(os.path.join(patches_folder, files[0], self.project_settings.file_format))
        self.assertTrue(len(images), 45)
        self.assertTrue(os.path.exists(result))
        shutil.rmtree(patches_folder)
        os.remove(result)
