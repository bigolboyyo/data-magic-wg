from flask import Flask, request, abort, g
from app import app
# from utils import create_generator, get_generator

import json
import os
import sys

# root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.insert(0, root_dir)

# def load_climate_tech_handbook():
#     if os.path.exists('generator.json'):
#         with open('generator.json', 'r') as f:
#             data = json.load(f)
#         app.config['climate_tech_handbook'] = create_generator(**data[0]["generator_data"])

# @app.before_first_request
# def load_default_generator():
#     load_climate_tech_handbook()

# @app.before_request
# def check_generator():
#     try:
#         generator_info = get_generator(request.get_json())
#         if generator_info[0]:
#             g.generator = generator_info[0]
#         else:
#             g.generator = app.config['climate_tech_handbook']
#     except Exception as e:
#         abort(400, str(e))

if __name__ == "__main__":
    app.run(debug=True)
