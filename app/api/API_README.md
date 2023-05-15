# Climate Tech Handbook API Guide

This guide will help you understand how to use the Climate Tech Handbook API using Postman for making HTTP requests.

## Overview

The API provides functionality to edit files, add tags, insert images, and add sections. By default, the API uses the Climate Tech Handbook instance for performing these operations. However, you can also create custom generator instances by passing in `generator_data` or a `generator_id` from a previously created generator. To create a custom generator, simply use any of the endpoints and reference the `get_generator` method code block at the bottom of this README.

## Prerequisites

- Make sure you have the Climate Tech Handbook API up and running locally or on a server.
- Install [Postman](https://www.postman.com/downloads/) if you haven't already.

## How to use Postman

1. Open Postman.
2. In the top-left corner, click the **+** button to create a new request tab.
3. Select the request method (POST for all the endpoints in this API) from the dropdown.
4. Enter the API endpoint URL. Make sure to include the appropriate `localhost` address and port (e.g., `http://localhost:5000/edit_file`).
5. Click on the **Body** tab below the URL input field.
6. Select the **raw** radio button and choose **JSON** from the dropdown menu.
7. Copy and paste the sample request JSON for the desired endpoint into the input field.
8. Modify the sample JSON as needed.
9. Click the **Send** button to send the request.
10. Check the response at the bottom of the Postman window.

## API Endpoints

### 1. Edit File

- **URL**: `/edit_file`
- **Method**: `POST`
- **Data Params**: `file_path`, `markdown`, `start_line`, `end_line`, `generator`, `generator_id`

**Sample Request:**

```
{
"file_path": "app/output/solution-abandoned-farmland-restoration.md",
"markdown": "## Edited section",
"start_line": 10,
"end_line": 15,
}
```

### 2. Add Tags

- **URL**: `/add_tags`
- **Method**: `POST`
- **Data Params**: `tags`, `generator`, `generator_id`, `file_directory`, `file_name`

**Sample Request:**

```
{
"tags": ["tag1", "tag2"],
"generator_id": "custom_generator_1",
"file_directory": "output",
"file_name": "solution-abandoned-farmland-restoration.md"
}
```

### 3. Insert Image

- **URL**: `/insert_image`
- **Method**: `POST`
- **Data Params**: `file_path`, `image_path`, `caption`, `position`, `generator`, `generator_id`

**Sample Request:**

```
{
"file_path": "app/output/solution-abandoned-farmland-restoration.md",
"image_path": "app/static/images/sample_image.jpg",
"caption": "Sample image caption",
"position": 12,
}
```

### 4. Add Section

- **URL**: `/add_section`
- **Method**: `POST`
- **Data Params**: `file_path`, `header_text`, `position`, `generator`, `generator_id`

**Sample Request:**

```
{
"file_path": "app/output/solution-abandoned-farmland-restoration.md",
"header_text": "New Section",
"position": 8,
}
```

### Example: Using generator_id

Assuming there's an existing generator with the identifier `custom_generator_1`, here's how you can access the `add_tags` endpoint with `generator_id`:

```
{
  "tags": ["tag1", "tag2"],
  "generator_id": "custom_generator_1",
  "file_directory": "output",
  "file_name": "solution-abandoned-farmland-restoration.md"
}
```

### Example: Using generator_data

Here's an example of accessing the `add_tags` endpoint by providing `generator_data` for creating a new generator on-the-fly:

```
{
  "tags": ["tag1", "tag2"],
  "generator": {
    "yml_files": ["path/to/yml1", "path/to/yml2"],
    "csv_files": ["path/to/csv1", "path/to/csv2"],
    "template_mds": ["path/to/template_md1", "path/to/template_md2"],
    "output_dir": "output"
  },
  "file_directory": "output",
  "file_name": "solution-abandoned-farmland-restoration.md"
}
```

## `get_generator`

```
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
```
