from flask import jsonify
from app import Climate_Tech_Handbook, GENERATORS
from utils.utils import create_generator


def get_generator(data):
    # Get the generator_data and generator_id from the provided data
    generator_data = data.get("generator")
    generator_id = data.get("generator_id")

    # If generator_id is provided, attempt to retrieve the generator from the GENERATORS dictionary
    if generator_id:
        generator = GENERATORS.get(generator_id)
        # If the generator is not found, return an error message and 404 status
        if not generator:
            return None, jsonify({"error": "Generator not found"}), 404

    # If generator_data is provided, create a new generator with the given configuration
    elif generator_data:
        yml_files = generator_data.get("yml_files", [])
        csv_files = generator_data.get("csv_files", [])
        template_mds = generator_data.get("template_mds", [])
        output_dir = generator_data.get("output_dir", "output")

        generator = create_generator(yml_files, csv_files, template_mds, output_dir)

        # If a generator_id is provided, store the newly created generator in the GENERATORS dictionary
        if generator_id:
            GENERATORS[generator_id] = generator
    # If neither generator_id nor generator_data are provided, use the Climate_Tech_Handbook instance by default
    else:
        try:
            generator = Climate_Tech_Handbook
        except:
            print(f"Climate Tech Handbook default generator not initialized.")

    # Return the generator, None for the error message, and None for the status code
    return generator, None, None
