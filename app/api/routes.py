from flask import jsonify, request
from app.api import cth_api
from app import Climate_Tech_Handbook
from utils.generator_utils import edit_file
from utils.utils import create_generator
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

    # call the edit_file function
    edit_file(file_path, markdown, start_line, end_line)

    # generate and write output
    output = await Climate_Tech_Handbook.create_output(file_path)
    await Climate_Tech_Handbook.write_output(file_path, output)

    # return a response indicating success
    return jsonify({"message": "File edited successfully"})


@cth_api.route("/add_tags", methods=["POST"])
def add_tags_endpoint():
    # get the file path and tags from the request data
    data = request.get_json()
    tags = data["tags"]
    generator_data = data.get("generator")

    # if generator data is provided, create a new generator with the provided data
    if generator_data:
        yml_files = generator_data.get("yml_files", [])
        csv_files = generator_data.get("csv_files", [])
        template_mds = generator_data.get("template_mds", [])
        output_dir = generator_data.get("output_dir", "")

        generator = create_generator(yml_files, csv_files, template_mds, output_dir)
        file_path = data.get("file_path")
    else:
        # use the Climate_Tech_Handbook instance by default
        try:
            generator = Climate_Tech_Handbook
        except:
            print(f"Climate Tech Handbook default generator not initialized.")

        # construct the file path
        file_path = os.path.join(
            os.getcwd(), "app", "output", "solution-abandoned-farmland-restoration.md"
        )
        print("file path:", file_path)

    # call the add_tags method on the generator instance
    generator.add_tags(file_path, tags)

    # return a response indicating success
    return jsonify({"message": "Tags added successfully"})
