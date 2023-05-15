import csv
import os, re
import requests
import yaml
import openai
import pdb


def to_snake_case(string):
    return string.lower().replace(" ", "_")


def save_progress(progress):
    with open("progress.txt", "w") as f:
        f.write(str(progress))


def load_progress():
    try:
        with open("progress.txt", "r") as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0


def list_models():
    models = openai.Model.list()
    print(models.data)


def stage_content(yml_files, csv_files, template_files, output_dir):
    if not isinstance(yml_files, list):
        yml_files = [yml_files]
    if not isinstance(csv_files, list):
        csv_files = [csv_files]
    if not isinstance(template_files, list):
        template_files = [template_files]

    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    except FileExistsError:
        return 0

    prompts = {}
    file_info = []
    templates = {}

    for yml_file in yml_files:
        with open(yml_file) as f:
            prompts.update(yaml.safe_load(f))

    for csv_file in csv_files:
        with open(csv_file, newline="") as f:
            reader = csv.DictReader(f)
            file_info.extend([row for row in reader])

    for template_file in template_files:
        template_name = os.path.splitext(os.path.basename(template_file))[0]
        with open(template_file) as f:
            templates[template_name] = f.read()

    return prompts, file_info, templates


def generate_completion(
    api_key, prompt, engine, temp, max_tokens, n, stop, freq_pen, pres_pen
):
    openai.api_key = api_key

    try:
        response = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            max_tokens=max_tokens,
            n=n,
            stop=stop,
            temperature=temp,
            frequency_penalty=freq_pen,
            presence_penalty=pres_pen,
        )

        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error generating completion: {e}")
        return None


def validate_and_assign(content_generator, prompts, file_info, templates):
    if prompts is not None:
        content_generator.prompts = prompts
    else:
        raise FileNotFoundError(
            f"Could not load prompts from '{content_generator.yml_file}'"
        )

    if file_info is not None:
        content_generator.file_info = file_info
    else:
        raise FileNotFoundError(
            f"Could not load file info from '{content_generator.csv_file}'"
        )

    if templates is not None:
        content_generator.templates = templates
    else:
        raise FileNotFoundError(
            f"Could not load template from '{content_generator.template_md}'"
        )


def generate_content(generator, prompt):
    if generator.request_count < generator.max_requests:
        completion = generator.create_completion(prompt)
        generator.request_count += 1
        return completion
    else:
        return "Max requests reached. No more content will be generated."


async def generate_output(generator, page, template_name="template"):
    prompt_keys = generator.extract_prompt_keys(template_name)
    generator.prompts = {
        to_snake_case(k): v
        for k, v in generator.prompts.items()
        if k.lower() != "topic"
    }

    print(f"{prompt_keys}")
    completions = []

    for key in prompt_keys:
        key = key.lower()
        if key == "topic":  # Skip if the key is 'topic'
            continue
        prompt = generator.prompts[key]["prompt"].replace("{Topic}", page["Topic"])
        completion = generate_content(generator, prompt)
        completions.append(completion)

    # Create a dictionary with keys and their corresponding completions
    pdb.set_trace()
    keys_and_completions = {
        key: completion.strip() for key, completion in zip(prompt_keys, completions)
    }
    # Add the 'topic' key to the dictionary
    keys_and_completions["topic"] = page["Topic"]

    print(generator.templates.keys())
    # Format the output using the keys and completions dictionary
    output = generator.templates[template_name].format(**keys_and_completions)

    return output


# adding new markdown content to a file at a specified line or range of lines
def edit_file(file_path, markdown, start_line=None, end_line=None):
    with open(file_path, "r+") as file:
        lines = file.readlines()
        if start_line and end_line:
            lines[start_line - 1 : end_line] = [f"{markdown}\n"]
        else:
            lines.append(f"{markdown}\n")
        file.seek(0)
        file.writelines(lines)


# takes a list of tags as input and inserts them at the top of the markdown file.
def add_tags(file_path, tags):
    with open(file_path, "r+") as file:
        content = file.read()
        new_content = f"Tags: {', '.join(tags)}\n\n{content}"
        file.seek(0)
        file.write(new_content)


# takes the path to the image file, its caption, and its position in the markdown file as input, and inserts an image tag at that position.
def insert_image(file_path, image_path, caption, position):
    with open(file_path, "r+") as file:
        lines = file.readlines()
        lines.insert(position, f"![{caption}]({image_path})\n")
        file.seek(0)
        file.writelines(lines)


# takes the header text and its position in the markdown file as input, and inserts a new section with a header and an empty body at that position
def add_section(file_path, header_text, position):
    with open(file_path, "r+") as file:
        lines = file.readlines()
        lines.insert(position, f"## {header_text}\n\n")
        lines.insert(position + 1, "TODO\n\n")
        file.seek(0)
        file.writelines(lines)


def extract_keys_from_template(template_path):
    with open(template_path, "r") as f:
        content = f.read()

    keys = []
    for key in re.findall(r"\{(.*?)\}", content):
        if key.lower() != "topic":
            keys.append(key)
