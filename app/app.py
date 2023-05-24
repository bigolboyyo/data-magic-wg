from api.routes import api_bp
from api.routes_fileapi import fileapi_bp

# Import the app and the global variable from init
from . import app, Climate_Tech_Handbook

app.register_blueprint(fileapi_bp)
app.register_blueprint(api_bp)


if __name__ == "__main__":
    app.run(debug=True)
