import json

from flask import request
from flask_restful import Resource, marshal

from source.db import db, SiteUser
from source.structures import user_struct


class UserRes(Resource):
    def get(self):
        data = db.session.query(SiteUser).all()
        return marshal(data, user_struct), 200

    def post(self):
        data = json.loads(request.data)
        if data.get('username') and data.get('group'):
            if db.session.query(SiteUser).filter(SiteUser.username == data.get('username')).first():
                return {'ErrorMessage': 'This username already exists'}, 409
            new = SiteUser(**data)
            db.session.add(new)
            db.session.commit()
            return marshal(db.session.query(SiteUser).all(), user_struct), 201
        return {'ErrorMessage': 'Not enough arguments'}, 400
