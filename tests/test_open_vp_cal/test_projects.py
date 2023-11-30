import os.path
import shutil
import json

from open_vp_cal.core import constants, ocio_config
from open_vp_cal.project_settings import ProjectSettings
from test_open_vp_cal.test_utils import TestProject


class BaseTestProjectPlateReuse(TestProject):
    def setUp(self):
        super(TestProject, self).setUp()
        self.project_settings = ProjectSettings.from_json(self.get_sample_project_settings())

        self.project_settings.output_folder = self.get_output_folder()
        if os.path.exists(self.project_settings.output_folder):
            shutil.rmtree(self.project_settings.output_folder)

        os.makedirs(self.project_settings.output_folder)
        for led_wall in self.project_settings.led_walls:
            current_plate = led_wall.input_sequence_folder
            folder_name = os.path.basename(current_plate)
            unit_test_input_folder_path = os.path.join(self.get_sample_plates(), folder_name)
            if not os.path.exists(unit_test_input_folder_path):
                raise Exception("Missing plate folder: {}".format(unit_test_input_folder_path))
            led_wall.input_sequence_folder = unit_test_input_folder_path


class TestProject7_ROE_WrongWB(BaseTestProjectPlateReuse):
    project_name = "Sample_Project7_ROE_WRONGWB"

    def test_project7_roe_wrong_wb(self):
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
            self.compare_data(expected_results, result.calibration_results)

class TestProject7_ROE_WrongWB_CS_EOTF(BaseTestProjectPlateReuse):
    project_name = "Sample_Project7_ROE_WRONGWB_CS_EOTF"

    def test_project7_roe_wrong_wb(self):
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
            self.compare_data(expected_results, result.calibration_results)


class TestProject7_ROE_WrongWB_CS_Only(BaseTestProjectPlateReuse):
    project_name = "Sample_Project7_ROE_WRONGWB_CS_Only"

    def test_project7_roe_wrong_wb(self):
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
            self.compare_data(expected_results, result.calibration_results)


class TestSample_Project1_ROE_Wall1_CSOnly(BaseTestProjectPlateReuse):
    project_name = "Sample_Project1_ROE_Wall1_CSOnly"

    def test_project1(self):
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
            self.compare_data(expected_results, result.calibration_results)


class TestSample_Project2_ROE_Wall1_CS_EOTF(BaseTestProjectPlateReuse):
    project_name = "Sample_Project2_ROE_Wall1_CS_EOTF"

    def test_project2(self):
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
            self.compare_data(expected_results, result.calibration_results)


class TestSample_Project3_ROE_Wall1_EOTF_CS(BaseTestProjectPlateReuse):
    project_name = "Sample_Project3_ROE_Wall1_EOTF_CS"

    def test_project3(self):
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
            self.compare_data(expected_results, result.calibration_results)


class TestSample_Project4_Reference_Wall(BaseTestProjectPlateReuse):
    project_name = "Sample_Project4_Reference_Wall"

    def test_project4(self):
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
            self.compare_data(expected_results, result.calibration_results)


class TestSample_Project5_Decoupled_Lens(BaseTestProjectPlateReuse):
    project_name = "Sample_Project5_Decoupled_Lens"

    def setUp(self):
        super().setUp()
        for led_wall in self.project_settings.led_walls:
            if led_wall.external_white_point_file:
                led_wall.external_white_point_file = os.path.join(
                    self.get_sample_plates(), "A104_C003_11080B_001.R3D", "A104_C003_11080B_001.01397369.exr")

    def test_project5(self):
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
            self.compare_data(expected_results, result.calibration_results)


class TestSample_Project6_Reference_Wall_With_Decoupled_Lens(BaseTestProjectPlateReuse):
    project_name = "Sample_Project6_Reference_Wall_With_Decoupled_Lens"

    def setUp(self):
        super().setUp()
        for led_wall in self.project_settings.led_walls:
            if led_wall.external_white_point_file:
                led_wall.external_white_point_file = os.path.join(
                    self.get_sample_plates(), "A104_C003_11080B_001.R3D", "A104_C003_11080B_001.01397369.exr")

    def test_project6(self):
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
            self.compare_data(expected_results, result.calibration_results)


class TestSample_Project8_AcesCCT(BaseTestProjectPlateReuse):
    project_name = "Sample_Project8_ACES_CCT_LUT"

    def test_project8(self):
        results = self.run_cli(self.project_settings)
        for led_wall_name, result in results.items():
            led_wall = self.project_settings.get_led_wall(led_wall_name)
            if led_wall.is_verification_wall:
                continue

            expected_ocio_file = os.path.join(
                self.get_sample_project_folder(),
                constants.ProjectFolders.EXPORT,
                constants.ProjectFolders.CALIBRATION,
                ocio_config.OcioConfigWriter.post_calibration_config_name)
            expected_file = self.get_results_file(led_wall)
            with open(expected_file, "r", encoding="utf-8") as handle:
                expected_results = json.load(handle)

            self.assertTrue(os.path.exists(result.lut_output_file))
            self.assertTrue(os.path.exists(result.calibration_results_file))
            self.files_are_equal(expected_ocio_file, result.ocio_config_output_file)
            self.compare_data(expected_results, result.calibration_results)

