import unittest
from openfast_toolbox.fastfarm.MoorDynCaseCreation import MoorDynCaseCreation
import os
import math

class TestMoorDynCaseCreation(unittest.TestCase):
    """
    Unit tests for the MoorDynCaseCreation class.
    """

    def setUp(self):
        """
        Setup for the tests. Creates a temporary template file.
        """
        self.template_path = "temp_template.txt"
        self.output_path = "temp_output.txt"

        # Create a sample template file
        with open(self.template_path, 'w') as f:
            f.write("LineLength={LineLength}\n")
            f.write("LineDiameter={LineDiameter}\n")
            f.write("AnchorDepth={AnchorDepth}\n")
            f.write("LineX={LineX}\n")
            f.write("LineY={LineY}\n")

        self.moordyn_case = MoorDynCaseCreation(self.template_path)

    def tearDown(self):
        """
        Cleanup temporary files.
        """
        if os.path.exists(self.template_path):
            os.remove(self.template_path)
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

    def test_generate_input_file(self):
        """
        Test the generation of the MoorDyn input file.
        """
        params = {
            "LineLength": 900.0,
            "LineDiameter": 0.1,
            "AnchorDepth": 50.0
        }

        self.moordyn_case.parse_parameters(params)
        self.moordyn_case.generate_input_file(self.output_path)

        # Verify the output file
        with open(self.output_path, 'r') as f:
            content = f.read()

        self.assertIn("LineLength=900.0", content)
        self.assertIn("LineDiameter=0.1", content)
        self.assertIn("AnchorDepth=50.0", content)

    def test_generate_input_file_missing_parameter(self):
        """
        Test the behavior when a required parameter is missing.
        """
        params = {
            "LineLength": 900.0,
            "LineDiameter": 0.1
            # Missing AnchorDepth
        }

        self.moordyn_case.parse_parameters(params)
        self.moordyn_case.generate_input_file(self.output_path)

        with open(self.output_path, 'r') as f:
            content = f.read()

        self.assertIn("LineLength=900.0", content)
        self.assertIn("LineDiameter=0.1", content)
        self.assertIn("AnchorDepth={AnchorDepth}", content)  # Placeholder should remain

    def test_rotation_logic(self):
        """
        Test the rotation functionality by verifying coordinate transformations.
        """
        params = {
            "LineX": 100.0,
            "LineY": 0.0
        }

        self.moordyn_case.parse_parameters(params)

        # Apply a 90-degree rotation
        self.moordyn_case.rotate_mooring_system(90)
        self.moordyn_case.generate_input_file(self.output_path)

        # Verify rotated coordinates
        with open(self.output_path, 'r') as f:
            content = f.read()

        self.assertIn("LineX=0.0", content)
        self.assertIn("LineY=100.0", content)

    def test_large_scale_simulation(self):
        """
        Test handling of a large-scale simulation configuration.
        """
        params = {
            f"LineLength_{i}": 900.0 + i for i in range(1000)
        }
        params.update({
            f"LineDiameter_{i}": 0.1 for i in range(1000)
        })
        params.update({
            f"AnchorDepth_{i}": 50.0 for i in range(1000)
        })

        self.moordyn_case.parse_parameters(params)
        self.moordyn_case.generate_input_file(self.output_path)

        # Verify the file was created successfully
        self.assertTrue(os.path.exists(self.output_path))

    def test_invalid_template_path(self):
        """
        Test behavior when the template file is missing.
        """
        invalid_case = MoorDynCaseCreation("non_existent_template.txt")

        with self.assertRaises(FileNotFoundError):
            invalid_case.generate_input_file(self.output_path)

if __name__ == "__main__":
    unittest.main()
