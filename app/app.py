import sys, os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app import app, create_climate_tech_handbook


@app.before_first_request
async def initialize():
    await create_climate_tech_handbook()


if __name__ == "__main__":
    # Change to False to ignore any breakpoints/pdb traces, etc.
    app.run(debug=True)
