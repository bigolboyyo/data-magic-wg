from flask import Flask
from dotenv import load_dotenv
from .utils.utils import get_env_vars, create_generator

load_dotenv()

app = Flask(__name__)

yml_files = ["data/prompts/prompts.yml"]
csv_files = ["data/csv/file_info.csv"]
template_mds = ["data/templates/template.md"]
output_dir = "output"

Climate_Tech_Handbook = None  # initialize as None

GENERATORS = {}


def create_climate_tech_handbook():
    global Climate_Tech_Handbook  # access the global variable
    Climate_Tech_Handbook = create_generator(
        yml_files, csv_files, template_mds, output_dir
    )


# You could consider this our main() method for the Flask app initialization
async def initialize():
    await create_climate_tech_handbook()


# Import cth_api after the definitions of Climate_Tech_Handbook and GENERATORS
from .api.routes import cth_api

app.register_blueprint(cth_api)
