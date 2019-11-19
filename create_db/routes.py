from flask_restful import Resource

from db import db


class CreateDBRes(Resource):
    def get(self):
        db.create_all()
        db.session.commit()
        return "Database created"