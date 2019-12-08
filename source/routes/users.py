from flask_restful import Resource, marshal

from source.db import db, SiteUser
from source.structures import user_struct


class UserRes(Resource):
    def get(self):
        data = db.session.query(SiteUser).all()
        return marshal(data, user_struct), 200
