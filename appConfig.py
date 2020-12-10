from flask import Flask
from db_file import db
from consumer import bp


# Class-based application configuration
class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///user.db'  # File-based SQL database
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids SQLAlchemy warning


def create_app():
    """ Flask application factory """

    # Create Flask app load app.config
    app = Flask(__name__)
    app.config.from_object(__name__ + '.ConfigClass')

    # adding user Blueprint
    app.register_blueprint(bp)
    # Initialize Flask-SQLAlchemy
    db.init_app(app)

    # Create all database tables
    with app.app_context():
        db.create_all()
    return app
