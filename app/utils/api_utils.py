from flask import jsonify
from app import Climate_Tech_Handbook, GENERATORS
from utils.utils import create_generator


def get_generator(data):
    generator_data = data.get("generator")
    generator_id = data.get("generator_id")

    if generator_id:
        generator = GENERATORS.get(generator_id)
        if not generator:
            return None, jsonify({"error": "Generator not found"}), 404

    elif generator_data:
        yml_files = generator_data.get("yml_files", [])
        csv_files = generator_data.get("csv_files", [])
        template_mds = generator_data.get("template_mds", [])
        output_dir = generator_data.get("output_dir", "output")

        generator = create_generator(yml_files, csv_files, template_mds, output_dir)

        if generator_id:
            GENERATORS[generator_id] = generator
    else:
        try:
            generator = Climate_Tech_Handbook
        except:
            print(f"Climate Tech Handbook default generator not initialized.")

    return generator, None, None
