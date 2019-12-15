import json

import sqlalchemy
from flask import request
from flask_restful import Resource, marshal
from sqlalchemy import and_

from source.db import db, SiteUser, Address, Library, LibBooks
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
            # check if username already exists
            if db.session.query(SiteUser).filter(SiteUser.username == data.get('username')).first():
                return {'ErrorMessage': 'This username already exists'}, 409

            # check if all of the posted info has it's column in DB
            try:
                new = SiteUser(**data)
            except TypeError:
                return {'ErrorMessage': 'Excessive arguments posted'}, 400
            db.session.add(new)

            # create library for this user
            new_lib = Library(user_id=db.session.query(SiteUser).filter(SiteUser.username == data.get('username'))
                              .first().id)
            db.session.add(new_lib)
            db.session.commit()
            return marshal(db.session.query(SiteUser).all(), user_struct), 201
        return {'ErrorMessage': 'Not enough arguments'}, 400

    def patch(self, user_id=None):
        if user_id:
            data = json.loads(request.data)
            if data.get('id'):
                return {'ErrorMessage': "You can't change ID"}, 403

            if data.get('address_id'):
                if not db.session.query(Address).get(data.get('address_id')):
                    return {'ErrorMessage': 'No such address'}, 404

            if db.session.query(SiteUser).get(user_id):
                # check if all of the posted info has it's column in DB
                try:
                    db.session.query(SiteUser).filter(SiteUser.id == user_id).update(data)
                except sqlalchemy.exc.InvalidRequestError:
                    return {'ErrorMessage': 'Excessive arguments posted'}, 400
                db.session.commit()
                return marshal(db.session.query(SiteUser).get(user_id), user_struct), 200
            return {'ErrorMessage': 'No such user'}, 404
        return {'ErrorMessage': 'User not specified'}, 400

    def delete(self, user_id=None):
        if user_id:
            user = db.session.query(SiteUser).get(user_id)
            if user:
                # also we need to delete this user's library
                lib = db.session.query(Library).filter(Library.user_id == user_id).first()
                lib_books = db.session.query(LibBooks).filter(LibBooks.lib_id == lib.id).all()

                db.session.delete(user)
                db.session.delete(lib)
                for lb in lib_books:
                    db.session.delete(lb)
                db.session.commit()

                return marshal(db.session.query(SiteUser).order_by(SiteUser.id).all(), user_struct), 200
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
        # check if all necessary info posted
        if (data.get('street_addr') and data.get('city') and data.get('region')
                and data.get('zip') and data.get('country')):

            # check if this address is in DB already, unique address its city + street_addr
            if db.session.query(Address).filter(and_(Address.street_addr == data.get('street_addr'),
                                                     Address.city == data.get('city'))).first():
                return {'ErrorMessage': 'This address already exists'}, 403

            # check if all of the posted info has it's column in DB
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
                return {'ErrorMessage': "You can't change ID"}, 403
            if db.session.query(Address).get(addr_id):
                # check if all of the posted info has it's column in DB
                try:
                    db.session.query(Address).filter(Address.id == addr_id).update(data)
                except sqlalchemy.exc.InvalidRequestError:
                    return {'ErrorMessage': 'Excessive arguments posted'}, 400
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
                return marshal(db.session.query(Address).order_by(Address.id).all(), address_struct), 200
            return {'ErrorMessage': 'No such address'}, 404
        return {'ErrorMessage': 'Address not specified'}, 400
