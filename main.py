from flask import Flask

from config import get_config
from source.db import db, migrate
from source import routes_bp


def create_app(env='DEV'):
    app = Flask(__name__)
    app.config.from_object(get_config(env))
    app.register_blueprint(routes_bp)
    with app.app_context():
        migrate.init_app(app, db)
        db.init_app(app)
        db.create_all()

    return app


if __name__ == '__main__':
    create_app().run(debug=True, host='0.0.0.0', port='8000')
