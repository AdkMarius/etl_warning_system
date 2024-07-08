from flask import Flask
from flask_cors import CORS

from warning_system.controllers import new_indicator


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    app.register_blueprint(new_indicator.bp)

    return app
