from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_db_integration(app):
    db.init_app(app)
