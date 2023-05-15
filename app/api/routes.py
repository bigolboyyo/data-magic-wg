from flask import jsonify, request
from app.api import cth_api
from app import Climate_Tech_Handbook, GENERATORS
from utils.generator_utils import edit_file
from utils.utils import create_generator
from utils.api_utils import get_generator
import os


@cth_api.route("/hello")
def hello():
    return jsonify({"message": f"Hello, I am Flask!"})


@cth_api.route("/edit_file", methods=["POST"])
async def edit_file_endpoint():
    # get the file path and markdown content from the request data
    data = request.get_json()
    file_path = data["file_path"]
    markdown = data["markdown"]
    start_line = data.get("start_line")
    end_line = data.get("end_line")

    # get the generator instance
    generator, response = get_generator(data)
    if response:
        return response

    # call the edit_file function
    edit_file(file_path, markdown, start_line, end_line)

    # generate and write output
    output = await generator.create_output(file_path)
    await generator.write_output(file_path, output)

    # return a response indicating success
    return jsonify({"message": "File edited successfully"})


@cth_api.route("/add_tags", methods=["POST"])
def add_tags_endpoint():
    # get the file path and tags from the request data
    data = request.get_json()
    tags = data["tags"]
    generator_data = data.get("generator")
    generator_id = data.get("generator_id")
    file_directory = data.get("file_directory", "output")
    file_name = data.get("file_name", "solution-abandoned-farmland-restoration.md")

    # construct the file path
    file_path = os.path.join(os.getcwd(), "app", file_directory, file_name)
    print("file path:", file_path)

    # if generator_id is provided, use the existing generator with the given identifier
    if generator_id:
        generator = GENERATORS.get(generator_id)
        if not generator:
            return jsonify({"error": "Generator not found"}), 404

    # if generator data is provided, create a new generator with the provided data
    elif generator_data:
        yml_files = generator_data.get("yml_files", [])
        csv_files = generator_data.get("csv_files", [])
        template_mds = generator_data.get("template_mds", [])
        output_dir = generator_data.get("output_dir", "output")
        generator_id = generator_data.get("generator_id")

        generator = create_generator(yml_files, csv_files, template_mds, output_dir)

        # if a generator_id is provided, store the generator in the dictionary
        if generator_id:
            GENERATORS[generator_id] = generator
    else:
        # use the Climate_Tech_Handbook instance by default
        try:
            generator = Climate_Tech_Handbook
        except:
            print(f"Climate Tech Handbook default generator not initialized.")

    # call the add_tags method on the generator instance
    generator.add_tags(file_path, tags)

    # return a response indicating success
    return jsonify({"message": "Tags added successfully"})


@cth_api.route("/insert_image", methods=["POST"])
def insert_image_endpoint():
    data = request.get_json()
    file_path = data["file_path"]
    image_path = data["image_path"]
    caption = data["caption"]
    position = data["position"]
    generator_data = data.get("generator")
    generator_id = data.get("generator_id")

    if generator_id:
        generator = GENERATORS.get(generator_id)
        if not generator:
            return jsonify({"error": "Generator not found"}), 404

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

    generator.insert_image(file_path, image_path, caption, position)

    return jsonify({"message": "Image inserted successfully"})


@cth_api.route("/add_section", methods=["POST"])
def add_section_endpoint():
    data = request.get_json()
    file_path = data["file_path"]
    header_text = data["header_text"]
    position = data["position"]
    generator_data = data.get("generator")
    generator_id = data.get("generator_id")

    if generator_id:
        generator = GENERATORS.get(generator_id)
        if not generator:
            return jsonify({"error": "Generator not found"}), 404

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

    generator.add_section(file_path, header_text, position)

    return jsonify({"message": "Section added successfully"})
