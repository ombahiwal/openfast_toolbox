from openfast_toolbox.fastfarm.MoorDynCaseCreation import MoorDynCaseCreation

# Example setup for MoorDyn input file generation
if __name__ == "__main__":
    # Define parameters for MoorDyn input file
    mooring_params = {
        "LineLength": 850.0,  # Length of the mooring line in meters
        "LineDiameter": 0.075,  # Diameter of the line in meters
        "AnchorDepth": 40.0,  # Depth of the anchor in meters
        "Buoyancy": 1.1,  # Buoyancy factor (example parameter)
        "WaterDepth": 200.0,  # Depth of water
    }

    # Path to the MoorDyn template file
    base_template_path = "path_to_moordyn_template.txt"  # Replace with actual file path

    # Initialize the MoorDyn case creation class
    moordyn_case = MoorDynCaseCreation(base_template_path)

    # Parse parameters into the class
    moordyn_case.parse_parameters(mooring_params)

    # Specify the output file path for the generated MoorDyn input
    output_file_path = "output_moordyn_input.txt"

    # Generate the MoorDyn input file
    moordyn_case.generate_input_file(output_file_path)

    # Example of rotating the mooring system (for demonstration)
    rotation_angle = 45  # Rotation angle in degrees
    moordyn_case.rotate_mooring_system(rotation_angle)

    print(f"MoorDyn input setup complete. Output saved to {output_file_path}.")
