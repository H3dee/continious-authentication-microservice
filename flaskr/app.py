import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv

from .api import continious_auth
from .database import create_db_integration

BLUEPRINTS = [continious_auth]

load_dotenv(find_dotenv())


def create_app(config=None, app_name="continious-auth-microservice", blueprints=None):
    app = Flask(
        app_name,
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    create_db_integration(app)

    CORS(app)

    if config:
        app.config.from_pyfile(config)

    if blueprints is None:
        blueprints = BLUEPRINTS

    blueprints_fabrics(app, blueprints)

    return app


def blueprints_fabrics(app, blueprints):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
