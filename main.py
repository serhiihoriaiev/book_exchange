from flask import Flask

from config import get_config
from db import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())
    db.init_app(app)
    db.create_all()
    return app


if __name__ == '__main__':
    create_app().run(debug=True)
