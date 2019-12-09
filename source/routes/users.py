import json

from flask import request
from flask_restful import Resource, marshal

from source.db import db, SiteUser
from source.structures import user_struct


class UserRes(Resource):
    def get(self, user_id=None):
        if user_id:
            data = db.session.query(SiteUser).get(user_id)
            return marshal(data, user_struct) if data else {'ErrorMessage': 'No such user'}, 200 if data else 404
        data = db.session.query(SiteUser).all()
        return marshal(data, user_struct), 200

    def post(self):
        data = json.loads(request.data)
        if data.get('username') and data.get('group'):
            if db.session.query(SiteUser).filter(SiteUser.username == data.get('username')).first():
                return {'ErrorMessage': 'This username already exists'}, 409
            try:
                new = SiteUser(**data)
            except TypeError:
                return {'ErrorMessage': 'Excessive arguments posted'}, 400
            db.session.add(new)
            db.session.commit()
            return marshal(db.session.query(SiteUser).all(), user_struct), 201
        return {'ErrorMessage': 'Not enough arguments'}, 400

    def patch(self, user_id=None):
        data = json.loads(request.data)
        if user_id:
            if db.session.query(SiteUser).get(user_id):
                db.session.query(SiteUser).filter(SiteUser.id == user_id).update(data)
                db.session.commit()
                return marshal(db.session.query(SiteUser).all(), user_struct), 200
            return {'ErrorMessage': 'No such user'}, 404

    def delete(self, user_id=None):
        if user_id:
            user = db.session.query(SiteUser).get(user_id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return marshal(db.session.query(SiteUser).all(), user_struct), 200
            return {'ErrorMessage': 'No such user'}, 404
