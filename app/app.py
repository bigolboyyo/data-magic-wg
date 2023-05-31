from flask import Flask, request, abort, g
from app import app

@app.route('/delete_frontmatter', methods=['POST'])
def remove_front_matter_endpoint():
    # Get the file path from the request data
    data = request.get_json()
    directory_path = data['directory_path']

    # Remove the YAML front matter block from the file
    
    file_paths = glob.glob(os.path.join(directory_path, '*.md'))

    with app.app_context():
        generator = current_app.Climate_Tech_Handbook
        for file_path in file_paths:
            generator.delete_fields_except_title(file_path)


    # Return a response indicating success
    return jsonify({'message': 'YAML front matter removed successfully'})


if __name__ == "__main__":
    app.run(debug=True)
