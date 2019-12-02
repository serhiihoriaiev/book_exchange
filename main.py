from flask import Flask, render_template

from config import get_config
from db import db, migrate
from routes import routes_bp


def create_app(env='DEV'):
    app = Flask(__name__)
    app.config.from_object(get_config(env))
    app.register_blueprint(routes_bp)
    with app.app_context():
        db.init_app(app)
        db.create_all()
        migrate.init_app(app, db)
    return app


if __name__ == '__main__':
    create_app().run(debug=True)
