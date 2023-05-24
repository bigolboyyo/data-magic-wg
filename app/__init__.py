from flask import Flask, g, abort, request
from dotenv import load_dotenv
from .utils.utils import get_env_vars, create_generator, get_generator

import json
import os

load_dotenv()

app = Flask(__name__)

def load_climate_tech_handbook():
    if os.path.exists('generator.json'):
        with open('generator.json', 'r') as f:
            data = json.load(f)
        g.climate_tech_handbook = create_generator(**data[0]["generator_data"])

@app.before_first_request
def load_default_generator():
    load_climate_tech_handbook()

@app.before_request
def check_generator():
    try:
        generator_info = get_generator(request.get_json())
        if generator_info[0]:
            g.generator = generator_info[0]
        else:
            g.generator = g.climate_tech_handbook
    except Exception as e:
        abort(400, str(e))
