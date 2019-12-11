import json

from flask import request
from flask_restful import Resource, marshal

from source.db import db, SiteUser, Address
from source.structures import user_struct, address_struct


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
        if user_id:
            data = json.loads(request.data)
            if data.get('id'):
                return {'ErrorMessage': 'You can''t change ID'}, 403
            if db.session.query(SiteUser).get(user_id):
                db.session.query(SiteUser).filter(SiteUser.id == user_id).update(data)
                db.session.commit()
                return marshal(db.session.query(SiteUser).get(user_id), user_struct), 200
            return {'ErrorMessage': 'No such user'}, 404
        return {'ErrorMessage': 'User not specified'}, 400

    def delete(self, user_id=None):
        if user_id:
            user = db.session.query(SiteUser).get(user_id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return marshal(db.session.query(SiteUser).all(), user_struct), 200
            return {'ErrorMessage': 'No such user'}, 404
        return {'ErrorMessage': 'User not specified'}, 400

class AddrRes(Resource):
    def get(self, addr_id=None):
        if addr_id:
            data = db.session.query(Address).get(addr_id)
            return marshal(data, address_struct) if data else {'ErrorMessage': 'No such address'}, 200 if data else 404
        return marshal(db.session.query(Address).all(), address_struct), 200

    def post(self):
        data = json.loads(request.data)
        if (data.get('street_addr') and data.get('city') and data.get('region')
                and data.get('zip') and data.get('country')):
            try:
                new = Address(**data)
            except TypeError:
                return {'ErrorMessage': 'Excessive arguments posted'}, 400
            db.session.add(new)
            db.session.commit()
            return marshal(db.session.query(Address).all(), address_struct), 201
        return {'ErrorMessage': 'Not enough arguments'}, 400

    def patch(self, addr_id=None):
        if addr_id:
            data = json.loads(request.data)
            if data.get('id'):
                return {'ErrorMessage': 'You can''t change ID'}, 403
            if db.session.query(Address).get(addr_id):
                db.session.query(Address).filter(Address.id == addr_id).update(data)
                db.session.commit()
                return marshal(db.session.query(Address).get(addr_id), address_struct), 200
            return {'ErrorMessage': 'No such address'}, 404
        return {'ErrorMessage': 'Address not specified'}, 400

    def delete(self, addr_id=None):
        if addr_id:
            data = db.session.query(Address).get(addr_id)
            if data:
                db.session.delete(data)
                db.session.commit()
                return marshal(db.session.query(Address).all(), address_struct), 200
            return {'ErrorMessage': 'No such address'}, 404
        return {'ErrorMessage': 'Address not specified'}, 400
