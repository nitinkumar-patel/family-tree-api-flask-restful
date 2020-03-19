from flask import Flask
from db import db, migrate, cors


def create_app(*, testing=False):
    app = Flask(__name__)

    # load config
    app.config.from_pyfile('settings.py')

    # use environment variables if in prod
    if testing:
        app.config["TESTING"] = True
        database_uri = "sqlite:///:memory:"
    else:
        database_uri = "sqlite:///db.sqlite"

    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    @app.before_first_request
    def create_tables():
        db.create_all()

    # apply overrides for tests
    # app.config.update(config_overrides)

    # setup db
    db.init_app(app)

    migrate.init_app(app, db)

    cors.init_app(app)

    url_prefix = '/api/v1/'

    # import bluprints
    from home.views import home_app
    # from app.views import app_app
    from family_tree.views import family_tree_app

    # regester blueprints
    app.register_blueprint(home_app, url_prefix=url_prefix)
    # app.register_blueprint(app_app, url_prefix=url_prefix)
    app.register_blueprint(family_tree_app, url_prefix=url_prefix)

    return app
