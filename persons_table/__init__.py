from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from persons_table.config import Config

bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    """Creates application instances with all extensions registered

    :return: app instance
    :rtype: class 'flask.app.Flask'
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    Bootstrap(app)
    db.init_app(app)
    migrate.init_app(app, db)

    from persons_table.persons.routes import persons

    app.register_blueprint(persons)

    return app
